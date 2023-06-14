import sys
import random
import numpy as np
import datetime


sys.path.append('.')
import unittest
import data_mock.mock_helpers.utils as utils


class TestResults(unittest.TestCase):

    def test_means(self):
        data = [1, 2, 3, 4, 1, 3]
        reshuf = utils.resample(data)
        self.assertEqual(len(data), len(reshuf))

    def test_scores_ex(self):
        s_size = 100
        scores =  [random.randint(1,100) for x in range(s_size)]
        sample_of_means = []
        for i in range(200):
            reshuf = utils.resample(scores)
            sample_of_means.append(np.mean(reshuf))
        sample_of_means = sorted(sample_of_means)
        first_05 = int(round(.05 * len(sample_of_means)))
        first_95 = int(round(.95 * len(sample_of_means)))
        lower = sample_of_means[first_05]
        upper = sample_of_means[first_95]

    def users_ex(self):
        data = [
        ['name', '2023-01-10' ],
        ['name', '2023-01-10' ],
                ]




if __name__ == '__main__':
    unittest.main()
