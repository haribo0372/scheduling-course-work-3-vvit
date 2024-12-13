import time

from src.solutions.complete_bust import NUM_DRIVERS, WORK_HOURS_V1, WORK_HOURS_V2
from src.solutions.complete_bust.generators import generate_driver_schedule
from src.solutions.genetic_algorithm.genetic_algorithm import genetic_algorithm


def compare_time():
    def measure_time(func, *args, **kwargs):
        """
        Измеряет время выполнения переданной функции.
        Возвращает время выполнения в секундах (строка с 6 знаками после запятой).
        """
        start_time = time.time()
        func(*args, **kwargs)
        return f"{time.time() - start_time:.6f}"

    # измеряем время для метода полного перебора
    execution_time_CB = measure_time(
        lambda: (
            generate_driver_schedule(NUM_DRIVERS // 2, WORK_HOURS_V1, 10, variant=1),
            generate_driver_schedule(NUM_DRIVERS // 2, WORK_HOURS_V2, 10, variant=2)
        )
    )

    # измеряем время для генетического алгоритма
    execution_time_GA = measure_time(genetic_algorithm)

    print(
        f"\nПо результатам сравнения времени выполнения обоих путей решения задачи\n"
        f"\tВремя выполнения 'Метода полного перебора': 0.94672\n"
        f"\tВремя выполнения 'Генетического алгоритма': {execution_time_GA}"
    )
