import keyboard
from time import sleep
from random import randint


class Snake:
    def __init__(self, init_body, init_direction):
        self.body = init_body
        self.direction = init_direction

    def take_step(self,position):
        self.body.append(position)  # Setting a new head position
        self.body.pop(0)  # Remove the tail

    def extend_body(self):
        tail = self.body[0]
        y = 0
        x = 0
        if self.direction == "UP":
            y = 1
        elif self.direction == "DOWN":
            y = -1
        elif self.direction == "LEFT":
            x += 1
        elif self.direction == "RIGHT":
            x -= 1
        self.body.insert(0, (tail[0]+y, tail[1]+x))

    def set_direction(self,direction):
        self.direction = direction

    def head(self):
        return self.body[-1]


class Apple:
    def __init__(self, points_per_apple):
        self.apple_exist = False
        self.points_per_apple = points_per_apple
        self.apple_pos = None

    def set_points(self, points):
        self.points_per_apple = points

    def apple_eaten(self):
        self.apple_exist = False
        self.apple_pos = None


class Game:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.points = 0

        self.board = []
        self.snake = Snake([(0, 0), (1, 0), (2, 0), (3, 0)], "DOWN")
        self.apple = Apple(1)

    def create_board(self, width, height):
        self.width = width
        self.height = height
        self.board = [[] for i in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.board[y].append(" ")

    def render(self):
        print("+" + ("-" * self.width) + "+")
        for y, row in enumerate(self.board):
            formatted_row = row.copy()
            for x, v in enumerate(formatted_row):
                if (y, x) == self.snake.head():
                    formatted_row[x] = "X"
                elif (y, x) in self.snake.body:
                    formatted_row[x] = "O"
                elif (y, x) == self.apple.apple_pos:
                    formatted_row[x] = "*"
            print("|" + "".join(formatted_row) + "|")
        print("+" + ("-" * self.width) + "+")

    # Apple spawning system
    def __create_spawn_point(self):
        spawn_x = randint(0, self.width-1)
        spawn_y = randint(0, self.height-1)
        spawn_point = (spawn_y, spawn_x)
        return spawn_point

    def spawn_apple(self):
        if self.apple.apple_exist:
            return
        spawn_point = self.__create_spawn_point()
        while spawn_point in self.snake.body:
            spawn_point = self.__create_spawn_point()
        self.apple.apple_pos = spawn_point
        self.apple.apple_exist = True

    # Snake system
    def check_hit(self):
        for i in self.snake.body:
            if self.snake.body.count(i) > 1:
                print("The snake hits its own body!")
                print("Game Over!")
                return True
        return False

    def out_of_bound(self):
        head = self.snake.head()
        if head[0] >= self.height or head[0] < 0:
            print("Out Of Bounds!")
            print("Game Over!")
            return True
        elif head[1] >= self.width or head[1] < 0:
            print("Out Of Bounds!")
            print("Game Over!")
            return True
        return False

    def check_if_found_apple(self):
        if self.snake.head() == self.apple.apple_pos:
            self.points += self.apple.points_per_apple
            self.apple.apple_eaten()
            self.snake.extend_body()

    def move_snake(self):
        while True:
            head_pos = self.snake.head()
            if keyboard.is_pressed("w"):
                self.snake.set_direction("UP")
                self.snake.take_step((head_pos[0]-1, head_pos[1]))
                break
            elif keyboard.is_pressed("s"):
                self.snake.set_direction("UP")
                self.snake.take_step((head_pos[0]+1, head_pos[1]))
                break
            elif keyboard.is_pressed("a"):
                self.snake.set_direction("UP")
                self.snake.take_step((head_pos[0], head_pos[1]-1))
                break
            elif keyboard.is_pressed("d"):
                self.snake.set_direction("UP")
                self.snake.take_step((head_pos[0], head_pos[1]+1))
                break


A = Game()
A.create_board(10,5)
while True:
    A.spawn_apple()
    A.render()
    A.move_snake()
    A.check_if_found_apple()
    if A.check_hit() or A.out_of_bound():
        break
    sleep(0.25)
print("You've got " + str(A.points) + " points!")
