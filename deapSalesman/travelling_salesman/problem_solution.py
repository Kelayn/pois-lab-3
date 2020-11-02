import random
import string
import numpy as np
from deap import base, creator, tools
from travelling_salesman import salesman


class ProblemSolution:
    def __init__(
            self, individual_size, population_size,
            n_iterations, n_matings, distances
    ):
        self.toolbox = base.Toolbox()
        self.POPULATION_SIZE = population_size
        self.N_ITERATIONS = n_iterations
        self.N_MATINGS = n_matings
        self.distances = distances

        # объявление класса Fitness_Min, наследующего base.Fitness
        # с базовыми весами -1.0. base.Fitness предоставляет интерфейс
        # для взаимодействия со значениями функции и ее весами:
        # максимизация, минимазация, сравнение
        creator.create("Fitness_Min", base.Fitness, weights=(-1.0,))
        # объявление класса Individual, наследующегося от list
        # в качестве fitness переаем ранее объявленный класс
        creator.create("Individual", list, fitness=creator.Fitness_Min)

        # регистрация вспомогательной функции indices
        # для получения массива уникальных значений от 0 до INDIVIDUAL_SIZE
        # так мы удостоверимся, что особь попадет в каждый город без повторений
        self.toolbox.register(
            "indices", random.sample, range(individual_size), individual_size
        )

        # регистрация вспомогательной функции individual - инициализации
        # особи функцией initIterate, принимающей контейнер и генератор
        # в нашем случае ранее обявленные Individual(list) и indices()
        self.toolbox.register(
            "individual",
            tools.initIterate,
            creator.Individual,
            self.toolbox.indices
        )

        # регистрация функции инициалиазации популяции
        self.toolbox.register(
            "population",
            tools.initRepeat,
            list,
            self.toolbox.individual
        )

    # функция подчета пройденного расстояния
    # начальная точка - первый элемент indices()
    def summarize_path(self, individual):
        summation = 0
        start = individual[0]
        for i in range(1, len(individual)):
            end = individual[i]
            summation += self.distances[start][end]
            start = end
        return summation

    def solve(self):

        # регистрация функций для выполнения алгоритма
        # алгоритм: посчитать путь, произвести кроссовер
        # добавить мутацию с незавимой вероятностью для гена в 0.01
        # произвести выборку с помощью random.choice (со скидкой на weights)
        self.toolbox.register("summarize_path", self.summarize_path)
        self.toolbox.register("mate", tools.cxOrdered)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.01)
        self.toolbox.register("select", tools.selTournament, tournsize=10)

        running_salesman = salesman.Salesman(
            self.toolbox, self.POPULATION_SIZE, self.N_ITERATIONS,
            self.N_MATINGS
        )

        return running_salesman.Run()
