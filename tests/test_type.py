import unittest
from Engine.type import Type, TypeChart, string_to_type


class TestTypeChart(unittest.TestCase):
    def setUp(self):
        self.type_chart = TypeChart()

    def test_get_weaknesses(self):
        self.assertEqual(self.type_chart.get_weaknesses(Type.FIRE), [Type.WATER, Type.ROCK, Type.GROUND])
        self.assertEqual(self.type_chart.get_weaknesses(Type.WATER), [Type.ELECTRIC, Type.GRASS])

    def test_get_resistances(self):
        self.assertEqual(self.type_chart.get_resistances(Type.FIRE),
                         [Type.FIRE, Type.GRASS, Type.ICE, Type.BUG, Type.STEEL, Type.FAIRY])
        self.assertEqual(self.type_chart.get_resistances(Type.WATER), [Type.WATER, Type.FIRE, Type.ICE, Type.STEEL])

    def test_get_immunities(self):
        self.assertEqual(self.type_chart.get_immunities(Type.NORMAL), [Type.GHOST])
        self.assertEqual(self.type_chart.get_immunities(Type.GROUND), [Type.ELECTRIC])

    def test_get_type_effectiveness(self):
        self.assertEqual(self.type_chart.get_type_effectiveness(Type.FIRE, Type.WATER), 0.5)
        self.assertEqual(self.type_chart.get_type_effectiveness(Type.WATER, Type.FIRE), 2.0)
        self.assertEqual(self.type_chart.get_type_effectiveness(Type.ELECTRIC, Type.GROUND), 0.0)

    def test_string_to_type_converts(self):
        self.assertEqual(string_to_type("fire"), Type.FIRE)
        self.assertEqual(string_to_type("Water"), Type.WATER)
        self.assertEqual(string_to_type("BUG"), Type.BUG)

    def test_string_to_type_throws(self):
        with self.assertRaises(ValueError):
            string_to_type("bla")
            string_to_type("")


if __name__ == '__main__':
    unittest.main()
