# schedule_maker

The schedule_maker is build in collaboration with the schedule desk of the University of Amsterdam. This thursday I have a  meeting with them to specifiy what the exact functionality of the application will be. This depends on the problem I can solve for them and the data they can provide to me. For now I assume that the application will look like the following description:

The schedule_maker creates an optimal schedule for a university by using optimization algorithms (hill-climber, simulated-annealing, genetic). The user uploads the input (students, courses, rooms, max-capacity) in csv-files, sets his desired preferences (algorithm, runtime, etc), and runs the computation. Progress of the computation is showed by a progress bar. The output of the computation is the most optimal schedule formatted in a csv-file, this file can be downloaded by the user.

This is a sketch of the application:

![](doc/sketch.png)

The data used to test the application will be provided by the schedule desk. Now I assume that the data are csv-files that are lists of students that follow certain courses, rooms with max-capacity, and courses with number of lectures, tutorials, practicum.

The application can be seperated by the front-end and the back-end. The front-end is the html page where the user can upload the input files, set his preferences and push the go button. The back-end are the algoriths written in python that start running when the go button is pushed. So the front-end is an html page connected with the backend that is a python application. Before I know the exact functionality of the application I will work on the front-end. So I got an html page where csv-files can be uploaded and csv-files can be downloaded.

Issues that I may run into is that the problem this tool is build for is to big to solve in a reasonable time. There is a chance that finding a optimal schedule for a whole university takes to much time for the algorithm (state space to big). Therfore together with the student desk we will structure the project in such a way that it is challenging but also realistic.













