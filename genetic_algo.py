
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

def truncation(old_generation):
    fitness_list = []
    for candidate in old_generation:
        fitness_output = fitness_function.main(candidate)
        fitness = fitness_output[0]
        fitness_list.append(fitness)

    selected_generation = []
    avg_fitness = sum(fitness_list) / len(fitness_list)
    for i in range(len(fitness_list)):
        if fitness_list[i] > avg_fitness:
            selected_generation.append(old_generation[i])

    return selected_generation


def make_roulette(old_generation):

    """ Determines the probabilities of the roulette_wheel (for selection)

    """
    fitness_list = []
    for candidate in old_generation:
        fitness_output = fitness_function.main(candidate)
        fitness = fitness_output[0]
        if fitness < 0:
            fitness = 1
        fitness_list.append(fitness)

    angle = 0
    roulette_wheel = []
    for fitness in fitness_list:
        pie = (float(fitness) / float(sum(fitness_list)))
        angle += pie
        roulette_wheel.append(angle)
    return fitness_list, roulette_wheel

def selection(old_generation, roulette_wheel):

    """ Selects three parents that will create offspring (with roulette_wheel)

    """
    parents = []
    for i in range(3):
        random_value = random.random()
        for j in range(len(roulette_wheel)):
            if roulette_wheel[j] > random_value:
                parents.append(old_generation[j])
                break
    return parents


def insert_ok(session, available_slots):

    """ Returns true if timeslot of session is still available

    """
    insert_ok = False
    if session.slot.id in available_slots:
        return True
    return insert_ok

def insert_session(session, offspring, available_slots):

    """ Inserts session into offspring

    """
    offspring[session.id] = session
    available_slots.remove(session.slot.id)


def into_garage(session, offspring, garage):

    """ Inserts session into offspring and garage

    """
    offspring[session.id] = session
    garage.append(session.id)

def repair_session(session_id , offspring, garage, available_slots, slot_list):

    """ Repairs session in garage

    """
    available_slot = random.choice(available_slots)
    available_slots.remove(available_slot)
    offspring[session_id].slot = slot_list[available_slot]

def crossover(parents, slot_list):

    """ Crossover of 3 parents into 1 offspring

    """

    # makes copies of the parents
    parent_x = list(parents[0])
    parent_y = list(parents[1])
    parent_z = list(parents[2])

    # is there a crossover?
    if random.random() > crossover_rate:
        return random.choice([parent_x, parent_y, parent_z])

    # instantiates offspring
    offspring = ["" for i in range(len(parent_x))]

    # slot id's that are still available in offspring
    available_slots = [slot.id for slot in slot_list]

    # sessions that need repair
    garage = []

    repairs = 0

    # inserts all sessions in offspring and remembers which need repair
    for i in range(len(parent_x)):

        # pop session from parent  x, y and z
        index = random.randint(0, len(parent_x) - 1)
        session_x = parent_x.pop(index)
        session_y = parent_y.pop(index)
        session_z = parent_z.pop(index)

        # decides the order of insertion
        ran_value = random.random()
        if ran_value < 0.33:
            session_1 = session_x
            session_2 = session_y
            session_3 = session_z
        elif ran_value >= 0.33 and ran_value <= 0.66:
            session_1 = session_y
            session_2 = session_z
            session_3 = session_x
        else:
            session_1 = session_z
            session_2 = session_x
            session_3 = session_y

        # checks for insertion and inserts session, else into garage
        if insert_ok(session_1, available_slots):
            insert_session(session_1, offspring, available_slots)
        elif insert_ok(session_2, available_slots):
            insert_session(session_2, offspring, available_slots)
        elif insert_ok(session_3, available_slots):
            insert_session(session_3, offspring, available_slots)
        else:
            into_garage(session_1, offspring, garage)

    # repairs sessions in garage
    for session_id in garage:
        repair_session(session_id, offspring, garage, available_slots, slot_list)

    return offspring

def mutation(offspring):
    """ Mutates some genes of the offspring by switching

    """
    if random.random() < mutation_rate:
        random_1 = random.choice(offspring)
        random_2 = random.choice(offspring)
        bucket = random_1.slot
        random_1.slot = random_2.slot
        random_2.slot = bucket


def next_generation(old_generation, slot_list):

    """ Creates whole new_generation out of old_generation

    """
    new_generation = []

    # under half of population dies
    selected_generation = truncation(old_generation)
    new_generation.extend(selected_generation)

    # designs the roulette_wheel for selection
    fitness_list, roulette_wheel = make_roulette(selected_generation)
    # untill new_generation is complete
    while len(old_generation) > len(new_generation):
        # selection, crossover and mutation of parents into offspring
        parents = selection(selected_generation, roulette_wheel)
        offspring = crossover(parents, slot_list)
        mutation(offspring)
        new_generation.append(offspring)
    return new_generation


import preparation
import fitness_function
import random

global crossover_rate
global mutation_rate
global repairs

# define constants
crossover_rate = 0.7
mutation_rate = 0.1
population_size = 10
number_generations = 1000

# instantiates the framework of the schedule
prep_schedule, slot_list = preparation.main()

# creates 100 random schedules
old_generation = []
for i in range(population_size):
    prep_schedule, slot_list = preparation.main()
    rand_schedule = random_schedule(prep_schedule, slot_list)
    old_generation.append(rand_schedule)

generation = 0

fitness_total = []

# print results of algo
for i in range(number_generations):
    new_generation = next_generation(old_generation, slot_list)
    old_generation = new_generation
    fitness_list = []
    capacity_list = []
    student_list = []
    for schedule in old_generation:
        fitness, capacity_minus, student_minus = fitness_function.main(schedule)
        fitness_list.append(fitness)
        fitness_total.append(fitness)
        capacity_list.append(capacity_minus)
        student_list.append(student_minus)
    print "Generation number: " + str(generation)
    print "Av Fitness: " + str(sum(fitness_list) / len(fitness_list))
    print "Av Capacity: " + str(sum(capacity_list) / len(capacity_list))
    print "Av Student: " + str(sum(student_list) / len(student_list))
    print "Best Fitness: " + str(max(fitness_list))
    print "Best Capacity: " + str(min(capacity_list))
    print "Best Student: " + str(min(student_list))
    print "Worst Fitness: " + str(min(fitness_list))
    print "Worst Capacity: " + str(max(capacity_list))
    print "Worst Student: " + str(max(student_list))
    print ""
    generation += 1

print "Highest fitness total"
print max(fitness_total)
