from datetime import datetime

from src.solutions.complete_bust import NUM_DRIVERS, WORK_HOURS_V1, WORK_HOURS_V2
from src.solutions.complete_bust.generators import generate_bus_schedule, generate_driver_schedule, \
    determine_interval
from src.solutions.util.print_drivers import print_schedule_driers_v1, print_schedule_driers_v2
from src.solutions.util.write_to_excel import write_to_xlsx


def solution_by_complete_bust() -> None:
    """
    Основная функция для симуляции расписания
    :return: None
    """

    print("\t\t\tМЕТОД ПОЛНОГО ПЕРЕБОРА НАЧАЛСЯ\n")
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
    print(*bus_schedules)

    print_schedule_driers_v1(driver_schedule_v1)
    print_schedule_driers_v2(driver_schedule_v2)

    write_to_xlsx("_1_bus_schedule", bus_schedules, driver_schedule_v1, driver_schedule_v2)
