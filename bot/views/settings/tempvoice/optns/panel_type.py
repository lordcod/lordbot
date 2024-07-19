import nextcord

from bot.databases.handlers.guildHD import GuildDateBases
from bot.misc.utils import AsyncSterilization, get_emoji_wrap
from bot.views.settings.tempvoice.optns.standart import ViewOptionItem


@AsyncSterilization
class TypePanelDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, type_panel: int) -> None:
        options = [
            nextcord.SelectOption(
                label='None',
                description='Disables the panel',
                value=0,
                default=type_panel == 0
            ),
            nextcord.SelectOption(
                label='Button',
                description='The panel will have buttons',
                value=1,
                default=type_panel == 1
            ),
            nextcord.SelectOption(
                label='DropDown',
                description='The panel will have a dropdown menu',
                value=2,
                default=type_panel == 2
            ),
        ]
        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = int(self.values[0])
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('tempvoice', 'type_panel', value)

        await self.view.edit_panel(interaction)
        await self.view.update(interaction)


@AsyncSterilization
class TypeMessagePanelDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int, type_message_panel: int) -> None:
        options = [
            nextcord.SelectOption(
                label='Control panel',
                description='Before that, select the channel panel',
                value=1,
                default=type_message_panel == 1
            ),
            nextcord.SelectOption(
                label='In voice',
                description='Sends a panel to the voice when it is created',
                value=2,
                default=type_message_panel == 2
            ),
            nextcord.SelectOption(
                label='Everywhere',
                description='Creates a panel in the voice and in the channel allocated for this purpose',
                value=3,
                default=type_message_panel == 3
            ),
        ]
        super().__init__(options=options)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = int(self.values[0])
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('tempvoice', 'type_message_panel', value)

        await self.view.edit_panel(interaction)
        await self.view.update(interaction)


@AsyncSterilization
class TypePanelView(ViewOptionItem):
    label = 'Panel Type'
    description = 'Open Panel Type Settings'

    async def __init__(self, guild: nextcord.Guild):
        gdb = GuildDateBases(guild.id)
        data = await gdb.get('tempvoice')
        type_panel = data.get('type_panel', 1)
        type_message_panel = data.get('type_message_panel', 1)

        get_emoji = await get_emoji_wrap(gdb)

        enabled_panel = True
        if type_panel == 0:
            enabled_panel = False
            default_advance_panel = False
        if type_panel == 1:
            default_advance_panel = False
        elif type_panel == 2:
            default_advance_panel = True

        self.advance_panel = data.get('advance_panel', default_advance_panel)

        super().__init__()

        tpdd = await TypePanelDropDown(guild.id, type_panel)
        tmpdd = await TypeMessagePanelDropDown(guild.id, type_message_panel)
        self.add_item(tpdd)
        self.add_item(tmpdd)

        if not enabled_panel:
            tmpdd.disabled = True
            self.edit.disabled = True

        if self.advance_panel:
            self.edit.emoji = get_emoji('simple')
            self.edit.label = 'Enable simple panel'
            self.edit.style = nextcord.ButtonStyle.blurple
        else:
            self.edit.emoji = get_emoji('advanced')
            self.edit.label = 'Enable extended panel'
            self.edit.style = nextcord.ButtonStyle.blurple

    @nextcord.ui.button()
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        await gdb.set_on_json('tempvoice', 'advance_panel', not self.advance_panel)

        await self.edit_panel(interaction)

        view = await TypePanelView(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
