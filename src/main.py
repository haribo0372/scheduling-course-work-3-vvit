from src.solutions.compare_time import compare_time
from src.solutions.complete_bust.solution import solution_by_complete_bust
from src.solutions.genetic_algorithm.solution import solution_by_genetic_algorithm

# Запуск программы
if __name__ == "__main__":
    solution_by_complete_bust()
    solution_by_genetic_algorithm()
    compare_time()
