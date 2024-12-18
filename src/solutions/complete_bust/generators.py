import random
from datetime import datetime, timedelta

from src.solutions.complete_bust import (PEAK_HOURS, INTERVAL_PEAK, NORMAL_HOURS, INTERVAL_NORMAL,
                                         INTERVAL_LOW, LOW_HOURS)


def generate_bus_schedule(start_time: int, end_time: int, interval: int) -> list[int]:
    """
    Функция для генерации расписания автобусов

    :param start_time: int
    :param end_time: int
    :param interval: int
    :return: list
    """
    schedule = []
    current_time = start_time
    while current_time < end_time:
        schedule.append(current_time)
        current_time += timedelta(minutes=interval)
    return schedule


def determine_interval(hour: int) -> int:
    """
    Функция для определения интервалов между автобусами по потоку пассажиров

    :hour: int
    :return: int
    """
    for start, end in PEAK_HOURS:
        if start <= hour < end:
            return INTERVAL_PEAK
    for start, end in NORMAL_HOURS:
        if start <= hour < end:
            return INTERVAL_NORMAL
    for start, end in LOW_HOURS:
        if start <= hour < end:
            return INTERVAL_LOW
    return INTERVAL_LOW


def generate_driver_schedule(num_drivers: int,
                             work_hours: int,
                             start_interval: int,
                             variant: int = 1) -> list[dict]:
    """
    Функция для распределения водителей

    :param num_drivers: int
    :param work_hours: int
    :param start_interval: int
    :param variant: int
    :return: list[dict[str, list/str]]
    """
    driver_schedule = []
    for i in range(num_drivers):
        shift_start = random.randint(6, start_interval)
        start_time = datetime(2024, 1, 1, shift_start, 0)
        if variant == 1:
            work_period = timedelta(hours=work_hours)
            lunch_start = start_time + timedelta(hours=4)
            lunch_end = lunch_start + timedelta(hours=1)
            end_time = start_time + work_period + timedelta(hours=1)
            driver_schedule.append({
                "driver": f"Driver {i + 1}",
                "start": start_time.strftime("%H:%M"),
                "lunch": f"{lunch_start.strftime('%H:%M')} - {lunch_end.strftime('%H:%M')}",
                "end": end_time.strftime("%H:%M")
            })
        elif variant == 2:
            work_period = timedelta(hours=work_hours)
            break_intervals = []
            current_time = start_time
            while current_time < start_time + work_period:
                current_time += timedelta(hours=random.randint(2, 4))
                if current_time < start_time + work_period:
                    break_intervals.append(current_time.strftime("%H:%M"))
            end_time = start_time + work_period
            driver_schedule.append({
                "driver": f"Driver {i + 1}",
                "start": start_time.strftime("%H:%M"),
                "breaks": break_intervals,
                "end": end_time.strftime("%H:%M")
            })
    return driver_schedule
