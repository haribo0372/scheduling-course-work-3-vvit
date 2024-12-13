from openpyxl.workbook import Workbook


def write_to_xlsx(file_name: str,
                  bus_schedules: list,
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
    path_to_xlsx_file = f"excel_files/{file_name}.xlsx"
    workbook.save(path_to_xlsx_file)
    print(
        f"Результаты успешно записаны в '{path_to_xlsx_file}'")
