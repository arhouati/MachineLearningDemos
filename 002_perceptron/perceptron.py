import numpy as np
from matplotlib import pyplot as plt

# %matplotlib inline

X = np.array([
    [0, 0],
    [2, 0],
    [3, 0],
    [0, 2],
    [2, 2],
    [5, 1],
    [5, 2],
    [2, 4],
    [4, 4],
    [5, 5],
])

y = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1])


def perceptron_sgd(X, Y):
    w = np.zeros(len(X[0]))
    z = 0

    eta = 1
    epochs = 10
    error_count = 0

    for t in range(epochs):
        for i, x in enumerate(X):
            if (np.dot(X[i], w) * Y[i]) <= 0:
                w = w + eta * X[i] * Y[i]
                z = z + Y[i]
                error_count += 1

    return w, z, error_count


w, z, error_count = perceptron_sgd(X, y)
print("final theta : ", w)
print("final theta_0 : ", z)
print("error count : ", error_count)

for d, sample in enumerate(X):
    # Plot the negative samples
    if y[d] == -1:
        plt.scatter(sample[0], sample[1], s=120, marker='_', linewidths=2)
    # Plot the positive samples
    else:
        plt.scatter(sample[0], sample[1], s=120, marker='+', linewidths=2)

# Print a possible hyperplane, that is seperating the two classes.
# W * X  + theta_0 = 0
# w[0] * x[0] + w[1] * x[1] + theta_0 = 0
# x[1] = -(w[0] * x[0] + theta_0)/w[1]

x_1 = np.linspace(-2, 5)
x_2 = -(w[0] * x_1 + z)

plt.plot(x_1, x_2)


