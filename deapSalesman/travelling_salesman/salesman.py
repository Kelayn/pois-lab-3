import numpy as np


class Salesman:

    def __init__(self, toolbox, population_size=10, iterations=5, n_matings=2):
        self.toolbox = toolbox
        self.iterations = iterations
        self.population_size = population_size
        self.n_matings = n_matings

    def set_fitness(self, population):
        # массив данных об индивидуальной особи и ее лучшем значении
        fitnesses = [
            (individual, self.toolbox.summarize_path(individual))
            for individual in population
        ]
        for individual, fitness in fitnesses:
            individual.fitness.values = (fitness,)

    def get_offspring(self, population):
        n = len(population)
        for _ in range(self.n_matings):
            i1, i2 = np.random.choice(range(n), size=2, replace=False)

            offspring1, offspring2 = \
                self.toolbox.mate(population[i1], population[i2])

            yield self.toolbox.mutate(offspring1)[0]
            yield self.toolbox.mutate(offspring2)[0]

    @staticmethod
    def pull_stats(population, iteration=1):
        fitnesses = [individual.fitness.values[0] for individual in population]
        return {
            'i': iteration,
            'mu': np.mean(fitnesses),
            'std': np.std(fitnesses),
            'max': np.max(fitnesses),
            'min': np.min(fitnesses)
        }

    def Run(self):
        population = self.toolbox.population(n=self.population_size)
        self.set_fitness(population)

        stats = []
        for iteration in list(range(1, self.iterations + 1)):
            current_population = list(map(self.toolbox.clone, population))
            offspring = list(self.get_offspring(current_population))
            for child in offspring:
                current_population.append(child)

            # reset fitness
            self.set_fitness(current_population)

            population[:] = self.toolbox.select(current_population,
                                                len(population))
            stats.append(
                Salesman.pull_stats(population, iteration))

        return stats, population
