import nextcord

from bot.views.settings._view import DefaultSettingsView
from .distribution import distrubuters

from bot.databases.varstructs import IdeasPayload
from bot.databases import GuildDateBases
from bot.views import settings_menu
from bot.views.ideas import IdeaView
from bot.languages import i18n
from bot.misc.time_transformer import display_time


class DropDown(nextcord.ui.Select):
    def __init__(self, guild_id):
        self.gdb = GuildDateBases(guild_id)

        options = [
            nextcord.SelectOption(
                label='Suggest',
                value='suggest'
            ),
            nextcord.SelectOption(
                label='Offers',
                value='offers'
            ),
            nextcord.SelectOption(
                label='Approved',
                value='approved'
            ),
            nextcord.SelectOption(
                label='Moderation roles',
                value='moderation_roles'
            ),
            nextcord.SelectOption(
                label='Cooldown',
                value='cooldown'
            )
        ]

        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        catalog = self.values[0]
        view = distrubuters.get(catalog)(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class IdeasView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(self, guild: nextcord.Guild) -> None:
        gdb = GuildDateBases(guild.id)
        color: int = gdb.get('color')
        locale: str = gdb.get('language')
        ideas: IdeasPayload | None = gdb.get('ideas')

        enabled = ideas.get('enabled')

        self.embed = nextcord.Embed(
            title="Ideas",
            description="",
            color=color
        )

        super().__init__()

        if channel_suggest := guild.get_channel(ideas.get("channel_suggest_id")):
            self.embed.description += ("Channel suggest: "
                                       f"{channel_suggest.mention}\n")

        if channel_offers := guild.get_channel(ideas.get("channel_offers_id")):
            self.embed.description += ("Channel offers: "
                                       f"{channel_offers.mention}\n")

        if channel_approved := guild.get_channel(
                ideas.get("channel_approved_id")):
            self.embed.description += ("Channel approved: "
                                       f"{channel_approved.mention}\n")

        if cooldown := ideas.get('cooldown'):
            self.embed.description += ("Cooldown: "
                                       f"{display_time(cooldown)}\n")

        if moderation_role_ids := ideas.get("moderation_role_ids"):
            moderation_roles = filter(lambda item: item is not None,
                                      map(guild.get_role,
                                          moderation_role_ids))
            if moderation_roles:
                self.embed.description += (
                    "Moderation roles: "
                    f"{', '.join([role.mention for role in moderation_roles])}"
                )

        self.allow_image.style = nextcord.ButtonStyle.green if ideas.get(
            'allow_image', True) else nextcord.ButtonStyle.red
        self.thread_delete.style = nextcord.ButtonStyle.green if ideas.get(
            'thread_delete', True) else nextcord.ButtonStyle.red

        if enabled:
            self.remove_item(self.enabled)
        else:
            self.remove_item(self.disabled)
            self.allow_image.disabled = True
            self.thread_delete.disabled = True

        self.add_item(DropDown(guild.id))

        self.back.label = i18n.t(locale, 'settings.button.back')

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Enabled', style=nextcord.ButtonStyle.blurple)
    async def enabled(self,
                      button: nextcord.ui.Button,
                      interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        color = gdb.get('color')
        ideas: IdeasPayload = gdb.get('ideas')

        channel_suggest_id = ideas.get("channel_suggest_id")
        channel_offers_id = ideas.get("channel_offers_id")

        channel_suggest = interaction.guild.get_channel(channel_suggest_id)
        channel_offers = interaction.guild.get_channel(channel_offers_id)

        if not (channel_suggest and channel_offers):
            await interaction.response.send_message(
                'You haven\'t set up everything to include ideas\n'
                'Requirement value: **suggest** and **offers** channel',
                ephemeral=True
            )
            return

        embed = nextcord.Embed(
            title="Ideas",
            description=(
                "Do you have a good idea?\n"
                "And you are sure that everyone will like it!\n"
                "Before you write it, make sure that there have "
                "been no such ideas yet!"
            ),
            color=color
        )
        view = IdeaView(interaction.guild_id)

        message_suggest = await channel_suggest.send(embed=embed, view=view)

        ideas['message_suggest_id'] = message_suggest.id
        ideas['enabled'] = True

        gdb.set('ideas', ideas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Disabled', style=nextcord.ButtonStyle.red)
    async def disabled(self,
                       button: nextcord.ui.Button,
                       interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = gdb.get('ideas')

        channel_suggest_id = ideas.get("channel_suggest_id")
        channel_suggest = interaction.guild.get_channel(channel_suggest_id)
        message_suggest_id = ideas.get("message_suggest_id")

        if channel_suggest and message_suggest_id:
            message_suggest = channel_suggest.get_partial_message(
                message_suggest_id)
            try:
                await message_suggest.delete()
            except nextcord.errors.HTTPException:
                pass

        ideas['enabled'] = False

        gdb.set('ideas', ideas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label="Allow image")
    async def allow_image(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = gdb.get('ideas')
        ideas['allow_image'] = not ideas.get('allow_image', True)
        gdb.set('ideas', ideas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label="Thread delete")
    async def thread_delete(self,
                            button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas: IdeasPayload = gdb.get('ideas')
        ideas['thread_delete'] = not ideas.get('thread_delete', False)
        gdb.set('ideas', ideas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
