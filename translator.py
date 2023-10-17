import googletrans
translate = googletrans.Translator()

text = "이 문장은 한글로 쓰여졌습니다"

laungs = googletrans.LANGUAGES
detect = translate.detect(text)
tanslators = translate.translate(text,dest='ru')

print(detect.lang)
print(tanslators) 