import random

import numpy as np


class Artificial(object):

    def and_problem(self, npc=10, ruido=0.015):
        X = []
        for i, j in zip([0, 0, 1, 1], [0, 1, 0, 1]):
            for _ in range(npc):
                X.append([random.uniform( i + ((-1) ** (_+1)) * ruido, i + ((-1) ** _) * ruido),
                          random.uniform(j + ((-1) ** (_+1)) * ruido, j + ((-1) ** _) * ruido)])

        X = np.array(X)
        y = np.concatenate((np.zeros((3*npc, 1), dtype=int), np.ones((npc, 1), dtype=int)))

        y = np.reshape(y, (4*npc))
        return X, y

    def or_problem(self, npc=10, ruido=0.015):
        X = []

        for i, j in zip([0, 0, 1, 1], [0, 1, 0, 1]):
            for _ in range(npc):
                X.append([random.uniform(i + ((-1) ** (_ + 1)) * ruido, i + ((-1) ** _) * ruido),
                          random.uniform(j + ((-1) ** (_ + 1)) * ruido, j + ((-1) ** _) * ruido)])

        X = np.array(X)
        y = np.concatenate((np.zeros((npc, 1), dtype=int), np.ones((3*npc, 1), dtype=int)))
        y = np.reshape(y, (4*npc))

        return X, y