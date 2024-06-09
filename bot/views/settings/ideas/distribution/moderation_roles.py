import nextcord

from bot.misc.utils import to_async

from ... import ideas
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload


@to_async
class RolesDropDown(nextcord.ui.RoleSelect):
    async def __init__(
        self,
        guild: nextcord.Guild
    ) -> None:
        self.gdb = GuildDateBases(guild.id)
        super().__init__(
            min_values=1,
            max_values=15
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        for role in self.values.roles:
            if role.is_integration() or role.is_bot_managed():
                await interaction.response.send_message(
                    content=f"The {role.mention} role cannot be assigned and is used for integration or by a bot.",
                    ephemeral=True
                )
                break
        else:
            await self.gdb.set_on_json('ideas', 'moderation_role_ids', self.values.ids)

            view = await ModerationRolesView(interaction.guild)
            await interaction.response.edit_message(embed=view.embed, view=view)


@to_async
class ModerationRolesView(DefaultSettingsView):
    embed: nextcord.Embed = None

    async def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload = await self.gdb.get('ideas')
        mod_role_ids = self.idea_datas.get('moderation_role_ids')

        super().__init__()

        if mod_role_ids:
            self.delete.disabled = False

        cdd = await RolesDropDown(guild)
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await ideas.IdeasView(interaction.guild)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.gdb.set_on_json('ideas', 'moderation_role_ids', [])

        view = await ModerationRolesView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
