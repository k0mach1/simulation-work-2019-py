### DEPENDENCIES ###
import numpy
import random

import test_function

### CONST ###
NUM = 1000
LOOP = 1000
MAX_COUNT = 10

### CLASS ###
class Colony:
    def __init__(self, x_min, x_max, y_min, y_max, problem_num):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.position = {
            "x": random.uniform(x_min, x_max),
            "y": random.uniform(y_min, y_max)
        }
        self.count = 0
        self.problem_num = problem_num

    def update_position(self, another_colony):
        r = random.uniform(-1.0, 1.0)
        new_x = self.position["x"] + r * (self.position["x"] - another_colony.position["x"])
        new_y = self.position["y"] + r * (self.position["y"] - another_colony.position["y"])
        new_position = {"x": new_x, "y": new_y}

        if self.value(new_position) < self.value(self.position):
            self.count = 0
            self.position = new_position
        else:
            self.count += 1

    def reset_position(self, position):
        self.position = position
        self.count = 0


    def value(self, position):
        if self.problem_num == 0:
            return test_function.sphere(position)
        elif self.problem_num == 1:
            return test_function.rastrigin(position)
        elif self.problem_num == 2:
            return test_function.rosenbrock(position)
        elif self.problem_num == 3:
            return test_function.griewank(position)
        elif self.problem_num == 4:
            return test_function.alpine(position)
        elif self.problem_num == 5:
            return test_function.two_n_minima(position)

# memo: coefficient for velocity update
W = 0.5
C1 = 1.0
C2 = 1.0

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

    file = open('abc_result.txt', mode='w')

    colonies = [Colony(x_min, x_max, y_min, y_max, problem_num) for i in range(NUM)]

    for l in range(LOOP):
        # memo: employ bee
        for index in range(len(colonies)):
            colony = colonies[index]
            other_colonies = list(colonies)
            other_colonies.pop(index)
            another_colony = random.choice(other_colonies)
            colony.update_position(another_colony)

        # memo: onlooker bee
        values = [colony.value(colony.position) for colony in colonies]
        value_sum = sum(values)
        ps = []
        for colony in colonies:
            value = colony.value(colony.position)
            p = value / value_sum
            ps.append(p)
        r = random.uniform(0, 1.0)
        for index in range(len(colonies)):
            if ps[index+1] >= r:
                if ps[index] <= r:
                    colony = colonies[index]
                    other_colonies = list(colonies)
                    other_colonies.pop(index)
                    another_colony = random.choice(other_colonies)
                    colony.update_position(another_colony)
            else:
                break

        # memo: scount bee
        values = [colony.value(colony.position) for colony in colonies]
        max_value_index = numpy.argmax(values)
        min_value_index = numpy.argmin(values)
        max_value_position = colonies[max_value_index].position
        min_value_position = colonies[min_value_index].position
        for colony in colonies:
            if colony.count >= MAX_COUNT:
                r = random.uniform(0, 1.0)
                position = {
                    "x": colony.position["x"] + r * (max_value_position["x"] - min_value_position["x"]),
                    "y": colony.position["y"] + r * (max_value_position["y"] - min_value_position["y"])
                }
                colony.reset_position(position)

        # memo: update global best when one loop has ended
        values = [colony.value(colony.position) for colony in colonies]
        global_best_index    = numpy.argmin(values)
        global_best_colony   = colonies[global_best_index]
        global_best_value    = global_best_colony.value(global_best_colony.position)
        global_best_position = global_best_colony.position

        print('LOOP: {loop}  BEST SCORE : {score} BEST POSITION : {x}, {y}'.format(
            loop=l+1,
            score=global_best_value,
            x=global_best_position["x"],
            y=global_best_position["y"]
        ))

        file.write(str(global_best_value) + "\n")

    file.close()

main()