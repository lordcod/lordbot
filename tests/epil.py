from easy_pil import Editor, load_image, Font

AVATAR_SIZE = 128
guild_name = "SERVER"
name = "LordCord"

background = Editor("tests/background.jpg").resize((800, 450))
profile_image = load_image(f"https://cdn.discordapp.com/avatars/636824998123798531/a2b7ba0e13dd4df0e77e767c5fc31813.png?size={AVATAR_SIZE}")

profile = Editor(profile_image).resize((150, 150)).circle_image()
poppins = Font("tests/Fredoka.ttf", size=50) #Font.poppins(size=50, variant="bold")
poppins_small = Font("tests/Fredoka.ttf", size=20) #Font.poppins(size=20, variant="light")
background.paste(profile, (325, 90))
background.ellipse((325, 90), 150, 150, outline=(37, 150, 190), stroke_width=5)

background.text((400, 260), f"WELCOME TO {guild_name}", color="blue", font=poppins, align="center")
background.text((400, 325), f"{name}", color="blue", font=poppins_small, align="center")

background.show()