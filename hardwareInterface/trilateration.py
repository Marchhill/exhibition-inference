import numpy as np
from scipy.optimize import minimize


def mse(x, beacon_locations, beacon_distances):
    calculated_distances = np.array(
        [np.linalg.norm(x - beacon_locations[i]) for i in range(len(beacon_locations))])
    return np.sum(np.power(calculated_distances - beacon_distances, 2)) / len(beacon_distances)


def trilaterate(beacon_locations, beacon_distances, initial_location=np.array([0, 0, 0])):

    result = minimize(
        mse,
        initial_location,
        args=(beacon_locations, beacon_distances),
        method='L-BFGS-B',
        options={
            'ftol': 1e-5,
            'maxiter': 1e+7
        })

    return result.x


def main():
    # Testing the code
    beacon_locations = np.array(
        [[0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0]])
    # Actual location of point is at [7,4,3]
    beacon_distances = np.array([8.6, 5.83, 7.35, 9.69])
    # Result generated is [ 6.99620322  4.00005823 -2.99673958]
    print(trilaterate(beacon_locations, beacon_distances))


if __name__ == "__main__":
    main()
