### DEPENDENCIES ###
import math
import numpy
import random

import test_function

### CONST ###
NUM = 100
LOOP = 1000

### CLASS ###
class Particle:
    def __init__(self, x_min, x_max, y_min, y_max, problem_num):
        position = {
            "x": random.uniform(x_min, x_max),
            "y": random.uniform(y_min, y_max)
        }
        self.position = position
        self.best_position = position
        self.velocity = {
            "x": 0.0,
            "y": 0.0
        }
        self.problem_num = problem_num

    def update_position(self):
        new_x = self.position["x"] + self.velocity["x"]
        new_y = self.position["y"] + self.velocity["y"]
        self.position = {"x": new_x, "y": new_y}

    def update_velocity(self, global_best_position):
        w  = 0.5
        c1 = 1.0
        c2 = 1.0
        r1 = random.uniform(0, 1.0)
        r2 = random.uniform(0, 1.0)
        new_x = w * self.velocity["x"] + c1 * r1 * (self.best_position["x"] - self.position["x"]) + c2 * r2 * (global_best_position["x"] - self.position["x"])
        new_y = w * self.velocity["y"] + c1 * r1 * (self.best_position["y"] - self.position["y"]) + c2 * r2 * (global_best_position["y"] - self.position["y"])
        self.velocity = {"x": new_x, "y": new_y}

    def update_best_position(self):
        if self.value() < self.best_value():
            self.best_position = self.position

    def value(self):
        if self.problem_num == 0:
            return test_function.sphere(self.position)
        elif self.problem_num == 1:
            return test_function.rastrigin(self.position)
        elif self.problem_num == 2:
            return test_function.rosenbrock(self.position)
        elif self.problem_num == 3:
            return test_function.griewank(self.position)
        elif self.problem_num == 4:
            return test_function.alpine(self.position)
        elif self.problem_num == 5:
            return test_function.two_n_minima(self.position)

    def best_value(self):
        if self.problem_num == 0:
            return test_function.sphere(self.best_position)
        elif self.problem_num == 1:
            return test_function.rastrigin(self.best_position)
        elif self.problem_num == 2:
            return test_function.rosenbrock(self.best_position)
        elif self.problem_num == 3:
            return test_function.griewank(self.best_position)
        elif self.problem_num == 4:
            return test_function.alpine(self.best_position)
        elif self.problem_num == 5:
            return test_function.two_n_minima(self.best_position)


### FUNCTIONS ###
def main():
    # memo: confirm problem number
    print("[0] Sphere\n[1] Rastrigin\n[2] Rosenbrock\n[3] Griewank\n[4] Alpine\n[5] 2^n minima")
    problem_num = int(input("Please Enter Problem Number: "))

    # memo: define x and y domain
    if problem_num == 0 or problem_num == 1 or problem_num == 5:
        x_min = -5.0
        x_max = 5.0
        y_min = -5.0
        y_max = 5.0
    elif problem_num == 2:
        x_min = -5.0
        x_max = 10.0
        y_min = -5.0
        y_max = 10.0
    elif problem_num == 3:
        x_min = -600.0
        x_max = 600.0
        y_min = -600.0
        y_max = 600.0
    elif problem_num == 4:
        x_min = -10.0
        x_max = 10.0
        y_min = -10.0
        y_max = 10.0
    else:
        print("wrong input")
        return

    file = open('pso_result.txt', mode='w')

    particles = [Particle(x_min, x_max, y_min, y_max, problem_num) for i in range(NUM)]
    personal_best_values = [particle.best_value() for particle in particles]
    global_best_index = numpy.argmin(personal_best_values)
    global_best_position = particles[global_best_index].best_position

    for l in range(LOOP):
        for particle in particles:
            particle.update_position()
            particle.update_velocity(global_best_position)
            particle.update_best_position()

        # memo: update global best when one loop has ended
        personal_best_values = [particle.best_value() for particle in particles]
        global_best_index    = numpy.argmin(personal_best_values)
        global_best_value    = particles[global_best_index].best_value()
        global_best_position = particles[global_best_index].best_position

        print('LOOP: {loop}  BEST SCORE : {value} BEST POSITION : {x}, {y}'.format(
            loop=l,
            value=global_best_value,
            x=global_best_position["x"],
            y=global_best_position["y"]
        ))

        file.write(str(global_best_value) + "\n")

    file.close()

main()