import unittest
from agent import ACS2
from agent.acs2 import Constants as const


class ACS2Test(unittest.TestCase):

    def test_should_generate_initial_classifier_set(self):
        num_classifiers = 4
        general_perception = []
        for i in range(num_classifiers):
            general_perception.append(const.CLASSIFIER_WILDCARD)

        initial_classifiers = ACS2.generate_initial_classifiers(num_classifiers)
        self.assertEqual(num_classifiers, len(initial_classifiers))

        for i in range(num_classifiers):
            cls = initial_classifiers[i]
            self.assertListEqual(general_perception, cls.condition)
            self.assertListEqual(general_perception, cls.effect)
            self.assertEquals(i, cls.action)
            self.assertEquals(0.5, cls.q)
            self.assertEquals(0, cls.r)
