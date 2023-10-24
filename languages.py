import nextcord
from datetime import datetime

exemple = {
    'ru':'',
    'en':''
}

class invites():
    def __init__(self,invite):
        self.invite = invite
    
    @property
    def description(self):
        guild = self.invite.guild
        invite = self.invite 
        return {
        'ru' : f"### **{self.channel_type[invite.channel.type.value]}{invite.channel.name}**"
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