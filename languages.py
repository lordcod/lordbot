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
    
    



class invites():
    def __init__(self,invite):
        self.invite = invite
    
    @property
    def description(self):
        invite = self.invite 
        return {
        'ru' : f"### **{self.channel_type[invite.channel.type.value]}{nftd(invite.channel.name)}**"
        }
    
    @property
    def is_guild(self):
        return hasattr(self.invite.guild,'owner') 
    
    @property
    def field_guild(self):
        invite = self.invite 
        guild = invite.guild
        return {
            'ru':f"""
                {Emoji.owner} Владелец: {guild.owner.mention}
                {Emoji.verified} Уровень проверки: Средний
                {Emoji.create} Создан: {format_dt(guild.created_at,'f')} ({format_dt(guild.created_at,'R')})
                {Emoji.channel_text} Всего {len(guild.channels)} каналов
                {Emoji.text1}{Emoji.channel_text} Текстовые каналы: {len(guild.text_channels)}
                {Emoji.text1}{Emoji.channel_voice}  Голосовые каналы: {len(guild.voice_channels)}
                {Emoji.text1}{Emoji.channel_forum}  Форум: {len(guild.forum_channels)}
                {Emoji.text1}{Emoji.channel_stage}  Трибуны: {len(guild.stage_channels)}
                {Emoji.text2}{Emoji.category}  Категории: {len(guild.categories)}
                {Emoji.member} Всего {guild.member_count} пользователя
                {Emoji.text1}Ботов: {len(guild.bots)}
                {Emoji.text2}Участников: {len(guild.humans)}
            """.replace("    ", "")
        }
    
    channel_type = {
        0:'<:channel_text:1166001040198484178>',
        1:'<:channel_text:1166001040198484178>',
        2:'<:channel_voice:1166001038772404284>',
        3:'<:category:1166001036553621534>',
        4:'<:category:1166001036553621534>',
        5:'<:channel_announce:1166092338242785370>',
        10:'<:thread:1166096258511937666>',
        11:'<:thread:1166096258511937666>',
        12:'<:thread:1166096258511937666>',
        13:'<:channel_stage:1166092341317226566> ',
        14:'<:category:1166001036553621534>',
        15:'<:channel_forum:1166094701020070009> ',
        16:'<:channel_forum:1166094701020070009> ',
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