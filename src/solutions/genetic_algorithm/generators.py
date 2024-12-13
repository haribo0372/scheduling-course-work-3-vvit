import random
from datetime import timedelta, datetime

from src.solutions.genetic_algorithm import NUM_BUSES, BUS_INTERVAL_MIN


# Функция для генерации начального расписания автобусов
def generate_initial_bus_schedule():
    schedule = []
    current_time = datetime(2024, 1, 1, 6, 0)
    # Генерируем время отправления автобусов с интервалом 10 минут
    for _ in range(NUM_BUSES):
        schedule.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=BUS_INTERVAL_MIN)
    return schedule


# Функция для генерации расписания водителей
def generate_driver_schedule(num_drivers, work_hours, variant=1):
    driver_schedule = []
    for i in range(num_drivers):
        shift_start = random.randint(6, 10)
        start_time = datetime(2024, 1, 1, shift_start, 0)
        if variant == 1:
            work_period = timedelta(hours=work_hours)
            lunch_start = start_time + timedelta(hours=4)
            lunch_end = lunch_start + timedelta(hours=1)
            end_time = start_time + work_period + timedelta(hours=1)
            driver_schedule.append({
                "driver": f"Driver {i + 1} (V1)",
                "start": start_time.strftime("%H:%M"),
                "lunch": f"{lunch_start.strftime('%H:%M')} - {lunch_end.strftime('%H:%M')}",
                "end": end_time.strftime("%H:%M"),
                "variant": 1
            })
        elif variant == 2:
            work_period = timedelta(hours=work_hours)
            # Перерывы в расписании второго варианта
            breaks = []
            current_time = start_time
            while current_time < start_time + work_period:
                current_time += timedelta(hours=random.randint(2, 4))
                if current_time < start_time + work_period:
                    breaks.append(current_time.strftime("%H:%M"))
            end_time = start_time + work_period
            driver_schedule.append({
                "driver": f"Driver {i + 1} (V2)",
                "start": start_time.strftime("%H:%M"),
                "breaks": breaks,
                "end": end_time.strftime("%H:%M"),
                "variant": 2
            })
    return driver_schedule


# Генерация нагрузки пассажиров для всех часов
def generate_passenger_load():
    load = [random.randint(20, 50) for _ in range(24)]  # Базовая загрузка
    for hour in range(7, 9):  # Утренний час пик
        load[hour] += 50
    for hour in range(17, 19):  # Вечерний час пик
        load[hour] += 50
    return load
