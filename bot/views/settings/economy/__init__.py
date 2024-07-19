import nextcord

from bot.misc.time_transformer import display_time
from bot.misc.utils import AsyncSterilization, get_emoji_wrap

from bot.resources.info import DEFAULT_ECONOMY_SETTINGS
from bot.views.information_dd import get_info_dd
from bot.views.settings.economy.theft import TheftView

from .emoji import EmojiView
from .bonuses import BonusView
from .shop import ShopView
from .._view import DefaultSettingsView

from bot.resources.ether import Emoji
from bot.databases import GuildDateBases
from bot.views import settings_menu


@AsyncSterilization
class ChooseDropDown(nextcord.ui.StringSelect):
    async def __init__(self, guild_id: int):
        gdb = GuildDateBases(guild_id)
        locale = await gdb.get('language')
        get_emoji = await get_emoji_wrap(guild_id)

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
            nextcord.SelectOption(
                label='Change the settings theft',
                emoji=Emoji.theft,
                value='theft'
            ),
        ]

        super().__init__(
            placeholder="Economy Settings:",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.values[0]
        distrubutes = {
            'bonus': BonusView,
            'emoji': EmojiView,
            'shop': ShopView,
            'theft': TheftView
        }
        view = await distrubutes[value](interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)


@AsyncSterilization
class Economy(DefaultSettingsView):
    async def __init__(self, guild: nextcord.Guild) -> None:
        self.gdb = GuildDateBases(guild.id)
        color: int = await self.gdb.get('color')
        locale: str = await self.gdb.get('language')
        self.es: dict = await self.gdb.get('economic_settings')
        operate: bool = self.es.get('operate')

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
            name="Economy Information",
            value=(
                f"・Daily reward: {self.es.get('daily')}\n"
                f"・Weekly reward: {self.es.get('weekly')}\n"
                f"・Monthly reward: {self.es.get('monthly')}\n"
                f"・Minimum bid: {self.es.get('bet', DEFAULT_ECONOMY_SETTINGS['bet']).get('min')}\n"
                f"・Maximum bid: {self.es.get('bet', DEFAULT_ECONOMY_SETTINGS['bet']).get('max')}\n"
                f"・Minimum payment for work: {self.es.get('work', DEFAULT_ECONOMY_SETTINGS['work']).get('min')}\n"
                f"・Maximum payment for work: {self.es.get('work', DEFAULT_ECONOMY_SETTINGS['work']).get('max')}\n"
                f"・Cooldown for work: {display_time(self.es.get('work', DEFAULT_ECONOMY_SETTINGS['work']).get('cooldown'), locale)}"
            )
        )

        super().__init__()

        self.add_item(get_info_dd(
            label='Economy emoji',
            emoji=self.es.get('emoji')
        ))
        economy_dd = await ChooseDropDown(guild.id)
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

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        view = await settings_menu.SettingsView(interaction.user)

        await interaction.response.edit_message(embed=view.embed, view=view)

    @nextcord.ui.button(label='Switch', style=nextcord.ButtonStyle.green)
    async def economy_switcher(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.gdb.set_on_json('economic_settings', 'operate',
                                   self.economy_switcher_value)

        view = await Economy(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
