
def random_schedule(rand_schedule, slot_list):

    """ Assigns random slot to every session

    """
    #
    copy_list = list(slot_list)
    for session in rand_schedule:
        slot = random.choice(copy_list)
        session.slot = slot
        copy_list.remove(slot)
    return rand_schedule

def make_roulette(old_generation):

    """ Determines the probabilities of the roulette_wheel (for selection)

    """
    fitness_list = []
    for candidate in old_generation:
        fitness_output = fitness_function.main(candidate)
        fitness = fitness_output[0]
        fitness_list.append(fitness)

    angle = 0
    roulette_wheel = []
    for fitness in fitness_list:
        pie = (float(fitness) / float(sum(fitness_list)))
        angle += pie
        roulette_wheel.append(angle)
    return fitness_list, roulette_wheel


def selection(old_generation, roulette_wheel):

    """ Selects two parents that will create offspring (with roulette_wheel)

    """
    parents = []
    for i in range(2):
        random_value = random.random()
        for j in range(len(roulette_wheel)):
            if roulette_wheel[j] > random_value:
                parents.append(old_generation[j])
                break
    return parents


def crossover(parents, slot_list):

    """ Crossover of genes of parents into offspring

    """
    # makes copies of the parents
    parent_x = list(parents[0])
    parent_y = list(parents[1])

    # makes copies of slot_list to check for empty slots
    slot_list_x = list(slot_list)
    slot_list_y = list(slot_list)

    # instantiates offspring
    offspring_x = []
    offspring_y = []

    # instantiates garage
    garage_x = []
    garage_y = []

    # switches between x => x, y => y to x => y, y => x
    direction = "straight"

    # empties all sessions of parents into offspring and garage
    for i in range(len(parent_x)):
        # selects random session from parent x and y (different timeslot)
        index = random.randint(0, len(parent_x) - 1)
        random_session_x = parent_x[index]
        random_session_y = parent_y[index]

        # tries straight first, diagonal second, single straight third, single diagonal fourth
        if direction == "straight":
            straight_ok, straight_x_ok, straight_y_ok = is_straight_ok(offspring_x, offspring_y, random_session_x, random_session_y)
            if straight_ok:
                straight_switch(parent_x, parent_y, offspring_x, offspring_y, random_session_x, random_session_y)
                del slot_list_x[index]
                del slot_list_y[index]
            else:
                diagonal_ok, diagonal_x_ok, diagonal_y_ok = is_diagonal_ok(offspring_x, offspring_y, random_session_x, random_session_y)
                if diagonal_ok:
                    diagonal_switch(parent_x, parent_y, offspring_x, offspring_y, random_session_x, random_session_y, direction)
                    del slot_list_x[index]
                    del slot_list_y[index]
                else:
                    if straight_x_ok:
                        single_switch(parent_x, offspring_x, random_session_x)
                        into_garage(parent_y, garage_y, random_session_y)
                        del slot_list_x[index]
                    elif straight_y_ok:
                        single_switch(parent_y, offspring_y, random_session_y)
                        into_garage(parent_x, garage_x, random_session_x)
                        del slot_list_y[index]
                    else:
                        if diagonal_x_ok:
                            single_switch(parent_x, offspring_y, random_session_x)
                            into_garage(parent_y, garage_x, random_session_y)
                            del slot_list_x[index]
                        elif diagonal_y_ok:
                            single_switch(parent_y, offspring_x, random_session_y)
                            into_garage(parent_x, garage_y, random_session_x)
                            del slot_list_y[index]
                        else:
                            into_garage(parent_x, garage_x, random_session_x)
                            into_garage(parent_y, garage_y, random_session_y)
            direction = "diagonal"

        # tries diagonal first, straight second, single diagonal third, single straight fourth
        else:
            diagonal_ok, diagonal_x_ok, diagonal_y_ok = is_diagonal_ok(offspring_x, offspring_y, random_session_x, random_session_y)
            if diagonal_ok:
                diagonal_switch(parent_x, parent_y, offspring_x, offspring_y, random_session_x, random_session_y)
                del slot_list_x[index]
                del slot_list_y[index]
            else:
                straight_ok, straight_x_ok, straight_y_ok = is_straight_ok(offspring_x, offspring_y, random_session_x, random_session_y)
                if straight_ok:
                    straight_switch(parent_x, parent_y, offspring_x, offspring_y, random_session_x, random_session_y)
                    del slot_list_x[index]
                    del slot_list_y[index]
                else:
                    if diagonal_x_ok:
                        single_switch(parent_x, offspring_y, random_session_x)
                        into_garage(parent_y, garage_x, random_session_y)
                        del slot_list_x[index]
                    elif diagonal_y_ok:
                        single_switch(parent_y, offspring_x, random_session_y)
                        into_garage(parent_x, garage_y, random_session_x)
                        del slot_list_y[index]
                    else:
                        if straight_x_ok:
                            single_switch(parent_x, offspring_x, random_session_x)
                            into_garage(parent_y, garage_y, random_session_y)
                            del slot_list_x[index]
                        elif straight_y_ok:
                            single_switch(parent_y, offspring_y, random_session_y)
                            into_garage(parent_x, garage_x, random_session_x)
                            del slot_list_y[index]
                        else:
                            into_garage(parent_x, garage_y, random_session_x)
                            into_garage(parent_y, garage_x, random_session_y)
            direction = "straight"

    # assign empty timeslot to the sessions in garages
    for session in garage_x:
        empty_slot = random.choice(slot_list_x)
        session.slot = empty_slot
        slot_list_x.remove(empty_slot)
    for session in garage_y:
        empty_slot = random.choice(slot_list_y)
        session.slot = empty_slot
        slot_list_x.remove(empty_slot)

    # Error checking
    if len(offspring_x) == len(parent_x) or len(offspring_x) == len(parent_x):
        print "!!!! Lenght of solution is not good !!!!!!"

    return offspring_x, offspring_y



def is_straight_ok(offspring_x, offspring_y, random_session_x, random_session_y):

    """ returns if straight switches can be done

    """
    straight_ok = True
    straight_x_ok = True
    straight_y_ok = True

    for session in offspring_x:
        if random_session_x is session:
            straight_ok = False
            straight_x_ok = False
    for session in offspring_y:
        if random_session_y is session:
            straight_ok = False
            straight_y_ok = False
    return straight_ok, straight_x_ok, straight_y_ok

def is_diagonal_ok(offspring_x, offspring_y, random_session_x, random_session_y):

    """ returns if straight switches can be done

    """
    diagonal_ok = True
    diagonal_x_ok = True
    diagonal_y_ok = True

    for session in offspring_x:
        if random_session_y is session:
            diagonal_ok = False
            diagonal_x_ok = False
    for session in offspring_y:
        if random_session_x is session:
            diagonal_ok = False
            diagonal_y_ok = False
    return diagonal_ok, diagonal_x_ok, diagonal_y_ok

def straight_switch(parent_x, parent_y, offspring_x, offspring_y, random_session_x, random_session_y):

    """ Does straight switch

    """
    parent_x.remove(random_session_x)
    offspring_x.append(random_session_x)
    parent_y.remove(random_session_y)
    offspring_y.append(random_session_y)


def diagonal_switch(parent_x, parent_y, offspring_x, offspring_y, random_session_x, random_session_y):

    """ Does diagonal switch

    """
    parent_x.remove(random_session_x)
    offspring_x.append(random_session_x)
    parent_y.remove(random_session_y)
    offspring_y.append(random_session_y)


def single_switch(parent, offspring, random_session, slot_list):

    """ Does single switch

    """
    parent.remove(random_session)
    offspring.append(random_session)

def into_garage(parent, garage, random_session):

    """ switches session into garage for later use

    """
    parent.remove(random_session)
    garage.append(random_session)


def mutation(offspring):
    """ Mutates some genes of the offspring by switching

    """
    if random.random() > 0.1:

        random_1 = random.choice(offspring)
        random_2 = random.choice(offspring)

        bucket = random_1.slot
        random_1.slot = random_2.slot
        random_2.slot = bucket

    return offspring

def next_generation(old_generation, slot_list):

    """ Creates whole new_generation out of old_generation

    """
    new_generation = []

    # designs the roulette_wheel for selection
    fitness_list, roulette_wheel = make_roulette(old_generation)

    # untill new_generation is complete
    while len(old_generation) > len(new_generation):
        # selection, crossover and mutation of parents into offspring
        parents = selection(old_generation, roulette_wheel)
        offspring_x, offspring_y = crossover(parents, slot_list)
        mutated_x = mutation(offspring_x)
        mutated_y = mutation(offspring_y)
        new_generation.append(mutated_x)
        new_generation.append(mutated_y)
    return new_generation

"""

"""

import preparation
import fitness_function
import random
import csv

# define constants for the algo
# crossover_rate = 0.7
# mutation_rate = 0.001

# instantiates the framework of the schedule
prep_schedule, slot_list = preparation.main()

# creates 10 random schedules
old_generation = []
for i in range(100):
    prep_schedule, slot_list = preparation.main()
    rand_schedule = random_schedule(prep_schedule, slot_list)
    old_generation.append(rand_schedule)

generation = 0

# print results of algo
for i in range(1000):
    new_generation = next_generation(old_generation, slot_list)
    old_generation = new_generation
    fitness_list = []
    capacity_list = []
    student_list = []
    for schedule in old_generation:
        fitness, capacity_minus, student_minus = fitness_function.main(schedule)
        fitness_list.append(fitness)
        capacity_list.append(capacity_minus)
        student_list.append(student_minus)
    print "Generation number: " + str(generation)
    print "Av Fitness: " + str(sum(fitness_list) / len(fitness_list))
    print "Av Capacity: " + str(sum(capacity_list) / len(capacity_list))
    print "Av Student: " + str(sum(student_list) / len(student_list))
    print "Best Fitness: " + str(max(fitness_list))
    print "Best Capacity: " + str(min(capacity_list))
    print "Best Student: " + str(min(student_list)) 
    generation += 1
