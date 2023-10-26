import nextcord
from datetime import datetime
from nextcord.utils import format_dt
from formatting import nftd

exemple = {
    'ru':'',
    'en':''
}

class Emoji():
    congratulation = '<a:congratulation:1165684808844845176>'
    owner = '<:owner:1166002519315599500>'
    verified = '<:verified:1166001046468964406>'
    create = '<:paint:1166001043562307674>'
    channel_text = '<:channel_text:1166001040198484178>'
    channel_voice = '<:channel_voice:1166001038772404284>'
    channel_forum = '<:channel_forum:1166094701020070009>'
    channel_stage = '<:channel_stage:1166092341317226566>'
    category = '<:category:1166001036553621534>'
    text1 = '<:text1:1166001701912846346>'
    text2 = '<:text2:1166001699295592528>'
    member = '<:member:1166001035182080161>'
    channel_announce = '<:channel_announce:1166092338242785370>'
    thread = '<:thread:1166096258511937666>'
    
    



class invites():
    def __init__(self,invite):
        self.invite = invite
    
    verification_level = {
        'ru':[
            "нет",
            "низкий",
            "средний",
            "высокий",
            "высочайший"
        ],
        'en':[
            'none',
            'low',
            'medium',
            'high',
            'highest'
        ]
    }
    
    channel_type = {
        0:Emoji.channel_text,
        1:Emoji.channel_text,
        2:Emoji.channel_voice,
        3:Emoji.category,
        4:Emoji.category,
        5:Emoji.channel_announce,
        10:Emoji.thread,
        11:Emoji.thread,
        12:Emoji.thread,
        13:Emoji.channel_stage,
        14:Emoji.category,
        15:Emoji.channel_forum,
        16:Emoji.channel_forum,
    }
    
    @property
    def description(self):
        invite = self.invite 
        return f"### **{self.channel_type[invite.channel.type.value]}{nftd(invite.channel.name)}**"
    
    @property
    def is_guild(self):
        return hasattr(self.invite.guild,'owner') 
    
    @property
    def field_guild(self):
        invite = self.invite 
        guild = invite.guild
        return {
            'ru':(
                f'{Emoji.owner} Владелец: {guild.owner.mention}\n'
                f'{Emoji.verified} Уровень проверки: {self.verification_level["ru"][guild.verification_level.value]}\n'
                f'{Emoji.create} Создан: {format_dt(guild.created_at,"f")} ({format_dt(guild.created_at,"R")})\n'
                f'{Emoji.channel_text} Всего {len(guild.channels)} каналов\n'
                f'{Emoji.text1}{Emoji.channel_text} Текстовые каналы: {len(guild.text_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_voice}  Голосовые каналы: {len(guild.voice_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_forum}  Форум: {len(guild.forum_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_stage}  Трибуны: {len(guild.stage_channels)}\n'
                f'{Emoji.text2}{Emoji.category}  Категории: {len(guild.categories)}\n'
                f'{Emoji.member} Всего {guild.member_count} пользователя\n'
                f'{Emoji.text1} Ботов: {len(guild.bots)}\n'
                f'{Emoji.text2} Участников: {len(guild.humans)}'
            ),
            'en':(
                f'{Emoji.owner} Owner: {guild.owner.mention}\n'
                f'{Emoji.verified} Verification level: {self.verification_level["en"][guild.verification_level.value]}\n'
                f'{Emoji.create} Generated: {format_dt(guild.created_at,"f")} ({format_dt(guild.created_at,"R")})\n'
                f'{Emoji.channel_text} Total {len(guild.channels)} channels\n'
                f'{Emoji.text1}{Emoji.channel_text} Text channels: {len(guild.text_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_voice}  Voice channels: {len(guild.voice_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_forum}  Forums: {len(guild.forum_channels)}\n'
                f'{Emoji.text1}{Emoji.channel_stage}  Stands: {len(guild.stage_channels)}\n'
                f'{Emoji.text2}{Emoji.category} Categories: {len(guild.categories)}\n'
                f'{Emoji.member} Total {guild.member_count} user\n'
                f'{Emoji.text1} Bots: {len(guild.bots)}\n'
                f'{Emoji.text2} Participants: {len(guild.humans)}'
            )
        }

class captcha():
    congratulation = {
        'ru':'Поздравляю, вы ввели капчу!',
        'en':'Congratulations you have passed the captcha!'
    }
    enter = {
        'ru':'У вас есть 30 секунд чтобы решить капчу!',
        'en':'You have 30 seconds to solve the captcha!'
    }
    failed = {
        'ru':'Капча не пройдена',
        'en':'Captcha failed'
    }

class activiti():
    failed = {
        'ru':'Это действие недоступно или не работает',
        'en':'This activity is unavailable or does not work'
    }
    embed_title = {
        'ru':'Активность успешно создана!',
        'en':'The activity has been successfully created!'
    }
    embed_description = {
        'ru':'Однако некоторые виды активностей могут быть недоступны для вашего сервера, если уровень бустов не соответствует требованиям активности.',
        'en':'However, some types of activities may not be available for your server if the boost level does not meet the activity requirements.'
    }
    fields_label = {
        'ru':'Название активности',
        'en':'Activity name'
    }
    fields_max_user = {
        'ru':'Максимальное кол-во пользователей',
        'en':'Maximum number of users'
    }

class auto_translate():
    title = {
        'ru':'Авто перевод',
        'en':'Automatic translation'
    }
    field_name_from = {
        'ru':'Переведено c',
        'en':'Translated from'
    }
    field_name_to = {
        'ru':'Переведено на',
        'en':'Translated to'
    }