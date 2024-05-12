

from dataclasses import dataclass
from typing import List, Optional

from discord import Interaction
from httpx import delete
from bot.databases.varstructs import LogsPayload
from bot.languages import i18n
from bot.databases import GuildDateBases
import nextcord
from bot.views import settings_menu
from ._view import DefaultSettingsView
from bot.misc.logstool import LogType


@dataclass
class LogItem:
    id: int
    name: str
    description: str
    emoji: Optional[str] = None


logs_items = [
    LogItem(LogType.delete_message, "Удаление сообщения",
            "Действия с удаленными сообщениями: Этот лог содержит информацию о всех удаленных сообщениях в системе. Он помогает отслеживать, кто и когда удалил сообщение, и обеспечивает прозрачность в отношении удаленных данных.",),
    LogItem(LogType.edit_message, "Редактирование сообщения",
            "Редактированные сообщения: Этот лог содержит информацию о всех сообщениях, которые были изменены после отправки. Он предоставляет возможность просмотра истории изменений сообщений, что полезно для контроля целостности коммуникации.",),
    LogItem(LogType.punishment, "Нарушение правил и наказание", "Примененные наказания за нарушения: Этот лог включает информацию о примененных наказаниях в ответ на нарушения правил. Он помогает поддерживать порядок и дисциплину в системе, обеспечивая справедливость и последовательность в применении мер дисциплинарного воздействия.",),
    LogItem(LogType.economy, "Транзакция или изменения в экономике",
            "Транзакции или изменения в экономике: Этот лог отражает все транзакции и изменения в экономике системы. Он предоставляет информацию о всех финансовых операциях, произошедших в системе, и помогает отслеживать денежные потоки и изменения в экономической ситуации.",),
    LogItem(LogType.ideas, "Предложение или идея", "Рассмотренные предложения и идеи: Этот лог содержит информацию о всех предложенных идеях и предложениях, которые были рассмотрены в системе. Он помогает отслеживать процесс развития идей и принятия решений на основе предложений от участников.")
]


class ChannelDropDown(nextcord.ui.ChannelSelect):
    def __init__(self, guild_id: int):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        super().__init__(
            channel_types=[nextcord.ChannelType.news,
                           nextcord.ChannelType.text]
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        view = LogsView(interaction.guild,  self.values[0].id)
        await interaction.message.edit(embed=view.embed, view=view)


class LogsDropDown(nextcord.ui.StringSelect):
    def __init__(self, guild_id: int, selected_channel_id: Optional[int] = None,
                 selected_logs: Optional[List[int]] = None):
        gdb = GuildDateBases(guild_id)
        locale = gdb.get('language')
        logs_data: LogsPayload = gdb.get('logs')
        channel_data = logs_data.get(selected_channel_id, [])
        self.selected_channel_id = selected_channel_id

        if selected_logs:
            channel_data = selected_logs

        options = [
            nextcord.SelectOption(
                label=log.name,
                value=log.id,
                emoji=log.emoji,
                default=log.id in channel_data
            )
            for log in logs_items
        ]

        super().__init__(
            min_values=1,
            max_values=len(options),
            options=options,
            disabled=not bool(selected_channel_id)
        )

    async def callback(self, interaction: nextcord.Interaction) -> None:
        values = list(map(int, self.values))

        view = LogsView(interaction.guild,  self.selected_channel_id, values)
        await interaction.message.edit(embed=view.embed, view=view)


class LogsView(DefaultSettingsView):
    embed: nextcord.Embed

    def __init__(
        self,
        guild: nextcord.Guild,
        selected_channel_id: Optional[int] = None,
        selected_logs: Optional[List[int]] = None
    ) -> None:
        self.selected_channel_id = selected_channel_id
        self.selected_logs = selected_logs
        gdb = GuildDateBases(guild.id)
        logs_data: LogsPayload = gdb.get('logs')
        color = gdb.get('color')
        locale = gdb.get('language')

        self.embed = None

        super().__init__()

        if selected_logs:
            self.edit.disabled = False
        if selected_channel_id in logs_data:
            self.delete.disabled = False

        self.back.label = i18n.t(locale, 'settings.button.back')

        self.add_item(ChannelDropDown(guild.id))
        self.add_item(LogsDropDown(
            guild.id, selected_channel_id, selected_logs))

    @nextcord.ui.button(label='Back', style=nextcord.ButtonStyle.red)
    async def back(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        view = settings_menu.SettingsView(interaction.user)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Edit', style=nextcord.ButtonStyle.blurple, disabled=True)
    async def edit(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        logs_data: LogsPayload = gdb.get('logs')
        logs_data[self.selected_channel_id] = self.selected_logs
        gdb.set('logs', logs_data)

        view = self.__class__(interaction.guild, self.selected_channel_id)

        await interaction.message.edit(embed=view.embed, view=view)

    @nextcord.ui.button(label='Delete', style=nextcord.ButtonStyle.red, disabled=True)
    async def delete(self,
                     button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        gdb = GuildDateBases(interaction.guild_id)
        logs_data: LogsPayload = gdb.get('logs')
        logs_data.pop(self.selected_channel_id, None)
        gdb.set('logs', logs_data)

        view = self.__class__(interaction.guild, self.selected_channel_id)

        await interaction.message.edit(embed=view.embed, view=view)
