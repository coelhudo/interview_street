import sys
import unittest

def CityGenerator():
    identifier_counter = 1
    while True:
        city = City(identifier_counter)
        identifier_counter += 1
        yield city

def get_number_of_paths_between(city_source, city_destiny):
    def calculate_number_of_paths(city_source, city_destiny):
        number_of_paths = 0
        if city_source.has_one_way_road_to(city_destiny):
            number_of_paths += 1
        for city in city_source.destinies:
            number_of_paths += calculate_number_of_paths(city, city_destiny)
        return number_of_paths

    try:
        return calculate_number_of_paths(city_source, city_destiny)
    except Exception:
        return '\"INFINITE PATHS\"'


class City:
    def __init__(self,identifier):
        self.identifier = identifier
        self.destinies = []

    def goes_to(self, city_destiny):
        self.destinies.append(city_destiny)

    def has_one_way_road_to(self, city_destiny):
        return self.destinies.count(city_destiny)

    def get_identifier(self):
        return self.identifier

class KingdomTest(unittest.TestCase):

    def setUp(self):
        self.city_gen = CityGenerator()

    def test_one_city_identifier_creation_manually(self):
        city_one = City(1)

        self.assertNotEqual(city_one.get_identifier(), 0)
        self.assertEqual(city_one.get_identifier(), 1)

    def test_one_city_identifier_creation(self):
        city_one = self.city_gen.next()

        self.assertNotEqual(city_one.get_identifier(), 0)
        self.assertEqual(city_one.get_identifier(), 1)

    def test_two_city_identifier_creation(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()

        self.assertEqual(city_one.get_identifier(), 1)
        self.assertEqual(city_two.get_identifier(), 2)

    def test_existence_of_one_way_road_between_two_cities(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()

        city_one.goes_to(city_two)
        self.assertTrue(city_one.has_one_way_road_to(city_two))

    def test_inexistence_of_one_way_road_between_two_cities(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()

        self.assertFalse(city_one.has_one_way_road_to(city_two))

    def test_number_of_paths_from_two_cities_connected_directly(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()

        city_one.goes_to(city_two)
        self.assertTrue(city_one.has_one_way_road_to(city_two))
        self.assertEqual(get_number_of_paths_between(city_one, city_two), 1)

    def test_number_of_paths_from_two_cities_connected_indirectly(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()
        city_three = self.city_gen.next()

        city_one.goes_to(city_two)
        city_two.goes_to(city_three)

        self.assertTrue(city_one.has_one_way_road_to(city_two))
        self.assertEqual(get_number_of_paths_between(city_one, city_two), 1)
        self.assertTrue(city_two.has_one_way_road_to(city_three))
        self.assertEqual(get_number_of_paths_between(city_two, city_three), 1)
        self.assertFalse(city_one.has_one_way_road_to(city_three))
        self.assertEqual(get_number_of_paths_between(city_one, city_three), 1)

    def test_number_of_paths_from_two_cities_connected_directly_and_indirectly(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()
        city_three = self.city_gen.next()
        city_four = self.city_gen.next()

        city_one.goes_to(city_two)
        city_one.goes_to(city_four)
        city_two.goes_to(city_three)
        city_two.goes_to(city_four)
        city_three.goes_to(city_four)

        self.assertEqual(get_number_of_paths_between(city_one, city_four), 3)

    def test_infinity_paths(self):
        city_one = self.city_gen.next()
        city_two = self.city_gen.next()

        city_one.goes_to(city_two)
        city_two.goes_to(city_one)
        self.assertEqual(get_number_of_paths_between(city_one, city_two), '\"INFINITE PATHS\"')

if __name__ == '__main__':
    unittest.main()

    # number_of_cities_and_roads = raw_input('Insert Number of Cities and Roads\n')
    # cities = int(number_of_cities_and_roads[0])
    # roads = int(number_of_cities_and_roads[2])
