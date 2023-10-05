times_hours = [i for i in range(8, 24, 3) if i + 3 <= 24]

times = [f'с {"00" if i == 24 else i}:00 до {"00" if i + 3 == 24 else i + 3}:00' for i in times_hours]

day_deltas = [
    "Сегодня",
    "Завтра",
    "Послезавтра",
]
