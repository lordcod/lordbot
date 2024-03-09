import i18n

# i18n.add_translation('foo', 'bar')

i18n.load_path.append('C:/Users/2008d/git/lordbot/bot/languages/localization')

title = i18n.t("bot-info", locale="en")

print(title)
