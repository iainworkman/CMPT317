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
        if not self.source or not self.destination:
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

    def __str__(self):
        s = "source: ({source_x}, {source_y}), destination=({dest_x}, {dest_y}), at_destination={at_home}, vehicle={vehicle}"
        return s.format(source_x=self.source.x_position, source_y=self.source.y_position,
                        dest_x=self.destination.x_position, dest_y=self.destination.y_position,
                        at_home=self.is_at_destination, vehicle=self.vehicle)


class Vehicle:
    """
    A vehicle which picks up and drops off packages
    """
    def __init__(self):
        self.name = -1
        self.packages = []
        self.current_package = 0
        self.has_package = False
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

    def can_pickup(self):
        if self.has_package or not self.packages or len(self.packages) == self.current_package:
            return False
            
        current = self.packages[self.current_package]
        return (not current.is_at_destination) and (current.source.x_position == self.current_city.x_position) and (current.source.y_position == self.current_city.y_position)

    def can_dropoff(self):
        if not self.has_package or not self.packages:
            return False
            
        current = self.packages[self.current_package]
        return self.current_city.x_position == current.destination.x_position and self.current_city.y_position == current.destination.y_position

    def __str__(self):
        s = """Name: {name}, current_city: ({x_cord}, {y_cord}),
        have_package: {have_package}\n\tPackages: {packages}"""
        
        return s.format(name=self.name, x_cord=self.current_city.x_position, y_cord=self.current_city.y_position,
                  have_package=self.has_package, packages=self.packages)
                  

class ProblemState:
    """
    The variable state of the problem, including the vehicle and
    the total distance traveled from the start state to reach this state.
    """
    def __init__(self):
        self.vehicle = None
        self.distance_traveled = 0
        self.garage_city = None # required for the comparator function

    def is_goal_state(self):
        return (
            self.vehicle.current_package == len(self.vehicle.packages)
        ) and (
            self.vehicle.current_city.x_position == self.garage_city.x_position
        ) and (
            self.vehicle.current_city.y_position == self.garage_city.y_position
        )

    def __cmp__(self, other):
        """
        Comparator function for use with the heapq. To make this comply with
        A* this will be self.distance_traveled + the heuristic value
        """
        if not self.garage_city or not self.vehicle:
            raise StateError("Uninitialized State instance")

        a_star_value = self.distance_traveled + heuristic(self)
        other_a_star = other.distance_traveled + heuristic(other)

        if a_star_value > other_a_star:
            return 1
        elif a_star_value == other_a_star:
          return 0
        else:
            return -1

    def __str__(self):
        """
        A readable version of this state
        """
        s = "Current_Position: (%s, %s)\n" % (self.vehicle.current_city.x_position, self.vehicle.current_city.y_position)
        s += "Has Package: %s\n" % self.vehicle.has_package
        s += "Packages: %s\n" % [str(p) for p in self.vehicle.packages]
        s += "Distance Travelled: %s\n" % self.distance_traveled
        s += "Garage: (%s, %s)\n" % (self.garage_city.x_position, self.garage_city.y_position)
        s += "h(x): (%s)\n" % (heuristic(self))
        return s


def heuristic(state):
    """
    A heuristic which estimates the travel distance required to get from the
    provided state, to the goal state. Is comprised of the sum of:
        - The straight line distance of current vehicle's distance from
            completing all of its package deliveries and moving to the garage.
    """
    h_value = 0
    # If the truck does not currently have a package, we need to add the distance from the truck to that package.
    if not state.vehicle.has_package and not state.vehicle.current_package == len(state.vehicle.packages):
        destination = state.vehicle.packages[state.vehicle.current_package].source
        delta_x = destination.x_position - state.vehicle.current_city.x_position
        delta_y = destination.y_position - state.vehicle.current_city.y_position
        h_value += sqrt(delta_x**2 + delta_y**2)

    for i in range(state.vehicle.current_package, len(state.vehicle.packages)):
        h_value += state.vehicle.packages[i].estimated_distance_to_destination()

        if i+1 < len(state.vehicle.packages):
            h_value += state.vehicle.packages[i].destination.distance_to_city(
                state.vehicle.packages[i+1].source
            )

    for package in state.vehicle.packages:
        h_value += package.estimated_distance_to_destination()

    # Add in the distance to garage.
    if not state.vehicle.has_package and not state.vehicle.current_package == len(state.vehicle.packages):
        destination = state.vehicle.packages[len(state.vehicle.packages) - 1].destination
        delta_x = destination.x_position - state.garage_city.x_position
        delta_y = destination.y_position - state.garage_city.y_position
        h_value += sqrt(delta_x**2 + delta_y**2)
    else:
        h_value += state.vehicle.estimated_distance_to_garage(state.garage_city)

    return h_value


def transition_operator(state):
    """
        A method that will recieve as an input the current state of the problem
        and will output all the possible states resulting from the current
        state.
    """
    possible_states=[]

    """
        Creating possible states for travelling to each adjacent city
    """
    for city in state.vehicle.current_city.adjacent_cities:
        new_city_state = copy.deepcopy(state)
        distance_to_travel = state.vehicle.current_city.distance_to_city(city)
        new_city_state.vehicle.current_city = city
        new_city_state.distance_traveled = new_city_state.distance_traveled + distance_to_travel

        possible_states.append(new_city_state)

    """
        Possible state for packge pick up
    """
    # if state.vehicle.current_city == state.vehicle.packages[state.vehicle.current_package].source and not state.vehicle.has_package:
    if state.vehicle.can_pickup():
        new_pick_up_state = copy.deepcopy(state)
        new_pick_up_state.vehicle.packages[new_pick_up_state.vehicle.current_package].vehicle = new_pick_up_state.vehicle
        new_pick_up_state.vehicle.has_package = True
        possible_states.append(new_pick_up_state)

    """
        Possible state for packge drop off
    """
    # if state.vehicle.current_city == state.vehicle.packages[state.vehicle.current_package].destination and state.vehicle.has_package:
    if state.vehicle.can_dropoff():
        new_drop_off_state = copy.deepcopy(state)
        new_drop_off_state.vehicle.packages[new_drop_off_state.vehicle.current_package].vehicle = None
        new_drop_off_state.vehicle.packages[new_drop_off_state.vehicle.current_package].is_at_destination = True
        new_drop_off_state.vehicle.has_package = False
        new_drop_off_state.vehicle.current_package += 1

        possible_states.append(new_drop_off_state)

    return possible_states
