import datetime

times = ['с 0:00 до 2:00',
         'с 2:00 до 4:00',
         'с 4:00 до 6:00',
         'с 6:00 до 8:00',
         'с 8:00 до 10:00',
         'с 10:00 до 12:00',
         'с 12:00 до 14:00',
         'с 14:00 до 16:00',
         'с 16:00 до 18:00',
         'с 18:00 до 20:00',
         'с 20:00 до 22:00',
         'с 22:00 до 24:00', ]

times_hours = [
    i for i in range(0, 24, 2)
]

day_deltas = [
    "Сегодня",
    "Завтра",
    "Послезавтра",
]