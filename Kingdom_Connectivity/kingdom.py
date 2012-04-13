import sys

def get_number_of_paths_between(city_source, city_destiny):

    class InfinitePathsException:
        pass
    #city_destiny will always be the max identifier, no need to strongly identify cicles
    max_connections = 1
    for i in range(1, city_destiny.get_identifier()+1):
        max_connections = i * max_connections
    max_connections = max_connections
    variable = {'counter' : 0 } #ugly but it works, simulation nonlocal feature
    def calculate_number_of_paths(city_source, city_destiny):
        variable['counter'] += 1
        if variable['counter'] > max_connections + 1:
            raise InfinitePathsException
        number_of_paths = 0
        if city_source.has_one_way_road_to(city_destiny):
            number_of_paths += 1
        for city in city_source.get_destinies():
            number_of_paths += calculate_number_of_paths(city, city_destiny)
        return number_of_paths

    try:
        return calculate_number_of_paths(city_source, city_destiny)
    except InfinitePathsException:
        return 'INFINITE PATHS'


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

    def get_destinies(self):
        return self.destinies

if __name__ == '__main__':
    number_of_cities_and_roads = raw_input()
    max_cities = int()
    roads = int()
    if number_of_cities_and_roads[0].isdigit():
        max_cities = int(number_of_cities_and_roads[0])
    if number_of_cities_and_roads[2].isdigit():
        roads = int(number_of_cities_and_roads[2])

    cities = {}

    for i in range(1,roads+1):
        first_and_second_cities = raw_input()
        first_city_identifier = int(first_and_second_cities[0])
        second_city_identifier = int(first_and_second_cities[2])
        if not first_city_identifier in cities:
            cities[first_city_identifier] = City(first_city_identifier)
        if not second_city_identifier in cities:
            cities[second_city_identifier] = City(second_city_identifier)

        cities[first_city_identifier].goes_to(cities[second_city_identifier])

    if len(cities):
        print get_number_of_paths_between(cities[1], cities[max_cities])
