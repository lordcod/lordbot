import nextcord

from ... import ideas
from bot.views.settings._view import DefaultSettingsView

from bot.databases import GuildDateBases
from bot.databases.varstructs import IdeasPayload


class RolesDropDown(nextcord.ui.RoleSelect):
    def __init__(
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
            await interaction.response.defer()
            idea_datas = self.gdb.get('ideas')
            idea_datas['moderation_role_ids'] = self.values.ids

            self.gdb.set('ideas', idea_datas)

        view = ModerationRolesView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)


class ModerationRolesView(DefaultSettingsView):
    embed: nextcord.Embed = None

    def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.idea_datas: IdeasPayload | None = self.gdb.get('ideas')
        mod_role_ids = self.idea_datas.get('moderation_role_ids')

        super().__init__()

        if mod_role_ids:
            self.delete.disabled = False

        cdd = RolesDropDown(guild)
        self.add_item(cdd)

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = ideas.IdeasView(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.idea_datas['moderation_role_ids'] = []

        self.gdb.set('ideas', self.idea_datas)

        view = self.__class__(interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)
