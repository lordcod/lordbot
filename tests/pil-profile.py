import PIL
import requests
from PIL import Image, ImageDraw, ImageFont
import io

AVATAR_SIZE = 128
name = "LordCord"
avatar = requests.get(f"https://cdn.discordapp.com/avatars/636824998123798531/a2b7ba0e13dd4df0e77e767c5fc31813.png?size={AVATAR_SIZE}").content
font = ImageFont.truetype("Fredoka.ttf", 52)

image = Image.open("background.jpg").resize((480, AVATAR_SIZE*2))

weightImg, heightImg = image.size


draw = ImageDraw.Draw(image)
l, r, weightTb, heightTb = draw.textbbox((0, 0), name, font=font)
draw.text(
    (
        ((weightImg-AVATAR_SIZE-weightTb)/2)+AVATAR_SIZE, 
        (heightImg-heightTb-(heightImg/20))//2
    ), 
    name, 
    font=font, 
    fill="black"
)


avatar_image = Image.open(io.BytesIO(avatar))
avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) 

circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
circle_draw = ImageDraw.Draw(circle_image)
circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)

avatar_image.putalpha(circle_image)

image.paste(avatar_image, (10, (heightImg-AVATAR_SIZE)//2), circle_image)


image.show()