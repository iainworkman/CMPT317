import math

from problem import ProblemState, City
from errors import ArgumentError

def generate_graph(number_of_nodes):
    """
    Return a graph of cities, organized in a grid, of the provided size
    """
    cities = []
    size = int(math.sqrt(number_of_nodes))
    if size*size != number_of_nodes:
        raise ArgumentError("At the moment generate_graph() only takes perfect squares (3, 16, 25 etc.). Feel free to improve it.")
    test = 0
    for position in range(0, number_of_nodes):
        city = City()
        city.x_position = (position) % size
        city.y_position = int(position / size)
        cities.append(city)
        
    for i_city in range(0, len(cities)):
        city = cities[i_city]
        x_pos = city.x_position
        y_pos = city.y_position
        
        if x_pos != 0:
            city.adjacent_cities.append(cities[i_city - 1])
            
        if x_pos != size-1:
            city.adjacent_cities.append(cities[i_city + 1])
            
        if y_pos != 0:
            city.adjacent_cities.append(cities[i_city - size])
            
        if y_pos != size-1:
            city.adjacent_cities.append(cities[i_city + size])
            
    return cities
    

def main():
    """
    Main Function. Just sets up the data, for now.
    """
    cities = None
    
    garage_city = None
    
    cities = generate_graph(25)
    for city in cities:
        print city.x_position,
        print city.y_position,
        print '[',
        for adjacent_city in city.adjacent_cities:
            print '(' + str(adjacent_city.x_position) + ', ' + str(adjacent_city.y_position) + ')',
        print ']'
        
    start_state = ProblemState()
    # Todo: Initialize start state
    
    

if __name__ == '__main__':
    main()