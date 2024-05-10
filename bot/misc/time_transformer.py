
class DatePluralRussia:
    @staticmethod
    def plural(numbers: int, forms: list[str]) -> str:
        idx = None
        if numbers % 10 == 1 and numbers % 100 != 11:
            idx = 0
        elif numbers % 10 >= 2 and numbers % 10 <= 4 and (numbers % 100 < 10 or numbers % 100 >= 20):
            idx = 1
        else:
            idx = 2
        return f"{numbers} {forms[idx]}"

    @staticmethod
    def years(timestamp: int):
        forms = ['год', 'года', 'лет']
        return DatePluralRussia.plural(timestamp, forms)

    @staticmethod
    def months(timestamp: int):
        forms = ['месяц', 'месяца', 'месяцов']
        return DatePluralRussia.plural(timestamp, forms)

    @staticmethod
    def days(timestamp: int):
        forms = ['день', 'дня', 'дней']
        return DatePluralRussia.plural(timestamp, forms)

    @staticmethod
    def hours(timestamp: int):
        forms = ['час', 'часа', 'часов']
        return DatePluralRussia.plural(timestamp, forms)

    @staticmethod
    def minutes(timestamp: int):
        forms = ['минута', 'минуты', 'минут']
        return DatePluralRussia.plural(timestamp, forms)

    @staticmethod
    def seconds(timestamp: int):
        forms = ['секунда', 'секунды', 'секунд']
        return DatePluralRussia.plural(timestamp, forms)

    def convertor(timestamp: int, great: str):
        method = getattr(DatePluralRussia, great)
        return method(timestamp)


def DataPluralEnglish(timestamp: int, great: str):
    if timestamp == 1:
        return f"{timestamp} {great.rstrip('s')}"
    return f"{timestamp} {great}"


distributing = {
    'ru': DatePluralRussia.convertor,
    'en': DataPluralEnglish
}


def time_convert(timestamp: (int | float)) -> dict[str, int]:
    return {
        "months": int(timestamp / 2_631_600 % 12),
        "days": int(timestamp / 86_400 % 30),
        "hours": int(timestamp / 3_600 % 24),
        "minutes": int(timestamp / 60 % 60),
        "seconds": int(timestamp % 60)
    }


def display_time(number: int, lang: str = "en") -> str:
    distributing.get(lang, distributing['en'])
    current_time = time_convert(number)
    time_strings = [distributing[lang](num, key)
                    for key, num in current_time.items() if num != 0]
    return ", ".join(time_strings)
