from __future__ import annotations
import time


class DatePlural:
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
        return DatePlural.plural(timestamp, forms)

    @staticmethod
    def months(timestamp: int):
        forms = ['месяц', 'месяца', 'месяцов']
        return DatePlural.plural(timestamp, forms)
    
    @staticmethod
    def days(timestamp: int):
        forms = ['день', 'дня', 'дней']
        return DatePlural.plural(timestamp, forms)
    
    @staticmethod
    def hours(timestamp: int):
        forms = ['час', 'часа', 'часов']
        return DatePlural.plural(timestamp, forms)
    days
    @staticmethod
    def minutes(timestamp: int):
        forms = ['минута', 'минуты', 'минут']
        return DatePlural.plural(timestamp, forms)
    
    @staticmethod
    def seconds(timestamp: int):
        forms = ['секунда', 'секунды', 'секунд']
        return DatePlural.plural(timestamp, forms)


def time_convert(timestamp: (int|float)) -> dict[str, int]:
    return {
        "months": round(timestamp / 2_631_600 % 12),
        "days": round(timestamp / 86_400 % 30),
        "hours": round(timestamp / 3_600 % 24),
        "minutes": round(timestamp / 60 % 60),
        "seconds": round(timestamp % 60)
    }

def sub_convertor(timestamp):
    timestamp = int(timestamp)
    
    years = 0
    months = 0
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    
    while timestamp > 0:
        timestamp -= 1
        seconds += 1
        
        if seconds == 60:
            seconds = 0
            minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 24:
            hours = 0
            days += 1
        if days == 30:
            days = 0
            months += 1
        if months == 12:
            months = 0
            years += 1
    
    return {
        "years": years,
        "months": months,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }



current_time = time_convert(1_000_000_000)
cur_sub_time = sub_convertor(1_000_000_000)

print(current_time, cur_sub_time)


for key, num in current_time.items():
    if num == 0:
        continue
    method = getattr(DatePlural, key)
