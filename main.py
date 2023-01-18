#Made by Alisher 2023 test test test I am learning to use GitHub


#Make logs

from usefulFunctions import *

filelog = open("logs.txt", 'w')
def logprint(text, end = "\n"):
    filelog.write(text + end)


# Setting important constants
velocity = 14  # kph to mps


class Car:
    def __init__(self, graph, init_node, target_node=None, color=None):  # add color later
        self.current_position = get_position_of_node(graph, init_node)
        self.color = color
        if target_node != None:
            self.target_pos = get_position_of_node(graph, target_node)
            self.target_node = target_node

    def update_pos(self, new_pos):  # manual update of position
        self.current_position = new_pos

    def move_towards_node(self, target_node, time=1):  # without considering other drivers' behavior so far
        tx, ty = get_position_of_node(G, target_node)
        ix, iy = self.current_position

        real_dist = lat_to_km(ix, iy, tx, ty)
        logprint("real distance = " + str(real_dist))  # Print to the logfile
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
        else:
            self.current_position = tx, ty

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

nodesList = getAllNodesIDs(G)
print(nodesList[0])
print(get_position_of_node(G, nodesList[0]))
route = nx.shortest_path(G, nodesList[0], nodesList[1])
# fig, ax = ox.plot_graph_route(G, route, orig_dest_size = 100, show=False, close=False)

# G_nx = nx.relabel.convert_node_labels_to_integers(G)
# nodes, edges = ox.graph_to_gdfs(G_nx, nodes=True, edges=True)
# results = [nodes, edges]


fig, ax = ox.plot_graph(G, show=False, close=False)
ax.set_facecolor('green')
xx1, yy1 = get_position_of_node(G, nodesList[0])
xx2, yy2 = get_position_of_node(G, nodesList[1])
ax.scatter(xx1, yy1, c='red')
ax.scatter(xx2, yy2, c='red')

# ax.scatter(traffic_nodes_temp[numtemp][0], traffic_nodes_temp[numtemp][1], c='red')
plt.show()

lat_to_km(xx1, yy1, xx2, yy2)



tsutsenya = Car (G, nodesList[0])
print(tsutsenya.current_position)

"""fig, ax = ox.plot_graph(G, show=False, close=False)
ax.set_facecolor('green')
xx1, yy1 = tsutsenya.current_position
ax.scatter(xx1, yy1, c='red')
plt.xlabel ("Initial Position")
plt.show()"""


for i in range (5):
    tsutsenya.move_towards_node(nodesList[1], 5)
    logprint("current position" + str(tsutsenya.current_position))

    """fig, ax = ox.plot_graph(G, show=False, close=False)
    ax.set_facecolor('green')
    xx1, yy1 = tsutsenya.current_position
    ax.scatter(xx1, yy1, c='red'
    plt.xlabel("Position, iteration: " + str(i))
    plt.show())"""



# Exiting
filelog.close()
