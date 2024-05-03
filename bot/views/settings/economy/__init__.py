import nextcord

from bot.misc.time_transformer import display_time
from bot.resources.info import DEFAULT_ECONOMY_SETTINGS

from .emoji import EmojiView
from .bonuses import BonusView
from .shop import ShopView
from .._view import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.databases import GuildDateBases
from bot.views import settings_menu


class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label='Change the amount of bonuses',
                emoji=Emoji.bagmoney,
                value='bonus'
            ),
            nextcord.SelectOption(
                label='Change the emoji',
                emoji=Emoji.emoji,
                value='emoji'
            ),
            nextcord.SelectOption(
                label='Change the shop roles',
                emoji=Emoji.auto_role,
                value='shop'
            ),
        ]

        super().__init__(
            placeholder="Economy Settings:",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        distrubutes = {
            'bonus': BonusView,
            'emoji': EmojiView,
            'shop': ShopView
        }
        view = distrubutes[value](interaction.guild)
        await interaction.message.edit(embed=view.embed, view=view)


class Economy(DefaultSettingsView):
    def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        self.es: dict = self.gdb.get('economic_settings')
        operate: bool = self.es.get('operate')
        color: int = self.gdb.get('color')
        locale: str = self.gdb.get('language')

        self.embed = nextcord.Embed(
            title='The economic system',
            description=(
                "The economic system will allow your server to rise to a completely different level.\n"
                "Games, levels, promotions, contests and more.\n"
                "All this is in our economic system."
            ),
            color=color
        )
        self.embed.add_field(
            name="Inforamtion",
            value=(
                f"Econonmy emoji: {self.es.get('emoji')}\n"
                f"Daily reward: {self.es.get('daily')}\n"
                f"Weekly reward: {self.es.get('weekly')}\n"
                f"Monthly reward: {self.es.get('monthly')}\n"
                f"Minimum bid: {self.es.get('bet', DEFAULT_ECONOMY_SETTINGS['bet']).get('min')}\n"
                f"Maximum bid: {self.es.get('bet', DEFAULT_ECONOMY_SETTINGS['bet']).get('max')}\n"
                f"Minimum payment for work: {self.es.get('work', DEFAULT_ECONOMY_SETTINGS['work']).get('min')}\n"
                f"Maximum payment for work: {self.es.get('work', DEFAULT_ECONOMY_SETTINGS['work']).get('max')}\n"
                f"Cooldown for work: {display_time(self.es.get('work', DEFAULT_ECONOMY_SETTINGS['work']).get('cooldown'), locale)}\n"
            )
        )

        super().__init__()

        economy_dd = DropDown()
        self.add_item(economy_dd)

        if operate:
            self.economy_switcher.label = "Disable"
            self.economy_switcher.style = nextcord.ButtonStyle.red
            self.economy_switcher_value = False
        else:
            self.economy_switcher.label = "Enable"
            self.economy_switcher.style = nextcord.ButtonStyle.green
            self.economy_switcher_value = True

            economy_dd.disabled = True

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red, row=1)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Switch', style=nextcord.ButtonStyle.green, row=1)
    async def economy_switcher(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.es['operate'] = self.economy_switcher_value
        self.gdb.set('economic_settings', self.es)

        view = self.__class__(interaction.guild)

        await interaction.message.edit(embed=view.embed, view=view)
