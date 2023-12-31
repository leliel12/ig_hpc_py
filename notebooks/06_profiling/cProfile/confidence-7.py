import math
import numpy as np

from numpy.random import random_integers as randint


def adaptive_confidence_interval(values, max_iterations=1000, alpha=0.05, trials=5, variance_threshold=0.5):
    """ Compute confidence interval using as few iterations as possible """

    try_iterations = 10

    while True:
        intervals = [confidence_interval(values, try_iterations, alpha) for _ in range(trials)]
        band_variance = np.var([upper_bound - lower_bound for lower_bound, upper_bound in intervals], ddof=1)

        print(try_iterations, band_variance)

        if band_variance < variance_threshold or try_iterations > max_iterations:
            return intervals[randint(0, trials - 1)], try_iterations

        try_iterations *= 2


def confidence_interval(values, iterations, alpha):
    """ Compute confidence interval of mean """

    subsample_means = []
    for _ in range(iterations):
        subsample_values = np.random.choice(values, size=len(values))
        subsample_means.append(np.mean(subsample_values))
    subsample_means.sort()

    lower_index = int(math.floor(iterations * (1 - alpha / 2)))
    upper_index = int(math.floor(iterations * alpha / 2))

    pivot = lambda idx: (2 * np.mean(values) - subsample_means[idx])

    return pivot(lower_index), pivot(upper_index)


def main(sample_size):
    np.random.seed(12345)
    values = randint(0, 1000, size=sample_size)
    print(np.mean(values), adaptive_confidence_interval(values))


if __name__ == '__main__':
    N = 100000
    main(N)
