import sys
import math

map_size_x = 16000
map_size_y = 9000

r_pod_colistion = 400
r_checkpoint = 600

def print_err(*args, **kwargs) -> None:
	print(*args, file=sys.stderr, **kwargs)

# Point
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

	def __eq__(self, other: 'Point') -> bool:
		return abs(self.x - other.x) <= r_checkpoint and abs(self.y - other.y) <= r_checkpoint

	def offset(self, off: int) -> 'Point':
		return Point(self.x + off, self.y + off)

	def dist(self, goal: 'Point') -> int:
		return int(math.sqrt((self.x - goal.x)**2 + (self.y - goal.y)**2))

# Checkpoint
class Checkpoint:
	def __init__(self, pos: Point, dist: int = 0):
		self.pos = pos
		self.dist = dist

def add_checkpoint(checkpoints: list[Checkpoint], pos: Point, dist: int) -> None:
	for checkpoint in checkpoints:
		if checkpoint.pos == pos:
			return
	checkpoints.append(Checkpoint(pos, dist))

def print_checkpoints(checkpoints: list[Checkpoint]) -> None:
	id = 0
	for checkpoint in checkpoints:
		print_err(id, checkpoint.pos.x, checkpoint.pos.y)
		id += 1

# Pods
class Pod:
	pos = Point(0, 0)
	def update_pos(self, pos: Point):
		self.pos = pos

class Enemie_Pod(Pod):
	pass

class My_Pod(Pod):
	pos = Point(0, 0)
	pos_dest = Point(0, 0)
	start_pos = Point(0, 0)
	nb_lap = 0
	dist = 0
	angle = 0
	speed = 100
	boost_used = False
	save_start = False
	checkpoint_reached = False
	def start_at(self, pos: Point):
		if not self.save_start:
			self.start_pos = pos
			self.save_start = True

	def update_checkpoint(self, pos: Point, dist: int, angle: int):
		self.pos_dest = pos
		self.dist = dist
		self.angle = angle
		if self.dist <= int(r_checkpoint * 1.5):
			self.checkpoint_reached = True
		else:
			self.checkpoint_reached = False

	def lap_done(self, pos: Point):
		if self.checkpoint_reached and self.start_pos == pos:
			self.nb_lap += 1
			print_err("Lap done")

	def longest_checkpoint(self, checkpoints: list[Checkpoint]) -> Checkpoint:
		return max(checkpoints, key=lambda checkpoint: checkpoint.dist)

	def speed_control(self):
		if abs(self.angle) > 90:
			self.speed = 0
		elif self.dist <= int(r_checkpoint * 1.5):
			self.speed = int(abs(math.cos(self.angle)) * 100)
		else:
			self.speed = 100

	def boost(self, checkpoints: list[Checkpoint]):
		if not self.boost_used and self.pos_dest == self.longest_checkpoint(checkpoints).pos and self.nb_lap > 0 and abs(self.angle) < 10:
			self.speed = "BOOST"
			self.boost_used = True

	def collision_imminent(self, enemiePod: Enemie_Pod) -> bool:
		return self.pos.dist(enemiePod.pos) <= r_pod_colistion

	def print_info(self):
		print_err(self.pos.x, self.pos.y, self.nb_lap, self.boost_used)

	def print(self):
		print(self.pos_dest.x, self.pos_dest.y, self.speed)

# Functions

def get_input_and_init_pods(myPod: My_Pod, enemiePod: Enemie_Pod, checkpoints: list[Checkpoint]) -> None:
	x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
	myPodPosition = Point(x, y)
	checkpointPos = Point(next_checkpoint_x, next_checkpoint_y)
	myPod.start_at(myPodPosition)
	myPod.update_pos(myPodPosition)
	myPod.update_checkpoint(checkpointPos, next_checkpoint_dist, next_checkpoint_angle)
	myPod.lap_done(checkpointPos)
	add_checkpoint(checkpoints, checkpointPos, next_checkpoint_dist)

	opponent_x, opponent_y = [int(i) for i in input().split()]
	enemiPosition = Point(opponent_x, opponent_y)
	enemiePod.update_pos(enemiPosition)

# game loop
def game_loop() -> None:
	myPod = My_Pod()
	enemiePod = Enemie_Pod()
	checkpoints = []
	while True:
		# initialisation
		get_input_and_init_pods(myPod, enemiePod, checkpoints)
		# print_checkpoints(checkpoints)
		# game logic
		myPod.speed_control()
		if myPod.collision_imminent(enemiePod):
			print_err("Collision imminent")
			myPod.pos_dest = myPod.pos_dest.offset(int(r_pod_colistion * 1.5))
		myPod.boost(checkpoints)
		myPod.print_info()
		myPod.print()

game_loop()