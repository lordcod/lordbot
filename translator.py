import translators as ts

text = "이 문장은 한글로 쓰여졌습니다."

lang = 'ru'

res = ts.translate_text(query_text=text,translator='google',to_language=lang)
ts
print(type(res))