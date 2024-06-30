
import asyncio
from typing import Optional
import nextcord
from bot.misc.lordbot import LordBot
from bot.misc.utils import is_custom_emoji, is_emoji
from nextcord.utils import MISSING


class RoleReactionItemModal(nextcord.ui.Modal):
    def __init__(self, guild: nextcord.Guild, future: asyncio.Future) -> None:
        self.future = future

        super().__init__("Emoji")

        self.emoji = nextcord.ui.TextInput(label="Emoji")
        self.add_item(self.emoji)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        value = self.emoji.value

        if not is_emoji(value):
            await interaction.response.send_message("You have entered an incorrect emoji", ephemeral=True)
            return

        self.future.set_result(value)


class ReactionUsingModal(nextcord.ui.View):
    def __init__(self, future: asyncio.Future) -> None:
        self.future = future
        super().__init__(timeout=30)

    @nextcord.ui.button(label="Use modal", style=nextcord.ButtonStyle.blurple)
    async def use_modal(self,
                        button: nextcord.ui.Button,
                        interaction: nextcord.Interaction
                        ):
        await interaction.response.send_modal(RoleReactionItemModal(interaction.guild, self.future))


async def fetch_reaction(
    interaction: nextcord.Interaction[LordBot],
    message: Optional[nextcord.Message] = None,
    content: Optional[str] = MISSING
) -> str:
    future = interaction._state.loop.create_future()
    view = ReactionUsingModal(future)

    if message is None:
        if content is MISSING:
            content = "Send a reaction"
        message = await interaction.response.send_message(content, view=view, ephemeral=True)

    def check(message: nextcord.Message):
        return message.author == interaction.user and message.channel == interaction.channel and is_emoji(message.content)

    try:
        listeners = interaction.client._listeners['message']
    except KeyError:
        listeners = []
        interaction.client._listeners['message'] = listeners
    finally:
        listeners.append((future, check))

    try:
        done = await asyncio.wait_for(future, timeout=30)
    except asyncio.TimeoutError:
        await message.edit("You didn't have time to specify the emoji, use the interaction for", view=None)
        return

    if isinstance(done, nextcord.Message):
        value = done.content
        await done.delete()
    else:
        value = done
    await message.delete()

    allowed_emoji = list(map(str, interaction._state.emojis))
    if is_custom_emoji(value) and value not in allowed_emoji:
        await message.edit("Unfortunately I can't use this emoji check that I am on the server where this emoji is located", view=None)
        return

    return value
