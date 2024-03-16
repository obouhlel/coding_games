import sys
import math

map_size_x = 16000
map_size_y = 9000
r_pod_colistion = 400
r_checkpoint = 600

# Classes
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: 'Point') -> 'Point':
        return Point(self.x * other.x, self.y * other.y)

    def dist(self, goal: 'Point') -> int:
        return int(math.sqrt((self.x - goal.x)**2 + (self.y - goal.y)**2))

class Pod:
    pos = Point(0, 0)
    def update_pos(self, pos: Point):
        self.pos = pos

class My_Pod(Pod):
    pos = Point(0, 0)
    pos_dest = Point(0, 0)
    dist = 0
    angle = 0
    speed = 100
    boost_used = False
    def update_checkpoint(self, pos: Point, dist: int, angle: int):
        self.pos_dest = pos
        self.dist = dist
        self.angle = angle

    def speed_control(self):
        if abs(self.angle) > 90:
            self.speed = 0
        elif self.dist < r_checkpoint * 4:
            self.speed = int(abs(math.cos(self.angle)) * 100)
        else:
            self.speed = 100

    def boost(self):
        if not self.boost_used:
            print(self.pos_dest.x, self.pos_dest.y, "BOOST")
            self.boost_used = True
        else:
            print_err("Boost is already used")

    def print_info(self):
        print_err(self.pos.x, self.pos.y, self.pos_dest.x, self.pos_dest.y, self.dist, self.angle, self.boost_used)

    def print(self):
        print(self.pos_dest.x, self.pos_dest.y, self.speed)

class Enemie_Pod(Pod):
    pass

# Functions
def print_err(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)

def get_input_and_init_pods(myPod: My_Pod, enemiePod: Enemie_Pod) -> None:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    myPodPosition = Point(x, y)
    checkpointPos = Point(next_checkpoint_x, next_checkpoint_y)
    myPod.update_pos(myPodPosition)
    myPod.update_checkpoint(checkpointPos, next_checkpoint_dist, next_checkpoint_angle)

    enemiPosition = Point(opponent_x, opponent_y)
    enemiePod.update_pos(enemiPosition)

# game loop
def game_loop() -> None:
    myPod = My_Pod()
    enemiePod = Enemie_Pod()
    while True:
        # initialisation
        get_input_and_init_pods(myPod, enemiePod)

        # game logic
        if myPod.angle == 0 and myPod.dist >= 2000 and not myPod.boost_used:
            myPod.boost()
            continue
        myPod.speed_control()
        myPod.print_info()
        myPod.print()

game_loop()