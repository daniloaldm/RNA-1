import copy as cp

import numpy as np


class PerceptronNN(object):

    def __init__(self, eta=0.1, epocas=50, base_treino=0.8, type_y='none', n=1):
        self.eta = eta
        self.epochs = epocas
        self.base_treino = base_treino
        self.type_y = type_y
        self.n = n

    def functionY(self, u):
        if self.type_y == 'none':
            return u
        elif self.type_y == 'logistic':
            return 1.0 / (1.0 + np.exp(-u))
        elif self.type_y == 'tanh':
            return (1.0 - np.exp(-u))/(1.0 + np.exp(-u))

    def functionYD(self, u):
        if self.type_y == 'none':
            return 1
        elif self.type_y == 'logistic':
            y = 1.0 / (1.0 + np.exp(-u))
            return y * (1.0 + y)
        elif self.type_y == 'tanh':
            y = (1.0 - np.exp(-u))/(1.0 + np.exp(-u))
            return 0.5 * (1.0 - y ** 2.0)

    def fit(self, X, y):
        self.w_ = np.ones((self.n, 1 + X.shape[1]))
        self.errors = []

        XX = np.c_[-np.ones(shape=(X.shape[0], 1)), X]
        yy = cp.deepcopy(y)
        for _ in range(self.epochs):
            erros = 0
            self.shuffle_(XX, yy) #Embaralha os dois vetores na mesma proporcao
            for xi, target in zip(XX, yy):
                y = self.predict(xi)
                e = target - self.around(y)
                att = self.eta * e * self.functionYD(y)

                # print(self.eta, end=' * ')
                # print(y, end=' * ')
                # print(e, end=' * ')
                # print(self.functionYD(y))

                # [1 -1 -1] - [-1 -1 1] = [2 0 -2]
                for i in range(len(self.w_)):
                    self.w_[i] += att[i] * xi

                for e_ in att:
                    if e_ != 0.0:

                        erros += 1

            self.errors.append(erros)

            if erros == 0:
                break

        return self

    def test(self, X, y):
        erros = 0
        hitrate = 0

        XX = np.c_[-np.ones(shape=(X.shape[0], 1)), X]
        yy = cp.deepcopy(y)
        for xi, target in zip(XX, yy):
            y = self.around(self.predict(xi))

            if np.array_equal(y.astype(int), target):
                hitrate += 1
            else:
                # print(y, end='   ==   ')
                # print(target)
                erros += 1

        return hitrate/(hitrate + erros)

    def predict(self, X):
        u = np.zeros(self.n, dtype=float)
        for i in range(len(u)):
            u[i] = self.functionY(np.dot(X, self.w_[i]))
        # u = self.around(u)
        return u

    def shuffle_(self, X, y):
        state = np.random.get_state()
        np.random.shuffle(X)
        np.random.set_state(state)
        np.random.shuffle(y)


    # dar somente 1 shuffle_ antes de usar estas funcoes
    def get_train_sample(self, K):
        return K[:int(len(K) * self.base_treino)]

    def get_test_sample(self, K):
        return K[int(len(K) * self.base_treino):]

    def around(self, predicted):
        predicted_ = cp.deepcopy(predicted)
        max_ = max(predicted_)
        for i in range(len(predicted_)):
            if predicted_[i] == max_:
                predicted_[i] = 1
            else:
                if self.type_y == 'tanh':
                    predicted_[i] = -1
                else:
                    predicted_[i] = 0

        return np.array(predicted_)