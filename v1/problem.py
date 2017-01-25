from math import sqrt
from errors import StateError
import copy
class City:
    """
    A city within the graph of cities
    """
    def __init__(self):
        self.x_position = 0
        self.y_position = 0
        self.adjacent_cities = []
        
    def distance_to_city(self, city):
        """
        The straight line distance from self to city
        """
        if not self.adjacent_cities:
            raise StateError("Uninitialized City instance")
            
        delta_x = self.x_position - city.x_position
        delta_y = self.y_position - city.y_position
        return sqrt(delta_x**2 + delta_y**2)
        
        
class Package:
    """
    A package which requires delivering, with a source and destination
    """
    def __init__(self):
        self.source = None
        self.destination = None
        self.vehicle = None
        self.is_at_destination = False
        
    def location(self):
        """
        The current location of the package
        """
        if self.source == None or self.destination == None:
            raise StateError("Uninitialized Package instance")
        
        if self.is_at_destination:
            return self.destination
        elif self.vehicle:
            return self.vehicle.current_city
        else:
            return self.source
            
    def estimated_distance_to_destination(self):
        """
        Helper method which returns the straight line distance from the 
        package's current location to its destination.
        """
        if self.is_at_destination:
            return 0
        
        position = self.location()
        delta_x = position.x_position - self.destination.x_position
        delta_y = position.y_position - self.destination.y_position
        return sqrt(delta_x**2 + delta_y**2) 
        
            
class Vehicle:
    """
    A vehicle which picks up and drops off packages
    """
    def __init__(self):
        self.package = None
        self.current_city = None
        
    def estimated_distance_to_garage(self, garage_city):
        """
        Helper method which returns the straight line distance from the 
        vehicle's current location to the provided garage_city.
        """
        if not self.current_city:
            raise StateError("Uninitialized Vehicle instance")
            
        delta_x = self.current_city.x_position - garage_city.x_position
        delta_y = self.current_city.y_position - garage_city.y_position
        return sqrt(delta_x**2 + delta_y**2)  
        
        
class ProblemState:
    """
    The variable state of the problem, including the all vehicles, packages and
    the total distance traveled from the start state to reach this state.
    """
    def __init__(self):
        self.vehicles = []
        self.packages = []
        self.distance_traveled = 0
        self.garage_city = None # required for the comparator function
        
    def __cmp__(self, other):
        """
        Comparator function for use with the heapq. To make this comply with
        A* this will be self.distance_traveled + the heuristic value
        """
        if not self.garage_city or not self.vehicles or not self.packages:
            raise StateError("Uninitialized State instance")
            
        a_star_value = self.distance_traveled + heuristic(self)
        other_a_star = other.distance_traveled + heuristic(other)
        
        return a_star_value > other_a_star
        
        
def heuristic(state):
    """
    A heuristic which estimates the travel distance required to get from the
    provided state, to the goal state. Is comprised of the sum of:
        - The total straight line distance between each package's location() and
          its destination.
        - The total straight line distance between all vehicles and the
          garage_city.
    """
    h_value = 0
    for package in state.packages:
        h_value += package.estimated_distance_to_destination()
    
    for vehicle in state.vehicles:
        h_value += vehicle.estimated_distance_to_garage(state.garage_city)
        
    return h_value


def transition_operator(state):
    """
        A method that will recieve as an input the current state of the problem
        and will output all the possible states resulting from the current 
        state as a priority queue based 
    """
    resulting_possible_states=[]
    initial_state = state.copy.deepcopy(state)
    for vehicle in state.vehicles:
        for package in packages:
            if package.source == vehicle.current_city and package.vehicle == None and package.is_at_destination == False:
                package.vehicle == vehicle
        for city in vehicle.current_city.adjacent_cities:
            initial_city = copy.deepcopy(vehicle.current_city)
            vehicle.current_city = city
            resulting_possible_states.append(copy.deepcopy(state))
        state = initial_state
            
    
    