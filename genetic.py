import preparation
import schedule_maker
import random
import score_function
import csv

# constants for the genetic algo
crossover_rate = 0.7
mutation_rate = 0.001

# creates a list of student and course objects in preparation file
lists = preparation.main()
student_list = lists[0]
course_list = lists[1]
session_list = lists[2]
room_list = lists[3]

# creates 100 random parent schedules
parent_list = []
for i in range(10):
    parent = schedule_maker.main(student_list, course_list, session_list, room_list)
    parent_list.append(parent)

# creates 10 generations
for i in range(10):
    # determine fitness for parents
    fitness_list = []
    for parent in parent_list:
        schedule_room_list = parent[0]
        schedule_student_list = parent[1]
        course_list = parent[2]
        score_output = score_function.main(schedule_room_list, schedule_student_list, course_list)
        fitness = score_output[0]
        fitness_list.append(fitness)

    # determine angle [0,1] of roulette wheel for selection of reproduction
    angle_list = []
    for fitness in fitness_list:
        angle = sum(angle_list) + (fitness / sum(fitness_list))
        angle_list.append(angle)

    # creates new schedules untill new generation is complete
    new_generation = []
    while True:
        # selects two parents with roulette wheel
        random_value_1 = random.random()
        for i in range(len(angle_list)):
            if angle_list[i] > random_value_1:
                parent_1 = parent_list[i]
                schedule_room_list_1 = parent_1[0]
                schedule_student_list_1 = parent_1[1]
                course_list_1 = parent_1[2]
                time_slot_list_1 = parent_1[3]
                break
        random_value_2 = random.random()
        for i in range(len(angle_list)):
            if angle_list[i] > random_value_2:
                parent_2 = parent_list[i]
                schedule_room_list_2 = parent_2[0]
                schedule_student_list_2 = parent_2[1]
                course_list_2 = parent_2[2]
                time_slot_list_2 = parent_2[3]
                break
