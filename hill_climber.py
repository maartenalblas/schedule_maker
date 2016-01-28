import preparation
import fitness_function
import random
import csv

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

def prep_table(schedule):

    """ Prepares html table

    """
    table_data = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    blocks = ["09:00", "11:00", "13:00", "15:00"]
    for i in range(len(schedule)):
            if schedule[i].course == schedule[i-1].course and schedule[i].type == schedule[i-1].type and schedule[i].slot.id > schedule[i-1].slot.id:
                bucket = schedule[i]
                schedule[i] = schedule[i-1]
                schedule[i-1] = bucket
    for session in schedule:
        day = days[session.slot.day]
        block = blocks[session.slot.block]
        row = [session.course, session.type, day, block, session.slot.room]
        table_data.append(row)
    return table_data

def hill_climber(data, prep_schedule, slot_list, course_list):

    """ Climbs the hill stops when he is stuck

    """
    schedule = random_schedule(prep_schedule, slot_list)
    old_fitness, old_capacity_minus, old_student_minus, old_sequence_minus = fitness_function.main(schedule, course_list)
    new_fitness = 0
    # one step
    while True:
        tries = 0
        # one trie
        while True:
            tries += 1
            session_1 = random.choice(schedule)
            session_2 = random.choice(schedule)
            switch(session_1, session_2)
            new_fitness, new_capacity_minus, new_student_minus, new_sequence_minus = fitness_function.main(schedule, course_list)
            if new_fitness > old_fitness:
                break
            else:
                switch(session_1, session_2)
            if tries > 500:
                return False
        old_fitness = new_fitness
        old_capacity_minus = new_capacity_minus
        old_student_minus = new_student_minus
        old_sequence_minus = new_sequence_minus
        print "Total Fitness: " + str(old_fitness)
        print "Capacity Conflict: " + str(old_capacity_minus)
        print "Student Conflict: " + str(old_student_minus)
        print "Sequence Conflict" + str(old_sequence_minus)
        if old_student_minus == 0 and  old_capacity_minus == 0 and old_sequence_minus == 0:
            table_data = prep_table(schedule)
            return table_data, old_capacity_minus, old_student_minus, old_sequence_minus

def main(data):
    prep_schedule, slot_list, course_list = preparation.main(data)
    for i in range(100):
        table_data = hill_climber(data, prep_schedule, slot_list, course_list)
        if table_data != False:
            return table_data





# main()
