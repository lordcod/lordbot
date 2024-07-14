from enum import StrEnum


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

    # Settings
    economy = '<:economy:1178742518553256026>'
    languages = '<:languages:1178742515420106906>'
    prefix = '<:prefix:1178742513083875368>'
    color = '<:color:1178742511649431573>'
    greeting = '<:greeting:1180603831378255974>'
    reactions = '<:reactions:1178742501109145740>'
    translate = '<:translate:1178742517190107287>'
    thread_message = '<:threadmessage:1178742507983601724>'
    command = '<:command:1178742498160545965>'

    # Greeting
    frame_person = '<:frame_person:1180609535107399770>'
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
    undo = '<:undo:1260237132321263656>'
    redo = '<:redo:1260237228945178664> '
    previous = '<:previous:1260237142618275840>'
    next = '<:next:1260237144157454447>'
    pause = '<:pause:1260237230262194267>'
    resume = '<:play:1260237150650372136>'
    volume_down = '<:volume2:1260237138289492008>'
    volume_up_2 = '<:volume3:1260237136838262854>'
    playlist_2 = '<:playlist:1260237135357808715>'
    stop = '<:stop:1260237147873742930>'
    repeat = '<:repeat:1260237133831213108>'

    volume_0 = '<:volume0:1260237141271908442>'
    volume_1 = '<:volume1:1260237139342393345>'
    volume_2 = volume_down
    volume_3 = volume_up_2

    # Ofher
    cooldown = '<:cooldown:1185277451295793192>'
    lightbulb = '<:lightbulb:1191467123462119554>'
    congratulation = '<a:congratulation:1165684808844845176>'
    rocket = '<a:rocketa:1165684783754522704>'

    tickmark = '<a:tickmark:1165684814557495326>'
    success = '<a:success:1165684794361917611>'
    check = '<a:check:1248999718823137422>'
    loading = '<a:loading:1249000397142626396>'
    cross = '<a:crossed:1248999695867707402>'
    warn = '<a:warning:1248999707963822150>'

    empty_card = '<:empty_card:1239171805885894717>'
    tic_tac_x = '<:tic_tac_x:1249468200626819133>'
    tic_tac_o = '<:tic_tac_o:1249468198869405726>'

    # Tickets
    tickets = '<:tickettool:1260646170590445598>'
    faq = '<:faq:1260652584507801640>'


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
