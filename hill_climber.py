
import preparation
import fitness_function
import random

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

def switch(session_1, session_2):
    """ Switches slots from 2 sessions

    """
    bucket = session_1.slot
    session_1.slot = session_2.slot
    session_2.slot = bucket


def main():
    prep_schedule, slot_list = preparation.main()
    schedule = random_schedule(prep_schedule, slot_list)

    old_fitness, old_capacity_minus, old_student_minus = fitness_function.main(schedule)
    new_fitness = 0

    for i in range(1000):
        while True:
            session_1 = random.choice(schedule)
            session_2 = random.choice(schedule)
            switch(session_1, session_2)
            new_fitness, new_capacity_minus, new_student_minus = fitness_function.main(schedule)
            if new_fitness > old_fitness:
                break
            else:
                switch(session_1, session_2)
        old_fitness = new_fitness
        old_capacity_minus = new_capacity_minus
        old_student_minus = new_student_minus

        print "fitness" + str(old_fitness)
        print "capacity" + str(old_capacity_minus)
        print "studentstr" + str(old_student_minus)

main()
