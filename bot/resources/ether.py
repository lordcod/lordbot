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

    # Greeting
    auto_role = '<:auto_role:1180609685112492172>'

    # Economy
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


every_emojis: Dict[str, Dict[int, str]] = {}

temp_voice_emojis = {
    "hide": {
        0: "<:aquahide:1262359492348088363>",
        1: "<:malahide:1262359494709477407>",
        2: "<:barhhide:1262359498589470771>",
        3: "<:lavahide:1262359606810902558>",
        4: "<:perlhide:1262367083875008575>",
        5: "<:yanthide:1262367085833486468>",
        6: "<:sumehide:1262367087146303600>",
        7: "<:slivhide:1262367088488747041>"
    },
    "kick": {
        3: "<:lavakick:1262365111394242631>",
        0: "<:aquakick:1262365112895803442>",
        1: "<:malakick:1262365114154094623>",
        2: "<:barhkick:1262365115273969758>",
        4: "<:perlkick:1262367114145300520>",
        5: "<:yantkick:1262367115718164570>",
        6: "<:sumekick:1262367117009748041>",
        7: "<:slivkick:1262367118629011457>",
    },
    "assets": {
        2: "<:barhassets:1262365168990552064>",
        3: "<:lavaassets:1262365170475204608>",
        0: "<:aquaassets:1262365171888816199>",
        1: "<:malaassets:1262365173524725791>",
        5: "<:yantassets:1262367160278454342>",
        6: "<:sumeassets:1262367162853621772>",
        7: "<:slivassets:1262367164338536545>",
        4: "<:perlassets:1262367165982441513>"
    },
    "mic": {
        2: "<:barhmic:1262365193846132756>",
        3: "<:lavamic:1262365195322527805>",
        0: "<:aquamic:1262365196635209850>",
        1: "<:malamic:1262365210149388351>",
        5: "<:yantmic:1262367186568220702>",
        6: "<:sumemic:1262367187843416085>",
        7: "<:slivmic:1262367189688913920>",
        4: "<:perlmic:1262367190984818749>"
    },
    "micoff": {
        2: "<:barhmicoff:1262365211877445662>",
        3: "<:lavamicoff:1262365213420687380>",
        0: "<:aquamicoff:1262365214792482898>",
        5: "<:yantmicoff:1262367211029266493>",
        6: "<:sumemicoff:1262367212346409072>",
        7: "<:slivmicoff:1262367213168623687>",
        4: "<:perlmicoff:1262367214959460424>"
    },
    "open": {
        2: "<:barhopen:1262365230277857321>",
        3: "<:lavaopen:1262365231275970571>",
        0: "<:aquaopen:1262365233054486632>",
        1: "<:malaopen:1262365235201708094>",
        5: "<:yantopen:1262367232227545251>",
        6: "<:sumeopen:1262367233557135420>",
        7: "<:slivopen:1262367234743996488>",
        4: "<:perlopen:1262367236706930739>"
    },
    "name": {
        2: "<:barhname:1262365253715492966>",
        3: "<:lavaname:1262365255145754624>",
        0: "<:aquaname:1262365256894906378>",
        1: "<:malaname:1262365258274832434>",
        5: "<:yantname:1262367258320179261>",
        6: "<:sumename:1262367260019003513>",
        7: "<:slivname:1262367261558177833>",
        4: "<:perlname:1262367262975856662>"
    },
    "limit": {
        2: "<:barhlimit:1262365279946801222>",
        3: "<:lavalimit:1262365281431588965>",
        0: "<:aqualimit:1262365282501136456>",
        1: "<:malalimit:1262365284359209012>",
        7: "<:slivlimit:1262367293586018337>",
        4: "<:perllimit:1262367295263735902>",
        5: "<:yantlimit:1262367297129938954>",
        6: "<:sumelimit:1262367298560327690>"
    },
    "owner": {
        1: "<:malaowner:1262365302331670650>",
        2: "<:barhowner:1262365303741091962>",
        3: "<:lavaowner:1262365304671965226>",
        0: "<:aquaowner:1262365306576306239>",
        5: "<:yantowner:1262367323554316348>",
        6: "<:sumeowner:1262367325181710398>",
        7: "<:slivowner:1262367327002038324>",
        4: "<:perlowner:1262367328331370587>"
    },
    "show": {
        1: "<:malashow:1262365326327414875>",
        2: "<:barhshow:1262365328181170216>",
        3: "<:lavashow:1262365329800036404>",
        0: "<:aquashow:1262365331289149471>",
        5: "<:yantshow:1262367346992087203>",
        6: "<:sumeshow:1262367348401246208>",
        7: "<:slivshow:1262367349697413242>",
        4: "<:perlshow:1262367351081402432>"
    },
    "lock": {
        5: "<:yantlock:1262367133015347231>",
        6: "<:sumelock:1262367134118445147>",
        7: "<:slivlock:1262367136202887199>",
        4: "<:perllock:1262367138044448838>",
        3: "<:lavalock:1262365150032429077>",
        0: "<:aqualock:1262365151357829142>",
        1: "<:malalock:1262365152607604838>",
        2: "<:barhlock:1262365154457161780>"
    },
    'bitrate': {
        0: '<:aquabitrate:1262477619362791594>',
        1: '<:malabitrate:1262477617563435223>',
        2: '<:barhbitrate:1262477614015053975>',
        3: '<:lavabitrate:1262477615780987014>',
        4: '<:perlbitrate:1262477624861528074>',
        5: '<:yantbitrate:1262477612702367807>',
        6: '<:sumebitrate:1262477621070008361>',
        7: '<:slivbitrate:1262477622731083950>'
    },
    'invite': {
        0: '<:aquainvite:1262477798518558802>',
        1: '<:malainvite:1262477797314527304>',
        2: '<:barhinvite:1262477794496090133>',
        3: '<:lavainvite:1262477795804581950>',
        4: '<:perlinvite:1262477803182362646>',
        5: '<:yantinvite:1262477793074090087>',
        6: '<:sumeinvite:1262477800418578464>',
        7: '<:slivinvite:1262477801513025581>'
    },
    'permit': {
        1: '<:malapermit:1262477949303521371>',
        2: '<:barhpermit:1262477946392805426>',
        3: '<:lavapermit:1262477947894501436>',
        4: '<:perlpermit:1262477955544780821>',
        5: '<:yantpermit:1262477944937381968>',
        6: '<:sumepermit:1262477952130744330>',
        7: '<:slivpermit:1262477953913065472>'
    },
    'reject': {
        0: '<:aquareject:1262477976688398397>',
        1: '<:malareject:1262477974968471622>',
        2: '<:barhreject:1262477971801903156>',
        3: '<:lavareject:1262477973265711298>',
        4: '<:perlreject:1262477968475684876>',
        5: '<:yantreject:1262477970048684033>',
        6: '<:sumereject:1262477978214989916>',
        7: '<:slivreject:1262478173619097601>'
    }
}

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
