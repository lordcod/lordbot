from easy_pil import Editor, load_image, Font

AVATAR_SIZE = 128
guild_name = "Dev"
name = "LordCode"

url = f"https://cdn.discordapp.com/avatars/636824998123798531/a2b7ba0e13dd4df0e77e767c5fc31813.png?size={AVATAR_SIZE}"

def cut_back(string: str, length: int):
    ellipsis = "..."
    current_lenght = len(string)
    if length >= current_lenght:
        return string
    
    cropped_string = string[:length-len(ellipsis)].strip()
    new_string = f"{cropped_string}{ellipsis}"
    return new_string


background = Editor("tests/background.jpg").resize((800, 450))
profile_image = load_image(url).resize((128, 128))

profile = Editor(profile_image).resize((150, 150)).circle_image()
poppins = Font("tests/Nunito-ExtraBold.ttf", size=50) 
poppins_small = Font("tests/Nunito-ExtraBold.ttf", size=20) 
background.paste(profile, (325, 90))
background.ellipse((325, 90), 150, 150, outline=(37, 150, 190), stroke_width=5)


background.text((400, 260), f"WELCOME TO {cut_back(guild_name.upper(), 14)}", color="blue", font=poppins, align="center")
background.text((400, 325), name, color="blue", font=poppins_small, align="center")

background.show()