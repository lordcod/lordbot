import nextcord

from bot.resources.ether import Emoji
from bot.databases.varstructs import IdeasPayload
from bot.databases.db import MongoDB, GuildDateBases

import time

timeout = {}


class ConfirmModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Suggest an idea",
            timeout = 5 * 60,
        )

        self.reason = nextcord.ui.TextInput(
            label="Argument:",
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
            title='New idea!',
            color=nextcord.Color.green()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(
            name='Old idea!',
            value=idea_content
        )
        
        author = interaction.guild.get_member(idea_author_id)
        content = f'{author.mention} Your idea is approved!'
        
        views = Confirm()
        views.confirm.disabled = True
        views.cancel.disabled = True
        
        await interaction.message.edit(content=content, embed=embed, view=views)
        
        if channel_approved_id is None:
            return
        
        channel = interaction.guild.get_channel(channel_approved_id)
        
        embed_accept = nextcord.Embed(
            title="The idea is approved!",
            color=nextcord.Color.green()
        )
        embed_accept.add_field(
            name='The essence of the idea:',
            value=reason,
            inline=False
        )
        if reason:
            embed_accept.add_field(
                name='Confirmation argument:', 
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
    
    
    @nextcord.ui.button(label="Approve", style=nextcord.ButtonStyle.green,custom_id='ideas-confirm:confirm')
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data: IdeasPayload = gdb.get('ideas')
        moderation_role_ids = ideas_data.get('moderation-role-ids', [])
        enabled: bool = ideas_data.get('enabled', False)
        if enabled is False:
            await interaction.response.send_message('The idea module is disabled on this server', ephemeral=True)
            return
        
        role_ids = set(interaction.user._roles)
        moderation_roles = set(moderation_role_ids)
        if not role_ids&moderation_roles:
            await interaction.response.defer(ephemeral=True)
            return
        
        await interaction.response.send_modal(ConfirmModal())
    
    @nextcord.ui.button(label="Deny", style=nextcord.ButtonStyle.red,custom_id='ideas-confirm:cancel')
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data: IdeasPayload = gdb.get('ideas')
        moderation_role_ids = ideas_data.get('moderation-role-ids', [])
        enabled: bool = ideas_data.get('enabled', False)
        if enabled is False:
            await interaction.response.send_message('The idea module is disabled on this server', ephemeral=True)
            return
        
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
            title='Old idea!',
            color=nextcord.Color.red()
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name='Idea:',value=idea_content)
        embed.set_footer(text=f'Refused | {name}',icon_url=interaction.user.display_avatar)
        
        author = interaction.guild.get_member(idea_author_id)
        content = f'{author.mention} Your idea has been rejected!'
        
        self.confirm.disabled = True
        self.cancel.disabled = True
        
        await interaction.message.edit(content=content,embed=embed,view=self)


class IdeaModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Suggest an idea",
            timeout=5 * 60, 
        )
        
        self.idea = nextcord.ui.TextInput(
            label="Tell us about your idea",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Describe your idea in as much detail as possible with usage examples.",
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
            title='New idea!',
            description='Whether the idea is approved or not depends on you!',
            color=0xffba08
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar
        )
        embed.add_field(name='Idea:', value=idea)
        
        mes = await channel.send(content=interaction.user.mention,embed=embed,view=Confirm())
        await mes.add_reaction(Emoji.tickmark)
        await mes.add_reaction(Emoji.cross)
        await mes.create_thread(name=f"Discussion of the idea from{interaction.user.display_name}")
        
        
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
        label="Suggest an idea",
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
                    "You can only propose an idea once every 30 minutes\n"
                    f"The next opportunity to submit an idea will be through:<t:{user_timeout :.0f}:R>"
                ),
                ephemeral=True
            )
            return
        
        gdb = GuildDateBases(interaction.guild_id)
        ideas_data: IdeasPayload = gdb.get('ideas')
        enabled: bool = ideas_data.get('enabled', False)
        if enabled is False:
            await interaction.response.send_message('The idea module is disabled on this server', ephemeral=True)
            return
        
        await interaction.response.send_modal(modal=IdeaModal())
