from enum import IntEnum, StrEnum
from typing import Dict

import orjson


class ColorType(IntEnum):
    aqua = 0
    mala = 1
    barh = 2
    lava = 3
    perl = 4
    yant = 5
    sume = 6
    sliv = 7

    @classmethod
    def get(cls, name: str) -> 'ColorType':
        return getattr(cls, name, None)


class Emoji(StrEnum):
    lordcord = '<:lordcord:1179130474006859776>'

    # Channels
    category = '<:category:1166001036553621534>'
    channel_text = '<:channel_text:1166001040198484178>'
    channel_voice = '<:channel_voice:1166001038772404284>'
    channel_forum = '<:channel_forum:1166094701020070009>'
    channel_stage = '<:channel_stage:1166092341317226566>'
    channel_announce = '<:channel_announce:1166092338242785370>'
    thread = '<:thread:1166096258511937666>'

    # Economy
    diamod = '<:diamond:1183363436780978186>'
    bagmoney = '<:bagmoney:1178745646128300083>'
    bank = '<:bank:1178745652352663663> '
    money = '<:money:1178745649248882770>'
    award = '<:award:1178745644714831954>'

    # Economy Sets
    auto_role = '<:auto_role:1180609685112492172>'
    theft = '<:robbery:1262915680575946772>'
    emoji = '<:emoji:1183456189141504091>'

    # Disabled command
    enabled = '<:enabled:1178742503822852248>'
    disabled = '<:disabled:1178742506544955522>'

    # Music settings
    music = '<:music:1207674677816991784>'
    playlist = '<:playlist:1207675618322550804>'
    volume_up = '<:volume_up:1207676856300478525>'

    # Music
    yandex_music = '<:yandex_music:1259622734132936784>'

    # Ofher
    cooldown = '<:cooldown:1185277451295793192>'
    congratulation = '<a:congratulation:1165684808844845176>'
    rocket = '<a:rocketa:1165684783754522704>'

    tickmark = '<a:tickmark:1165684814557495326>'
    success = '<a:success:1165684794361917611>'
    loading = '<a:loading:1249000397142626396>'
    cross = '<a:crossed:1248999695867707402>'
    warn = '<a:warning:1248999707963822150>'

    empty_card = '<:empty_card:1239171805885894717>'
    tic_tac_x = '<:tic_tac_x:1249468200626819133>'
    tic_tac_o = '<:tic_tac_o:1249468198869405726>'

    # Tickets
    tickets = '<:tickettool:1260646170590445598>'
    faq = '<:faq:1260652584507801640>'

    online = '<:online:1264700950585675776>'
    offline = '<:offline:1264700948702298192>'

    envelope_complete = '<:envelope_complete:1265711863040053280>'
    envelope_create = '<:envelope_create:1265711868165623922>'
    envelope_panel = '<:envelope_panel:1265711869977690303>'
    envelope = '<:envelope_default:1265711865187794996>'
    garbage = '<:garbage:1265711866668122212>'


every_emojis = {}

channel_types_emoji = {
    0: Emoji.channel_text,
    1: Emoji.channel_text,
    2: Emoji.channel_voice,
    3: Emoji.category,
    4: Emoji.category,
    5: Emoji.channel_announce,
    10: Emoji.thread,
    11: Emoji.thread,
    12: Emoji.thread,
    13: Emoji.channel_stage,
    14: Emoji.category,
    15: Emoji.channel_forum,
    16: Emoji.channel_forum
}


if __name__ == '__main__':
    from pprint import pprint
    rs = {}
    for name, item in ColorType.__dict__.items():
        if isinstance(item, ColorType):
            rs[name] = item.value
    new_data = {}
    data = {
        "bitrate": {
            "yant": "<:yantbitrate:1262477612702367807>",
            "barh": "<:barhbitrate:1262477614015053975>",
            "lava": "<:lavabitrate:1262477615780987014>",
            "mala": "<:malabitrate:1262477617563435223>",
            "aqua": "<:aquabitrate:1262477619362791594>",
            "sume": "<:sumebitrate:1262477621070008361>",
            "sliv": "<:slivbitrate:1262477622731083950>",
            "perl": "<:perlbitrate:1262477624861528074>"
        },
        "invite": {
            "yant": "<:yantinvite:1262477793074090087>",
            "barh": "<:barhinvite:1262477794496090133>",
            "lava": "<:lavainvite:1262477795804581950>",
            "mala": "<:malainvite:1262477797314527304>",
            "aqua": "<:aquainvite:1262477798518558802>",
            "sume": "<:sumeinvite:1262477800418578464>",
            "sliv": "<:slivinvite:1262477801513025581>",
            "perl": "<:perlinvite:1262477803182362646>"
        },
        "permit": {
            "yant": "<:yantpermit:1262477944937381968>",
            "barh": "<:barhpermit:1262477946392805426>",
            "lava": "<:lavapermit:1262477947894501436>",
            "mala": "<:malapermit:1262477949303521371>",
            "sume": "<:sumepermit:1262477952130744330>",
            "sliv": "<:slivpermit:1262477953913065472>",
            "perl": "<:perlpermit:1262477955544780821>"
        },
        "reject": {
            "perl": "<:perlreject:1262477968475684876>",
            "yant": "<:yantreject:1262477970048684033>",
            "barh": "<:barhreject:1262477971801903156>",
            "lava": "<:lavareject:1262477973265711298>",
            "mala": "<:malareject:1262477974968471622>",
            "aqua": "<:aquareject:1262477976688398397>",
            "sume": "<:sumereject:1262477978214989916>",
            "sliv": "<:slivreject:1262478173619097601>"
        }
    }

    for name, vals in data.items():
        new_data[name] = {}
        for color, emo in vals.items():
            new_data[name][rs[color]] = emo

    pprint(new_data)
