#algorithm imports
import math
import copy

#global parameter
margin = 0.1

# main functions 
def build_best_graph(node_list): # main master function
    i_dict = dict() # dictionary of the iterations
    for index in range(len(node_list)): # iter using each node as first node
        ordered_list = _improve_order(node_list,index) # call function, sort list using the first node
        i_dict[index] = dict()
        i_dict[index]['graph'], i_dict[index]['stress'] = _build_graph(ordered_list) # call function, get best coordinates
    best_graph = min([i_dict[x] for x in i_dict], key= lambda x: x['stress']) # select the best configuration
    return best_graph

def _improve_order(node_list, first_node_index): # sorting algorithm, slave of main master function
    improved_list = [ node_list[first_node_index] ] # set the first nodes, given by the parent function
    candidates_list = copy.copy(node_list)
    candidates_list.remove( improved_list[0] )
    for iteration in range( len(node_list)-1 ): # for each position
        candidates_score = list()
        for candidate in candidates_list: # try all candidates
            score = 0
            for used_node in improved_list:
                score += used_node.edges[candidate.id]
            candidates_score.append( [candidate,score] )
        max_score = max(candidates_score, key = lambda x: x[1])
        improved_list.append( max_score[0] ) # select candidates
        candidates_list.remove( max_score[0] )
    return improved_list # return best configuration

def _build_graph(x_list): # secondary master function, slave of main master function
    c_dict = _get_coordinates_dictionary(x_list) # call function
    total_stress = _total_stress(c_dict) # call function
    return c_dict, total_stress

def _get_coordinates_dictionary(x_list): # calculate coordinates, slave of secondary master function
    c_dict = dict() # dict of coordinates
    c_dict[0] = {'node':x_list[0],'coor':(0,0)} # special case
    c_dict[1] = {'node':x_list[1],'coor':_coor_index_1(x_list[0],x_list[1])} # call function, special case
    c_dict[2] = {'node':x_list[2],'coor':_coor_index_2(c_dict[0],c_dict[1],x_list[2])} # call function, special case
    for index in range(3,len(x_list)): # for non special cases
        c_dict[index] = _get_coordinates(x_list[index],c_dict) # call function, general case
    return c_dict

def _total_stress(c_dict): # total stress of the configuration coordinates, slave of secondary master function
    stress_sum = 0
    combination_list = _combinatory_without_repetition(len(c_dict)) # call function
    for combination in combination_list:
        nodedic1 = c_dict[ combination[0] ]
        nodedic2 = c_dict[ combination[1] ]
        edge_between_nodes = nodedic1['node'].edges[ nodedic2['node'].id ]
        x1 = nodedic1['coor'][0]
        y1 = nodedic1['coor'][1]
        x2 = nodedic2['coor'][0]
        y2 = nodedic2['coor'][1]
        distance = _distance(x1,y1,x2,y2) # call function
        stress_sum += edge_between_nodes*distance
    return stress_sum

#secondary functions
def _coor_index_1(node1,node2): # special case for the second circle of the bubble chart
    return ((node1.radius + node2.radius + margin),0 )

def _coor_index_2(nodedic1,nodedic2,node3): # special case for the third circle of the bubble chart
    coordinates = _get_points(nodedic1,nodedic2,node3)[0] # call function
    return (coordinates['x'],coordinates['y'])

def _get_points(nodedic1,nodedic2,node3):
    x1,y1,r1,x2,y2,r2,r3 = _get_parameters(nodedic1,nodedic2,node3) # call function
    virtual_radius_1 = (r1 + r3 + margin)
    virtual_radius_2 = (r2 + r3 + margin)
    return _intersecrions_points(x1,y1,virtual_radius_1,x2,y2,virtual_radius_2) # call function

def _get_coordinates(node3,c_dict):
    combination_list = _combinatory_without_repetition(len(c_dict)) # call function, get all node combinations
    candidates_list = list() #list of candidate coordinates
    for A, B in combination_list: # for each node combination
        dict_A = c_dict[A]
        dict_B = c_dict[B]
        if _is_valid_distance(dict_A,dict_B,node3): # call function, test if adyacent nodes are imposible
            candidate_points = _get_points(dict_A,dict_B,node3) # call function, get the possible coordinates
            for candidate in candidate_points:
                candidates_list.append(candidate) # append posible coordinates
    candidates_stress = _get_candidates_stress(candidates_list,c_dict,node3) # call function, get stress of the coordinates
    best_candidate = min(candidates_stress, key= lambda x: x[1]) # select coordinates with less stress
    return  {'node':node3,'coor':(best_candidate[0]['x'],best_candidate[0]['y'])} # return using dictionary format

def _get_candidates_stress(candidates_list,c_dict,node3): # get stress of the coordinates
    candidates_stress = list() 
    for index in range(len(candidates_list)): # for each candidate
        candidate    = candidates_list[index]
        stress_count = 0
        do_append = True
        x1 = candidate['x']
        y1 = candidate['y']
        r1 = node3.radius
        for index in c_dict: # for each node already in the graph
            x2 = c_dict[index]['coor'][0]
            y2 = c_dict[index]['coor'][1]
            r2 = c_dict[index]['node'].radius
            distance = _distance(x1,y1,x2,y2) # call function
            if distance < (r1 + r2): #check overlaping
                do_append = False
                break # stop if overlaping
            edge          = c_dict[index]['node'].edges[node3.id]
            stress        = edge*distance
            stress_count += stress
        if do_append: # remove overlaping coordinates
            candidates_stress.append([candidate,stress_count])
    return candidates_stress

#utility functions
class nodeclass(object): # sets the nodes as a class to store information
    pass

def _distance(x1,y1,x2,y2): # standard euclidian distance
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def _combinatory_without_repetition(number_of_indices): # standard combinaton without repetition
    combination_list = list()
    for index_A in range(number_of_indices):
        A = index_A
        for index_B in range(number_of_indices):
            if A < index_B:
                B = index_B
                combination_list.append((A,B))
    return combination_list

def _intersecrions_points(x1,y1,r1,x2,y2,r2): # standard intersecrion of circles
    R = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    a = (r1**2 - r2**2) / (2 * R**2)
    b = math.sqrt(2 * (r1**2 + r2**2) / R**2 - (r1**2 - r2**2)**2 / R**4 - 1)
    fx = (x1+x2) / 2 + a * (x2 - x1)
    gx = b * (y2 - y1) / 2
    ix1 = fx + gx
    ix2 = fx - gx
    fy = (y1+y2) / 2 + a * (y2 - y1)
    gy = b * (x1 - x2) / 2
    iy1 = fy + gy
    iy2 = fy - gy
    return [{'x':ix1, 'y':iy1}, {'x':ix2, 'y':iy2}]

def _get_parameters(nodedic1,nodedic2,node3): # get parameters from objects
    x1 = nodedic1['coor'][0]
    y1 = nodedic1['coor'][1]
    r1 = nodedic1['node'].radius
    x2 = nodedic2['coor'][0]
    y2 = nodedic2['coor'][1]
    r2 = nodedic2['node'].radius
    r3 = node3.radius
    return x1,y1,r1,x2,y2,r2,r3

def _is_valid_distance(nodedic1,nodedic2,node3): # test if circles overlap
    x1,y1,r1,x2,y2,r2,r3 = _get_parameters(nodedic1,nodedic2,node3) # call function
    valid = True
    distance = _distance(x1,y1,x2,y2) # call function
    overlaping = distance - r1 - r2 - 2*r3
    if overlaping > 0:
        valid = False
    return valid
	
# example data
node1 = nodeclass()
node2 = nodeclass()
node3 = nodeclass()
node4 = nodeclass()
node5 = nodeclass()

node1.radius = 3.
node2.radius = 5.
node3.radius = 7.
node4.radius = 1.
node5.radius = 2.

node1.edges = {'node1':  0., 'node2': 10., 'node3':  9., 'node4':  7., 'node5': 12.}
node2.edges = {'node1': 10., 'node2':  0., 'node3': 13., 'node4':  8., 'node5':  2.}
node3.edges = {'node1':  9., 'node2': 13., 'node3':  0., 'node4':  1., 'node5': 15.}
node4.edges = {'node1':  7., 'node2':  8., 'node3':  1., 'node4':  0., 'node5':  4.}
node5.edges = {'node1': 12., 'node2':  2., 'node3': 15., 'node4':  4., 'node5':  0.}

node1.id = 'node1'
node2.id = 'node2'
node3.id = 'node3'
node4.id = 'node4'
node5.id = 'node5'

node_list = [node1,node2,node3,node4,node5]

#run scrpit
my_dictionary = build_best_graph(node_list)

#graph imports
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

#graph values
fig, ax = plt.subplots(figsize=(10, 10))

x = [my_dictionary['graph'][x]['coor'][0] for x in my_dictionary['graph']]
y = [my_dictionary['graph'][x]['coor'][1] for x in my_dictionary['graph']]
radii = [my_dictionary['graph'][x]['node'].radius for x in my_dictionary['graph']]
patches = []
for x1, y1, r in zip(x, y, radii):
    circle = Circle((x1, y1), r)
    patches.append(circle)

p = PatchCollection(patches, alpha=0.4)
ax.add_collection(p)
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)

plt.show()