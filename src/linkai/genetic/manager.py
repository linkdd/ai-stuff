# -*- coding: utf-8 -*-

from b3j0f.conf.configurable import Configurable
from b3j0f.conf.configurable.decorators import conf_paths, add_category
from b3j0f.conf.params import Parameter
from b3j0f.utils import lookup


CONF_PATH = 'linkai/genetic.conf'
CATEGORY = 'GENETIC'
CONTENT = [
    Parameter('population_size', int),
    Parameter('new_candidate'),
    Parameter('fitness'),
    Parameter('selection'),
    Parameter('make_couples'),
    Parameter('crossover'),
    Parameter('mutation'),
    Parameter('test'),
    Parameter('show')
]


@conf_paths(CONF_PATH)
@add_category(CATEGORY, content=CONTENT)
class Genetic(Configurable):
    @property
    def population_size(self):
        if not hasattr('_population_size'):
            self.population_size = None

        return self._population_size

    @population_size.setter
    def population_size(self, value):
        if value is None:
            value = 1000

        self._population_size = value

    @property
    def new_candidate(self):
        if not hasattr('_new_candidate'):
            self.new_candidate = None

        return self._new_candidate

    @new_candidate.setter
    def new_candidate(self, value):
        if value is None:
            value = new_candidate

        if not callable(value):
            value = lookup(value)

        self._new_candidate = value

    @property
    def fitness(self):
        if not hasattr('_fitness'):
            self.fitness = None

        return self._fitness

    @fitness.setter
    def fitness(self, value):
        if value is None:
            value = fitness

        if not callable(value):
            value = lookup(value)

        self._fitness = value

    @property
    def selection(self):
        if not hasattr('_selection'):
            self.selection = None

        return self._selection

    @selection.setter
    def selection(self, value):
        if value is None:
            value = selection

        if not callable(value):
            value = lookup(value)

        self._selection = value

    @property
    def make_couples(self):
        if not hasattr('_make_couples'):
            self.make_couples = None

        return self._make_couples

    @make_couples.setter
    def make_couples(self, value):
        if value is None:
            value = make_couples

        if not callable(value):
            value = lookup(value)

        self._make_couples = value

    @property
    def crossover(self):
        if not hasattr('_crossover'):
            self.crossover = None

        return self._crossover

    @crossover.setter
    def crossover(self, value):
        if value is None:
            value = crossover

        if not callable(value):
            value = lookup(value)

        self._crossover = value

    @property
    def mutation(self):
        if not hasattr('_mutation'):
            self.mutation = None

        return self._mutation

    @mutation.setter
    def mutation(self, value):
        if value is None:
            value = mutation

        if not callable(value):
            value = lookup(value)

        self._mutation = value

    @property
    def test(self):
        if not hasattr('_test'):
            self.test = None

        return self._test

    @test.setter
    def test(self, value):
        if value is None:
            value = test

        if not callable(value):
            value = lookup(value)

        self._test = value

    @property
    def show(self):
        if not hasattr('_show'):
            self.show = None

        return self._show

    @show.setter
    def show(self, value):
        if value is not None and not callable(value):
            value = lookup(value)

        self._show = value

    def __init__(
        self,
        population_size=None,
        new_candidate=None,
        fitness=None,
        selection=None,
        make_couples=None,
        crossover=None,
        mutation=None,
        test=None,
        show=None,
        *args, **kwargs
    ):
        super(Genetic, self).__init__(*args, **kwargs)

        if population_size is not None:
            self.population_size = population_size

        if new_candidate is not None:
            self.new_candidate = new_candidate

        if fitness is not None:
            self.fitness = fitness

        if selection is not None:
            self.selection = selection

        if make_couples is not None:
            self.make_couples = make_couples

        if crossover is not None:
            self.crossover = crossover

        if mutation is not None:
            self.mutation = mutation

        if test is not None:
            self.test = test

        if show is not None:
            self.show = show

    def __call__(self, nstep=10):
        population = [
            self.new_candidate()
            for _ in range(self.population_size)
        ]

        for step in range(nstep):
            if self.show is not None:
                self.show(step, population)

            evaluated = [self.fitness(candidate) for candidate in population]
            selected = self.selection(evaluated)

            new_population = []

            while len(new_population) < len(population):
                couples = self.make_couples(selected)

                for a, b in couples:
                    child_a, child_b = self.crossover(a, b)
                    child_a = self.mutation(child_a)
                    child_b = self.mutation(child_b)

                    if self.test(child_a):
                        new_population.append(child_a)

                    if self.test(child_b):
                        new_population.append(child_b)

            population = new_population


def new_candidate():
    """
    :return: custom data
    """

    raise NotImplementedError()


def fitness(candidate):
    """
    :param candidate: candidate to evaluate
    :type candidate: returned from new_candidate()
    :return: evaluated candidate
    """

    raise NotImplementedError()


def selection(evaluated):
    """
    :param evaluated: list of evaluated candidates
    :type evaluated: list
    :return: list of candidates
    """

    raise NotImplementedError()


def make_couples(population):
    """
    :param population: list of candidates
    :type population: list
    :return: list of random pair from population
    """

    raise NotImplementedError()


def crossover(a, b):
    """
    :param a: candidate as parent A
    :param b: candidate as parent B
    :return: tuple containing child A and child B
    """

    raise NotImplementedError()


def mutation(candidate):
    """
    :param candidate: candidate to eventually mutate
    :return: mutated (or not) candidate
    """

    raise NotImplementedError()


def test(candidate):
    """
    :param candidate: test if candidate is viable
    :return: True if viable, False otherwise
    """

    raise NotImplementedError()


def show(step, population):
    """
    :param step: generation number
    :type step: int

    :param population: list of candidates
    :type population: list
    """
