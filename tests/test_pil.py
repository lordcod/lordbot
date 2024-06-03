from PIL import Image, ImageDraw, ImageFile
from typing import List
ImageFile.LOAD_TRUNCATED_IMAGES = True

roulette_image = Image.open('assets/roulette.png')
ball_image = Image.open('assets/ball.png')

ball_image = ball_image.resize((25, 25))


roulette_board = roulette_image.copy()
roulette_board = roulette_board.rotate(0)

tmp_img = Image.new('RGBA', roulette_board.size, color=(0, 0, 0, 0))
tmp_img.paste(ball_image,
              box=((roulette_image.size[0]-ball_image.size[0])//2,
                   (202-ball_image.size[1])//2))
roulette_board.alpha_composite(tmp_img)


images: List[Image.Image] = []

width = 200
center = width // 2
color_1 = (0, 0, 0)
color_2 = (255, 255, 255)
max_radius = int(center * 1.5)
step = 1

for i in range(0, max_radius, step):
    im = Image.new('RGB', (width, width), color_1)
    draw = ImageDraw.Draw(im)
    draw.ellipse((center - i, center - i, center +
                 i, center + i), fill=color_2)
    images.append(im)

for i in range(0, max_radius, step):
    im = Image.new('RGB', (width, width), color_2)
    draw = ImageDraw.Draw(im)
    draw.ellipse((center - i, center - i, center +
                 i, center + i), fill=color_1)
    images.append(im)

images[0].save(
    'pillow_imagedraw.gif',
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=20,
    loop=0
)
