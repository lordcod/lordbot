import nextcord
from nextcord.ext import commands, application_checks
from nextcord.utils import oauth_url

from bot.resources.ether import Emoji
from bot.misc import utils
from bot.databases.db import GuildDateBases
from bot.resources import info
from bot.views.translate import TranslateView
from bot.languages import (
    captcha as lang_captcha,
    activiti as lang_activiti,
    data as lang_datas
)

import jmespath
import googletrans
import asyncio
import random
import re

translator = googletrans.Translator()

EMOJI_REGEXP = re.compile(r"<(a?):([a-zA-Z_-]+):(\d{19})>")


class basic(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        content = (
            "Pong!🏓🎉\n"
            f"Latency: {(self.bot.latency)*100:.1f}ms"
        )

        await ctx.send(content)

    @commands.command()
    async def invite(self, ctx: commands.Context):
        invite_link = oauth_url(
            client_id=self.bot.user.id,
            permissions=nextcord.Permissions.all(),
            redirect_uri=info.site_link,
            scopes=("bot", "applications.commands"),
        )

        content = (
            "Special bot invitation to the server:\n"
            f"{invite_link}"
        )

        await ctx.send(content)

    @commands.command()
    async def captcha(self, ctx: commands.Context):
        gdb = GuildDateBases(ctx.guild.id)
        lang = gdb.get('language')
        data, code = await utils.generator_captcha(random.randint(3, 7))
        image_file = nextcord.File(
            data, filename="captcha.png", description="Captcha", spoiler=True)
        await ctx.send(content=lang_captcha.enter.get(lang), file=image_file)
        try:
            def check(
                m): return m.channel == ctx.channel and m.author == ctx.author
            message: nextcord.Message = await self.bot.wait_for("message",
                                                                timeout=30,
                                                                check=check)
        except asyncio.TimeoutError:
            await ctx.send(content=lang_captcha.failed.get(lang))
            return

        if message.content.upper() == code:
            await ctx.send((f"{Emoji.congratulation}"
                           f"{lang_captcha.congratulation.get(lang)}"))
        else:
            await ctx.send(content=lang_captcha.failed.get(lang))

    @commands.command(name="welcome-message")
    async def welcome_message(self, ctx: commands.Context):
        image_bytes = await utils.generate_welcome_message(ctx.author)

        file = nextcord.File(image_bytes, "welcome-message.png")

        embed = nextcord.Embed()
        embed.set_image("attachment://welcome-message.png")

        await ctx.send(embed=embed, file=file)

    @nextcord.slash_command(
        name="activiti",
        description="Create an activity",
    )
    @application_checks.guild_only()
    async def activiti(
        self,
        interaction: nextcord.Interaction,
        voice: nextcord.VoiceChannel = nextcord.SlashOption(
            required=True,
            name="voice",
            description=("Select the voice channel in which"
                         " the activity will work!")
        ),
        act: str = nextcord.SlashOption(
            required=True,
            name="activiti",
            description="Select the activity you want to use!",
            choices=[activ.get('label') for activ in info.activities_list],
        ),
    ) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        lang = gdb.get('language')
        color = gdb.get('color')

        activiti: dict = jmespath.search(
            f"[?label=='{act}']|[0]", info.activities_list)

        try:
            inv = await voice.create_invite(
                target_type=nextcord.InviteTarget.embedded_application,
                target_application_id=activiti.get('id')
            )
        except (nextcord.HTTPException, nextcord.NotFound):
            await interaction.response.send_message(
                content=lang_activiti.failed.get(lang))
            return

        view = nextcord.ui.View(timeout=None)
        view.add_item(nextcord.ui.Button(
            label="Activiti", emoji=Emoji.roketa, url=inv.url))

        embed = nextcord.Embed(
            title=f"**{lang_activiti.embed_title.get(lang)}**",
            color=color,
            description=lang_activiti.embed_description.get(lang)
        )
        embed.add_field(
            name=lang_activiti.fields_label.get(lang),
            value=activiti.get('label')
        )
        embed.add_field(
            name=lang_activiti.fields_max_user.get(lang),
            value=activiti.get('max_user')
        )

        await interaction.response.send_message(embed=embed,
                                                view=view)

    @nextcord.message_command(name="Translate")
    async def translate(
        self,
        inters: nextcord.Interaction,
        message: nextcord.Message
    ):
        if not message.content:
            await inters.response.send_message("This message has no content, "
                                               "so we will not be able to "
                                               "translate it.")

        data = jmespath.search(
            f"[?discord_language=='{inters.locale}']|[0]", lang_datas)

        result = translator.translate(
            text=message.content, dest=data.get('google_language'))

        view = TranslateView(inters.guild_id, data.get('google_language'))

        await inters.response.send_message(content=result.text,
                                           view=view,
                                           ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(basic(bot))
