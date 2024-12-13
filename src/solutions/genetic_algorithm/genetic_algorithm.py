import random
from datetime import datetime, timedelta

from src.solutions.genetic_algorithm import NUM_BUSES, BUS_INTERVAL_MIN, WORK_HOURS_VARIANT_1, \
    WORK_HOURS_VARIANT_2, GENERATION_SIZE, NUM_DRIVERS, MUTATION_RATE, NUM_GENERATIONS, \
    MIN_NUM_DRIVER_VARIANT_1
from src.solutions.genetic_algorithm.generators import generate_initial_bus_schedule, \
    generate_driver_schedule


# Функция приспособленности
def fitness_function(individual):
    bus_schedule = individual["bus_schedule"]
    driver_schedule = individual["driver_schedule"]

    # Базовый показатель
    fitness = 1000 - len(driver_schedule) * 50 - NUM_BUSES * 20

    # Штрафы
    penalty = 0

    # Проверяем интервалы между автобусами
    for i in range(1, len(bus_schedule)):
        time_diff = (
                int(bus_schedule[i].split(":")[0]) * 60 + int(bus_schedule[i].split(":")[1]) -
                (int(bus_schedule[i - 1].split(":")[0]) * 60 + int(
                    bus_schedule[i - 1].split(":")[1])))
        if time_diff < BUS_INTERVAL_MIN:
            penalty += 10

    # Проверяем расписание водителей
    num_drivers_variant_1 = sum(1 for driver in driver_schedule if driver["variant"] == 1)
    num_drivers_variant_2 = len(driver_schedule) - num_drivers_variant_1

    if num_drivers_variant_1 < MIN_NUM_DRIVER_VARIANT_1:
        penalty += (
                               MIN_NUM_DRIVER_VARIANT_1 - num_drivers_variant_1) * 50  # Штраф за каждого водителя, которого не хватает до 7

    for driver in driver_schedule:
        start_time = datetime.strptime(driver["start"], "%H:%M")
        end_time = datetime.strptime(driver["end"], "%H:%M")
        max_hours = WORK_HOURS_VARIANT_1 if driver["variant"] == 1 else WORK_HOURS_VARIANT_2
        if end_time - start_time > timedelta(hours=max_hours):
            penalty += 20

    # Итоговая приспособленность
    fitness -= penalty
    return max(fitness, 0)

# Создание популяции
def create_population():
    population = []
    for _ in range(GENERATION_SIZE):
        num_drivers_variant_1 = random.randint(1, NUM_DRIVERS - 1)  # Минимум один водитель каждого варианта
        num_drivers_variant_2 = NUM_DRIVERS - num_drivers_variant_1

        # Генерация расписаний для обоих типов водителей
        driver_schedule_variant_1 = generate_driver_schedule(num_drivers_variant_1, WORK_HOURS_VARIANT_1, variant=1)
        driver_schedule_variant_2 = generate_driver_schedule(num_drivers_variant_2, WORK_HOURS_VARIANT_2, variant=2)

        individual = {
            "bus_schedule": generate_initial_bus_schedule(),
            "driver_schedule": driver_schedule_variant_1 + driver_schedule_variant_2
        }
        population.append(individual)
    return population

# Скрещивание
def crossover(parent1, parent2):
    split_point = len(parent1["bus_schedule"]) // 2
    child = {
        "bus_schedule": parent1["bus_schedule"][:split_point] + parent2["bus_schedule"][split_point:],
        "driver_schedule": parent1["driver_schedule"][:split_point] + parent2["driver_schedule"][split_point:]
    }
    return child

# Мутация
def mutate(individual):
    if random.random() < MUTATION_RATE:
        individual["bus_schedule"][random.randint(0, len(individual["bus_schedule"]) - 1)] = generate_initial_bus_schedule()[0]
    if random.random() < MUTATION_RATE:
        new_variant = 1 if random.random() > 0.5 else 2
        individual["driver_schedule"][random.randint(0, len(individual["driver_schedule"]) - 1)] = generate_driver_schedule(1, WORK_HOURS_VARIANT_1 if new_variant == 1 else WORK_HOURS_VARIANT_2, variant=new_variant)[0]
    return individual

# Основной алгоритм
def genetic_algorithm():
    population = create_population()
    for generation in range(NUM_GENERATIONS):
        population = sorted(population, key=fitness_function, reverse=True)
        next_generation = population[:10]  # Топ 10 лучших особей

        while len(next_generation) < GENERATION_SIZE:
            parent1 = random.choice(population[:20])
            parent2 = random.choice(population[:20])
            child = crossover(parent1, parent2)
            next_generation.append(mutate(child))

        population = next_generation

        # Лучшая приспособленность текущего поколения
        best_individual = population[0]
        print(f"Поколение {generation + 1}: Лучшая приспособленность = {fitness_function(best_individual)}")

    return population[0]


