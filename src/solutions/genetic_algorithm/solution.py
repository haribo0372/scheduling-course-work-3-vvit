from src.solutions.genetic_algorithm.genetic_algorithm import genetic_algorithm
from src.solutions.util.print_drivers import print_schedule_driers_v1, print_schedule_driers_v2
from src.solutions.util.write_to_excel import write_to_xlsx


def solution_by_genetic_algorithm():
    print("\n\n\n\t\t\tГЕНЕТИЧЕСКИЙ АЛГОРИТМ НАЧАЛСЯ\n")
    best_schedule = genetic_algorithm()
    driver_schedule_v1 = []
    driver_schedule_v2 = []

    for i, v in enumerate(best_schedule['driver_schedule'], start=1):
        if v['variant'] == 1:
            v['driver'] = f"Driver {i}"
            driver_schedule_v1.append(v)
        elif v['variant'] == 2:
            v['driver'] = f"Driver {i}"
            driver_schedule_v2.append(v)

    print("\nЛучшее расписание найдено:")
    print("Расписание автобусов (отправление):")
    print(*best_schedule['bus_schedule'])

    print_schedule_driers_v1(driver_schedule_v1)
    print_schedule_driers_v2(driver_schedule_v2)

    write_to_xlsx("_2_bus_schedule",
                  best_schedule['bus_schedule'], driver_schedule_v1, driver_schedule_v2)
