from captcha.image import ImageCaptcha
from io import BytesIO
from PIL import Image
import string
import random

list_upper = string.ascii_uppercase
def generator(num):
    text = "".join([random.choice(list_upper) for i in range(num)])
    image = ImageCaptcha(width = 280, height = 90)
    captcha_image = ImageCaptcha(
        width=400,
        height=220,
        fonts=[
            'SF-Pro',
            'SF-Compact-Rounded-Black',
            'SF-Pro-UltraLightItalic',
            'Neoneon'
        ],
        font_sizes=(40,70,100)
    )
    data:BytesIO = image.generate(text)
    return data,text