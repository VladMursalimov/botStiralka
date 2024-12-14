times_hours = [i for i in range(0, 24)]


times = [f'с {i:02}:00 до {i + 3:02}:00' for i in range(20)]

shifted_times = [f'с {(i + j) % 24:02}:00 до {(i + j + 3) % 24:02}:00'
                 for i in range(20) for j in range(3)]

all_times = sorted(set(shifted_times))

times = all_times

day_deltas = [
    "Сегодня",
    "Завтра",
    "Послезавтра",
]
