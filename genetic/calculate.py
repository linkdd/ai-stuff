# -*- coding: utf-8 -*-

from redbaron import RedBaron
import random
import ipdb


class Candidate(object):
    __slots__ = ['score', 'adn']

    def __init__(self, game, goal, parents=None, *args, **kwargs):
        super(Candidate, self).__init__(*args, **kwargs)

        game = list(game)
        random.shuffle(game)

        self.adn = ''

        if parents is None:
            for i in range(len(game)):
                if i > 0:
                    self.adn += random.choice(['+', '-', '*', '/'])

                self.adn += str(game[i])

        else:
            a = RedBaron(parents[0].adn)
            a_nb = [n.value for n in a.find_all('float')]
            a_op = [n.value for n in a.find_all('binary_operator')]

            b = RedBaron(parents[1].adn)
            b_nb = [n.value for n in b.find_all('float')]
            b_op = [n.value for n in b.find_all('binary_operator')]

            # combination
            numbers = a_nb[:3] + b_nb[3:]
            operators = b_op[:3] + a_op[3:]

            # mutation
            i = random.randrange(0, len(operators))
            operators[i] = random.choice(['+', '-', '*', '/'])

            self.adn += str(numbers.pop(0))

            while len(operators) > 0:
                self.adn += operators.pop(0)
                self.adn += str(numbers.pop(0))

        self.score = abs(goal - eval(self.adn))


class Game(object):
    def __init__(self, n=1000, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        elements = list(range(1, 11)) * 2 + [25, 50, 75, 100]
        elements = [float(e) for e in elements]
        self.game = random.sample(elements, 6)
        self.goal = float(random.randint(100, 999))

        self.generation = 1
        self.population = [Candidate(self.game, self.goal) for _ in range(n)]

    def selection(self):
        scored = sorted(self.population, key=lambda c: c.score)
        scored = scored[:int(len(scored) / 2)]
        parents = []

        for _ in range(4):
            _set = list(scored)

            while len(_set) > 1:
                i = random.randrange(0, len(_set))
                a = _set.pop(i)

                i = random.randrange(0, len(_set))
                b = _set.pop(i)

                parents.append((a, b))

        self.population = [
            Candidate(self.game, self.goal, parents=couple)
            for couple in parents
        ]

        self.generation += 1

    def show(self):
        for candidate in sorted(self.population, key=lambda c: -c.score):
            print('{0} = {1}\t|\t{2}'.format(
                candidate.adn,
                eval(candidate.adn),
                candidate.score
            ))

        scores = [c.score for c in self.population]
        avg = sum(scores) / len(scores)

        print('Generation: {0}'.format(self.generation))
        print('Goal: {0}'.format(self.goal))
        print(
            'Average: {0} (>{1}%, <{2}%)'.format(
                avg,
                100.0 * len(filter(lambda s: s >= avg, scores)) / len(scores),
                100.0 * len(filter(lambda s: s < avg, scores)) / len(scores)
            )
        )
        print(
            'Ecart-type: {0}'.format(max(scores) - min(scores))
        )

if __name__ == '__main__':
    import sys

    n = None
    steps = 0

    if len(sys.argv) > 1:
        n = int(sys.argv[1])

    if len(sys.argv) > 2:
        steps = int(sys.argv[2])

    g = Game(n=n)
    wins = []

    while True:
        g.show()

        if steps == 0:
            a = raw_input('Y/n: ')

            if a == 'n':
                break

        else:
            steps -= 1

        g.selection()

        wins = filter(lambda c: c.score == 0.0, g.population)

        if len(wins) > 0:
            break

    if wins:
        print('WIN:')

        for win in wins:
            print(win.adn)
