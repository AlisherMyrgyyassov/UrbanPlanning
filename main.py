# Made by Alisher 2023 test test test I am learning to use GitHub

# Make function to test the movement
# Modify movement function
# Add signs and traffic lights
# Pedestrians (?)
# Make an adjacency matrix

from usefulFunctions import *

filelog = open("logs.txt", 'w')
def logprint(text, end = "\n"):
    filelog.write(text + end)


# Setting important constants
velocity = 50  # kph to mps, 14 by default


class Car:
    """
    Class of a car driver initially assigned with the current node and the target node
    """

    def __init__(self, graph, init_node, target_node, color=None):  # add color later
        """
        :param init_node: node ID of the initial node
        :param target_node: node ID of the target node
        """
        self.current_position = get_position_of_node(graph, init_node)
        self.color = color

        self.target_position = get_position_of_node(graph, target_node)
        self.target_node = target_node

        self.all_target_nodes = nx.shortest_path(graph, init_node, target_node)
        self.all_target_nodes = self.all_target_nodes[1:]

        self.current_node = init_node

        self.is_on_node = False  # A boolean variable to check if the car is on intersection

        self.waiting_count = 0  # Number of ticks to wait

    def wait(self, tick_number):
        self.waiting_count = tick_number

    def update_pos(self, new_pos):  # manual update of position
        self.current_position = new_pos

    def move_towards_node(self, local_target_node, time=1):  # without considering other drivers' behavior so far
        tx, ty = get_position_of_node(G, local_target_node)
        ix, iy = self.current_position

        real_dist = lat_to_km(ix, iy, tx, ty)
        # print("real distance = ", real_dist)
        if real_dist >= (velocity * time):
            map_dist = math.sqrt((tx - ix) ** 2 + (ty - iy) ** 2)
            traveling_dist = map_dist / real_dist * velocity * time

            angle = math.atan((ty - iy) / (tx - ix))
            if (tx - ix) < 0:
                angle += math.pi
            new_x = ix + traveling_dist * math.cos(angle)
            new_y = iy + traveling_dist * math.sin(angle)
            # print("map_dist = ", map_dist, "\ntravelling dist", traveling_dist, ix, iy, new_x, new_y)
            self.current_position = np.array([new_x, new_y])
            self.is_on_node = False  # Still moving, not on node
        else:
            self.current_position = tx, ty
            self.current_node = local_target_node
            self.is_on_node = True  # Is on node

    def finished(self):
        """
        Returns boolean true if the destination is reached, false if not
        """
        if self.current_node == self.target_node:
            return True
        else:
            return False

    def iter_to_target(self):
        if not self.finished():
            if self.waiting_count == 0:
                self.move_towards_node(self.all_target_nodes[0])
                if self.current_node == self.all_target_nodes[0]:
                    # print (self.all_target_nodes[0], "is reached")
                    self.all_target_nodes = self.all_target_nodes[1:]
            else:
                self.waiting_count -= 1

    def get_status(self):
        """
        Returns a dictionary with the status information about an object
        """
        self.status = {"CurrentNode": self.current_node,
                       "CurrentPosition": self.current_position,
                       "TargetNode": self.target_node,
                       "TargetPosition": self.target_position,
                       "OnNode": self.is_on_node}
        return self.status


class TrafficLight:
    """Class for traffic lights"""

    def __init__(self, graph, node_id, time=5):
        self.state = random.randint(0, 1)  # Initialize with random, green (0) or red (1)
        self.ticks = 0
        self.id = node_id
        self.graph = graph
        self.time = time

    def get_position(self):
        return get_position_of_node(self.graph, self.id)

    def one_tick(self):
        self.ticks += 1
        if self.ticks % self.time == self.time - 1:
            if self.state == 0:
                self.state = 1
            else:
                self.state = 0

    def get_color(self):
        if self.state:
            return "red"
        else:
            return "green"

    def draw_on_map(self, ax):
        xx, yy = self.get_position()
        ax.scatter(xx, yy, c=self.get_color())


#Uploading coordinates. To change, modify config file

f = open('.\config\coordinates.txt')
boundtemp = []
for line in f:
    boundtemp.append(float(line[0:len(line)-1]))

boundaries = {"north": boundtemp[0], #Coordinates of Hong Kong Happy Valley
              "south": boundtemp[1],
              "east": boundtemp[2],
              "west": boundtemp[3] }
print (boundaries)

f.close()

#Initializing the map

geod = Geodesic.WGS84
G = ox.graph_from_bbox(boundaries["north"], boundaries["south"], boundaries["east"], boundaries["west"], network_type='drive')
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

projected_graph = ox.project_graph(G, to_crs="EPSG:3395")
Gc = ox.consolidate_intersections(projected_graph, dead_ends=True)
edges = ox.graph_to_gdfs(ox.get_undirected(Gc), nodes=False)

# fig, ax = ox.plot_graph_route(G, route, orig_dest_size = 100, show=False, close=False)

# G_nx = nx.relabel.convert_node_labels_to_integers(G)
# nodes, edges = ox.graph_to_gdfs(G_nx, nodes=True, edges=True)
# results = [nodes, edges]


"""fig, ax = ox.plot_graph(G, show=False, close=False)
ax.set_facecolor('green')
xx1, yy1 = get_position_of_node(G, nodesList[0])
xx2, yy2 = get_position_of_node(G, nodesList[1])
ax.scatter(xx1, yy1, c='red')
ax.scatter(xx2, yy2, c='red')"""

# ax.scatter(traffic_nodes_temp[numtemp][0], traffic_nodes_temp[numtemp][1], c='red')
# plt.show()

nodesList = getAllNodesIDs(G)

tsutsenya = Car (G, nodesList[0], nodesList[12])
print(tsutsenya.current_position)

"""fig, ax = ox.plot_graph(G, show=False, close=False)
ax.set_facecolor('green')
xx1, yy1 = tsutsenya.current_position
ax.scatter(xx1, yy1, c='red')
plt.xlabel ("Initial Position")
plt.show()"""


for i in range (5):
    tsutsenya.iter_move()
    logprint("current position" + str(tsutsenya.current_position))

    fig, ax = ox.plot_graph(G, show=False, close=False)
    ax.set_facecolor('green')
    xx1, yy1 = tsutsenya.current_position
    ax.scatter(xx1, yy1, c='red')
    plt.xlabel("Position, iteration: " + str(i))
    plt.show()



# Exiting
filelog.close()
