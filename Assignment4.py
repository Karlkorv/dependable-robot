from Assignment3 import known_obstacles, dijkstra_find_path

board = [[1, 2, 3, 4, 5, 6],
         [7, 8, 9, 10, 11, 12],
         [13, 14, 15, 16, 17, 18], 
         [19, 20, 21, 22, 23, 24],
         [25, 26, 27, 28, 29, 30],
         [31, 32, 33, 34, 35, 36],
         [37, 38, 39, 40, 41, 42]]

conveyor_belt = {
    "coordinates": [0,0],
    "position": 0
}

class task:
    def __init__(self, source_coordinates, source_position, destination_position, destination_coordinates):
        self.source_coordinates = source_coordinates
        self.source_position = source_position
        self.destination_coordinates = destination_coordinates
        self.destination_position = destination_position
        sellf.assigned_robot = None

    def assignRobot(robot):
        ass
    
    def getSourcePosition(self):
        return 




tasks = [{
    # Bring a box from the conveyor belt to shelf 8 position p1
    
    "source": conveyor_belt,
    "destination": {"coordinates": [1,1], # shelf 8
                    "position": 1}},
    # Bring a box from shelf 9 position p2 to the conveyor belt
    {"source": {"coordinates": [1,2], # shelf 9
                    "position": 2}, 
    "destination": conveyor_belt}, 
    #Bring a box from shelf s29 position p3 to shelf s35 position p4
        {"source": {"coordinates": [4,4], # shelf 29
                    "position": 3}, 
    "destination": {"coordinates": [5,4], #shelf 35
                    "position": 4}}, 
    # Bring a box from shelf s9 position p1 to the conveyor belt
        {"source": {"coordinates": [1,2], # shelf 9 
                    "position": 1},
    "destination": conveyor_belt}, 
    # Bring a box from shelf s8 position p2 to shelf s29 position p1         
        {"source": {"coordinates": [1,1], # shelf 8
                    "position": 2},
    "destination": {"coordinates": [4,4], # shelf 29
                    "position": 1}}]

class robot:
    def __init__(self, pos):
        self.position = pos
        self.battery = 100
        self.assigned = False
    
    def getPosition(self):
        return self.position

    def getBattery(self):
        return self.battery

robots = [robot([1,5]),
          robot([5,5]),
          robot([0,3]),
          robot([4,4]),
          robot([1,3])]


def assignRobots():
    for task in tasks:
        for robot in robots:
            if not robot.assigned:
                path = calculatePath(robot, task)
                if len(path) < robot.getBattery:
                    #Assign that robot to task
                    break
                
    

# assignRobots:
# for task in tasks[]:
# calculatePath(robot, goal)
# chooseRobotForTask(robots[])

def calculatePath():
    pass

# calculatePath:
# 	path = djikstras(robot.position, goal)
# 	if (path.length > robot.charge)
# 		signalWMS(“needs charging”)

# executePath:
# 	detectObstacles(path)
# 	move()
# 	checkRobotBattery(robot, pathLength)

# detectObstacles:
# 	obstacle = readRadar()
# 	if (obstacle)
# 		signalWMS(“need new path”)


# chooseRobotForTask:
# 	for robot in robots:
# 		if (len(calculatePath) < robot.charge)
# 			return robot
# 	return “No robot available for task :(”
	
# executeTask:
# 	executePath()
# 	pickUpBox()
# 	executePath()
# 	dropBox()

# main:
# 	assignRobots()
# 	executeTask()
