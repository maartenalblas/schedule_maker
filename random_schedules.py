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

import preparation
import fitness_function
import random

# instantiates the framework of the schedule
prep_schedule, slot_list = preparation.main()

# creates 10.000 random schedules
fitness_list = []
for i in range(10000):
    prep_schedule, slot_list = preparation.main()
    rand_schedule = random_schedule(prep_schedule, slot_list)
    fitness, capacity_minus, student_minus = fitness_function.main(rand_schedule)
    fitness_list.append(fitness)

print max(fitness_list)
