from easy_pil import Editor, Font, load_image

url = f"https://cdn.discordapp.com/avatars/636824998123798531/a2b7ba0e13dd4df0e77e767c5fc31813.png?size=128"

background = Editor("tests/background.jpeg").resize((800, 450))

profile_image = load_image(url)
profile = Editor(profile_image).resize((150, 150)).circle_image()


poppins = Font("tests/Nunito-ExtraBold.ttf", 50) #Font.poppins(size=50, variant="bold")
poppins_small = Font("tests/Nunito-ExtraBold.ttf", 25) #Font.poppins(size=25, variant="regular")
poppins_light = Font("tests/Nunito-ExtraBold.ttf", 20) #Font.poppins(size=20, variant="light")

background.paste(profile, (325, 90))
background.ellipse((325, 90), 150, 150, outline=(125, 249, 255), stroke_width=4)
background.text((400, 260), "WELCOME TO SERVER", color="white", font=poppins, align="center")
background.text(
    (400, 320), "LordCode", color="white", font=poppins_small, align="center"
)
background.text(
    (400, 360),
    "You are the 457th Member",
    color="#F5923B",
    font=poppins_small,
    align="center",
)

background.show()