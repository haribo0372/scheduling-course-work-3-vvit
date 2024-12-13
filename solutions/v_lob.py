from datetime import datetime, timedelta
from openpyxl import Workbook
import random

# Константы
NUM_BUSES = 8  # кол-во автобусов
NUM_DRIVERS = 10  # кол-во водителей
WORK_HOURS_V1 = 8  # рабочее время по варианту водителей 1
WORK_HOURS_V2 = 12  # рабочее время по варианту водителей 2
ROUTE_DURATION = 90  # длительность маршрута в минутах
PEAK_HOURS = [(7, 9), (17, 19)]  # границы времени самой высокой загруженности (часпик)
NORMAL_HOURS = [(10, 16)]  # границы времени нормальной загруженности
LOW_HOURS = [(6, 7), (19, 22)]  # границы времени легкой загруженности
INTERVAL_PEAK = 10  # интервал между автобусами в час пик (в минутах)
INTERVAL_NORMAL = 15  # интервал между автобусами в нормальной загруженности (в минутах)
INTERVAL_LOW = 20  # интервал между автобусами в легкой загруженности (в минутах)


# Функция для генерации расписания автобусов
def generate_bus_schedule(start_time, end_time, interval):
    schedule = []
    current_time = start_time
    while current_time < end_time:
        schedule.append(current_time)
        current_time += timedelta(minutes=interval)
    return schedule


# Функция для распределения водителей
def generate_driver_schedule(num_drivers, work_hours, start_interval, variant=1):
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


# Функция для определения интервалов между автобусами по потоку пассажиров
def determine_interval(hour):
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


def print_schedule_driers_v1(driver_schedule_v1):
    print("\nРасписание водителей (Вариант 1):")
    for schedule in driver_schedule_v1:
        print(f"Водитель: {schedule['driver']},\n"
              f"\tНачало работы: {schedule['start']},\n"
              f"\tОбед: {schedule['lunch']},\n"
              f"\tКонец работы: {schedule['end']}")


def print_schedule_driers_v2(driver_schedule_v2):
    print("\nРасписание водителей (Вариант 2):")
    for schedule in driver_schedule_v2:
        print(
            f"Водитель: {schedule['driver']},"
            f"\n\tНачало работы: {schedule['start']},"
            f"\n\tПерерывы: {', '.join(schedule['breaks'])},"
            f"\n\tКонец работы: {schedule['end']}")


def _1_write_to_xlsx(bus_schedules: list,
                  driver_schedule_v1: list[dict[str, str]],
                  driver_schedule_v2: list[dict[str, str]]) -> None:
    workbook = Workbook()
    sheet = workbook.active

    sheet["A1"] = "Расписание автобусов"
    sheet["A2"] = "первая половина"
    sheet["B2"] = "вторая половина"

    sheet["D1"] = "Расписание водителей (Вариант 1)"
    sheet["D2"] = "Водитель"
    sheet["E2"] = "Начало рабочего дня"
    sheet["F2"] = "Обед"
    sheet["G2"] = "Конец рабочего дня"


    sheet["D11"] = "Расписание водителей (Вариант 2)"
    sheet["D12"] = "Водитель"
    sheet["E12"] = "Начало рабочего дня"
    sheet["F12"] = "Перерывы"
    sheet["G12"] = "Конец рабочего дня"


    L = len(bus_schedules)
    middle = L // 2
    _1_bus_schedules = bus_schedules[:middle]
    _2_bus_schedules = bus_schedules[middle:]
    # Записываем расписание автобусов
    for i, time in enumerate(_1_bus_schedules, start=3):
        sheet[f"A{i}"] = time
    for i, time in enumerate(_2_bus_schedules, start=3):
        sheet[f"B{i}"] = time

    # Записываем расписание водителей (Вариант 1)
    for i, driver in enumerate(driver_schedule_v1, start=3):
        sheet[f"D{i}"] = driver['driver']
        sheet[f"E{i}"] = driver['start']
        sheet[f"F{i}"] = driver['lunch']
        sheet[f"G{i}"] = driver['end']

    # Записываем расписание водителей (Вариант 2)
    for i, driver in enumerate(driver_schedule_v2, start=13):
        sheet[f"D{i}"] = driver['driver']
        sheet[f"E{i}"] = driver['start']
        sheet[f"F{i}"] = ", ".join(driver['breaks'])
        sheet[f"G{i}"] = driver['end']

    # Сохраняем файл
    workbook.save("bus_schedule.xlsx")
    print("Результаты решения методом перебора успешно записаны в _1_bus_schedule.xlsx")


# Основная функция для симуляции расписания (решение в методом перебора)
def solution_v_lob():
    start_hour = 6
    end_hour = 22

    bus_schedules = []
    for hour in range(start_hour, end_hour):
        interval = determine_interval(hour)
        schedule = generate_bus_schedule(
            datetime(2024, 1, 1, hour, 0),
            datetime(2024, 1, 1, hour + 1, 0),
            interval
        )
        bus_schedules.extend([str(i.strftime("%H:%M")) for i in schedule])

    driver_schedule_v1 = generate_driver_schedule(NUM_DRIVERS // 2, WORK_HOURS_V1, 10, variant=1)
    driver_schedule_v2 = generate_driver_schedule(NUM_DRIVERS // 2, WORK_HOURS_V2, 10, variant=2)

    print("Расписание автобусов:")
    for bus_time in bus_schedules:
        print(bus_time)

    print_schedule_driers_v1(driver_schedule_v1)
    print_schedule_driers_v2(driver_schedule_v2)

    _1_write_to_xlsx(bus_schedules, driver_schedule_v1, driver_schedule_v2)
