import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)


def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i - 1]) for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(1)  # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))


def plot_tour(tour):
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')  # blue circle markers, solid line style
    plt.axis('scaled')  # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)
    return tour_length(tour)


def nearest_neighbour(cities):
    start = next(iter(cities)) #start is chosen
    visited = [start]   # add start to visited
    unvisited = set(cities - {start}) # unvisited cities
    while unvisited:    # while unvisited cities
        city = return_closest_city(unvisited, visited[-1])   #get closest city meegeven: de niet bezochte steden en de laatste uit de lijst visited
        visited.append(city)    # add city to visited
        unvisited.remove(city)  # remove city from unvisited
    return visited


def return_closest_city(cities, current):
    closest_city_distance = min([distance(current, city) for city in cities - {current}])
    for city in cities:
        if distance(current, city) == closest_city_distance:
            return city

def all_segments(N):
    return [(start, start + length)
            for length in range(N,2-1,-1)
            for start in range(N - length +1)]


def remove_intersection(tour, i, j):
    A,B,C,D = tour[i-1], tour[i], tour[j-1], tour[j % len(tour)]
    if distance(A,B) + distance(C,D) > distance(A,C) + distance(B,D):
        print(tour[i:j])
        tour[i:j] = reversed(tour[i:j])



def update_tour_2opt(tour):
    original_length = tour_length(tour)
    for (start, end) in all_segments(len(tour)):
        remove_intersection(tour, start, end)
    if tour_length(tour) < original_length:
        return update_tour_2opt(tour)
    return tour

def calculate_difference_from_optimal_path(alg1, alg2):
    dist1 = plot_tsp(alg1, make_cities(10))
    dist2 = plot_tsp(alg2, make_cities(10))

    return 100 - (dist1 / dist2 * 100)

# 1A print perscentage verschil
#print(calculate_difference_from_optimal_path(try_all_tours, nearest_neighbour))

#1B
#plot_tsp(nearest_neighbour, make_cities(500))
# lengte 20582.0 in tijd 0.188 secs met random.seed(1)

#1C
# in een route met N steden zijn er N takken tussen de steden. Hoeveel er kruisen is afhankelijk van de locaties
#pseudocode
# zie code


#1D
def plot_opt2_vs_NN():
    cities = make_cities(500)
    t0 = time.process_time()
    tour = update_tour_2opt(nearest_neighbour(cities))
    t1 = time.process_time()
    plot_tour(tour)
    print("OPT2:")
    print("Afstand: ", tour_length(tour))
    print("Tijd: " , t1 - t0 , " secs")
    plot_tsp(nearest_neighbour, cities)

plot_opt2_vs_NN()


#1E
# tijdcomplexiteit: Nearest Neighbour is O((N^2)/2)
# OP2 brengt daar nog een factor N bij op omdat je nog een keer door de lijst met segmenten gaat
# #segmenten is immers gelijk aan #steden
