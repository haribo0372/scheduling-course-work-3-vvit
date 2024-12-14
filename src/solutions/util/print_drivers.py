def print_schedule_driers_v1(driver_schedule_v1: list[dict[str, str]]) -> None:
    """
    Функция для понятного вывода водителей варианта_1 в терминал
    :param driver_schedule_v1: list[dict[str, str]]
    :return: None
    """
    print("\nРасписание водителей (Вариант 1):")
    for schedule in driver_schedule_v1:
        print(f"Водитель: {schedule['driver']},\n"
              f"\tНачало работы: {schedule['start']},\n"
              f"\tОбед: {schedule['lunch']},\n"
              f"\tКонец работы: {schedule['end']}")


def print_schedule_driers_v2(driver_schedule_v2: list[dict]) -> None:
    """
    Функция для понятного вывода водителей варианта_2 в терминал
    :param driver_schedule_v2: list[dict]
    :return: None
    """
    print("\nРасписание водителей (Вариант 2):")
    for schedule in driver_schedule_v2:
        print(
            f"Водитель: {schedule['driver']},"
            f"\n\tНачало работы: {schedule['start']},"
            f"\n\tПерерывы: {', '.join(schedule['breaks'])},"
            f"\n\tКонец работы: {schedule['end']}")
