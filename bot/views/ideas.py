import nextcord

from bot.resources.ether import Emoji
from bot.databases.db import MongoDB, GuildDateBases

import time

timeout = {}


class ConfirmModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Предложить идею",
            timeout = 5 * 60,  # 5 minutes
        )

        self.reason = nextcord.ui.TextInput(
            label="Аргумент:",
            required=False,
            style=nextcord.TextInputStyle.paragraph,
            min_length=0,
            max_length=1500,
        )
        self.add_item(self.reason)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data = gdb.get('ideas')
        channel_approved_id = ideas_data.get('channel-approved-id')
        
        mdb = MongoDB('ideas')
        idea_data = mdb.get(interaction.message.id)
        if idea_data is None:
            await interaction.response.defer(ephemeral=True)
            return
        
        
        idea_content = idea_data.get('idea')
        idea_author_id = idea_data.get('user_id')
        
        reason = self.reason.value
        
        embed = nextcord.Embed(
            title='Новая идея!',
            color=nextcord.Color.green()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(
            name='Прежняя идея!',
            value=idea_content
        )
        
        author = interaction.guild.get_member(idea_author_id)
        content = f'{author.mention} твоя идея одобрена!'
        
        views = Confirm()
        views.confirm.disabled = True
        views.cancel.disabled = True
        
        await interaction.message.edit(content=content,embed=embed,view=views)
        
        
        channel = interaction.guild.get_channel(channel_approved_id)
        
        embed_accept = nextcord.Embed(
            title="Идея одобрена!",
            color=nextcord.Color.green()
        )
        embed_accept.add_field(
            name='Суть идеи:',
            value=reason,
            inline=False
        )
        if reason:
            embed_accept.add_field(
                name='Аргумент подтверждения:', 
                value=reason, 
                inline=False
            )
        embed_accept.set_footer(
            text=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        await channel.send(content=content,embed=embed_accept)

class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(label="Одобрить", style=nextcord.ButtonStyle.green,custom_id='ideas-confirm:confirm')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data = gdb.get('ideas')
        moderation_role_ids = ideas_data.get('moderation-role-ids')
        
        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)
        if not role_ids&moderation_roles:
            await interaction.response.defer(ephemeral=True)
            return
        
        await interaction.response.send_modal(ConfirmModal())
    
    @nextcord.ui.button(label="Отказать", style=nextcord.ButtonStyle.red,custom_id='ideas-confirm:cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data = gdb.get('ideas')
        moderation_role_ids = ideas_data.get('moderation-role-ids')
        
        mdb = MongoDB('ideas')
        idea_data = mdb.get(interaction.message.id)
        if idea_data is None:
            await interaction.response.defer(ephemeral=True)
        
        idea_content = idea_data.get('idea')
        idea_author_id = idea_data.get('user_id')
        
        
        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)
        if not interaction.user.id == idea_author_id and not role_ids&moderation_roles:
            await interaction.response.defer(ephemeral=True)
            return
        
        
        name = interaction.user.display_name
        embed = nextcord.Embed(
            title='Прежняя идея!',
            color=nextcord.Color.red()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name='Идея:',value=idea_content)
        embed.set_footer(text=f'Отказано | {name}',icon_url=interaction.user.display_avatar)
        
        author = interaction.guild.get_member(idea_author_id)
        content = f'{author.mention} твоей идеи отказано!'
        
        self.confirm.disabled = True
        self.cancel.disabled = True
        
        await interaction.message.edit(content=content,embed=embed,view=self)


class IdeaModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Предложить идею",
            timeout=5 * 60, 
        )
        
        self.idea = nextcord.ui.TextInput(
            label="Расскажи нам о своей идее",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Опиши свою идею как можно более подробно с примерами использования.",
            min_length=10,
            max_length=1500,
        )
        self.add_item(self.idea)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data = gdb.get('ideas')
        channel_offers_id = ideas_data.get('channel-offers-id')
        
        channel = interaction.guild.get_channel(channel_offers_id)
        idea = self.idea.value
        
        
        embed = nextcord.Embed(
            title='Новая идея!',
            description='Одобрят идею или нет, зависит от вас!',
            color=0xffba08
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name='Идея:', value=idea)
        
        mes = await channel.send(content=interaction.user.mention,embed=embed,view=Confirm())
        await mes.add_reaction(Emoji.tickmark)
        await mes.add_reaction(Emoji.cross)
        await mes.create_thread(name=f"Обсуждение идеи от {interaction.user.display_name}")
        
        
        idea_data = {
            'user_id': interaction.user.id,
            'idea':idea
        }
        mdb = MongoDB('ideas')
        mdb.set(mes.id, idea_data)
        
        timeout[interaction.user.id] = time.time()+(60*30)

class IdeaBut(nextcord.ui.View):
    def __init__(self, guild_id: int = None):
        super().__init__(timeout=None)
        if guild_id is None:
            return
    
    @nextcord.ui.button(
        label="Предложить идею",
        style=nextcord.ButtonStyle.green,
        custom_id="ideas-main-button:suggest"
    )
    async def suggest(
        self,
        button: nextcord.ui.Button,
        interaction: nextcord.Interaction
    ) -> None:
        user_timeout = timeout.get(interaction.user.id)
        if user_timeout and user_timeout > time.time():
            await interaction.response.send_message(
                content=(
                    "Предложить идею можно только раз в 30 минут\n"
                    f"Следующия возможность подать идею будет через: <t:{user_timeout :.0f}:R>"
                ),
                ephemeral=True
            )
            return
        await interaction.response.send_modal(modal=IdeaModal())
