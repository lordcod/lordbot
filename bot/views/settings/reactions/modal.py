import nextcord

from bot.misc.utils import is_emoji

from .. import reactions

from bot.databases import GuildDateBases
from bot.languages import i18n


class ModalBuilder(nextcord.ui.Modal):
    def __init__(self, guild_id, channel_id) -> None:
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')

        self.channel_id = channel_id
        super().__init__(i18n.t(
            locale, 'settings.reactions.modal.title'))

        self.emoji_1 = nextcord.ui.TextInput(
            label=i18n.t(
                locale, 'settings.reactions.modal.label'),
            placeholder='<a:name:id>',
            required=True
        )

        self.emoji_2 = nextcord.ui.TextInput(
            label=i18n.t(
                locale, 'settings.reactions.modal.label'),
            placeholder='<:name:id>',
            default_value=None,
            required=False
        )

        self.emoji_3 = nextcord.ui.TextInput(
            label=i18n.t(
                locale, 'settings.reactions.modal.label'),
            placeholder='😀',
            default_value=None,
            required=False
        )

        self.add_item(self.emoji_1)
        self.add_item(self.emoji_3)
        self.add_item(self.emoji_2)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        gdb = GuildDateBases(interaction.guild_id)
        reacts: dict = gdb.get('reactions')
        emojis = list(filter(
            lambda item: item,
            [self.emoji_1.value, self.emoji_2.value, self.emoji_3.value]
        ))

        for num, emo in enumerate(emojis, start=1):
            if not is_emoji(emo):
                await interaction.response.send_message(
                    f"You have entered an incorrect emoji into the form number {num}", ephemeral=True)
                return

        channel_id = self.channel_id
        reacts[channel_id] = emojis

        gdb.set('reactions', reacts)

        view = reactions.AutoReactions(interaction.guild)
        await interaction.response.edit_message(embed=view.embed, view=view)
