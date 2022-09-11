#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/11 12:41
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA4m2mSPTP.py
# @Statement : The ripple-spreading algorithm for the many-to-many shortest path problem
# @Reference : 马一鸣，胡小兵，周航. 一种快速求解最短路径巡游问题的涟漪扩散算法[J]. 计算机应用研究.
import copy


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    Find the ripple-spreading speed
    :param network:
    :param neighbor:
    :return:
    """
    speed = 1e10
    for i in range(len(network)):
        for j in neighbor[i]:
            speed = min(speed, network[i][j])
    return speed


def subRSA(network, neighbor, source, destination, init_time, init_radius, v):
    """
    the ripple-spreading algorithm for the subproblems of SPTP
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param neighbor: the neighbor set
    :param source: the set of source nodes
    :param destination: the set of destination nodes
    :param init_time: the set of initial time for each initial ripple
    :param init_radius: the set of initial radius for each initial ripple
    :param v: the ripple-spreading speed
    :return:
    """
    # Step 1. Initialization
    nn = len(network)
    t = min(init_time) - 1
    nr = 0  # the number of ripples - 1
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    path_set = []  # path set
    active_set = []  # the set containing all active ripples
    start_flag = copy.deepcopy(source)
    dest_ripple = {}  # the ripple reaching destinations
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = -1

    # Step 2. The main loop
    while True:

        # Step 2.1. Termination judgment
        flag = True
        for node in destination:
            if omega[node] == -1:
                flag = False
                break
        if flag:
            break

        # Step 2.2. Time updates and generate initial ripples
        t += 1
        incoming_ripples = {}
        for ripple in active_set:

            # Step 2.3. Active ripples spread out
            radius_set[ripple] += v

            # Step 2.4. New incoming ripples
            epicenter = epicenter_set[ripple]
            path = path_set[ripple]
            radius = radius_set[ripple]
            for node in neighbor[epicenter]:
                if omega[node] == -1:  # the node is unvisited
                    temp_length = network[epicenter][node]
                    if node in incoming_ripples.keys():
                        temp_radius = incoming_ripples[node]['radius']
                    else:
                        temp_radius = 0
                    if temp_length + temp_radius <= radius:
                        temp_path = copy.deepcopy(path)
                        temp_path.append(node)
                        incoming_ripples[node] = {
                            'path': temp_path,
                            'radius': radius - temp_length,
                        }

        # Step 2.5 Generate initial ripples
        if start_flag:
            need_to_delete = []
            for node in start_flag:
                ind = source.index(node)
                if t == init_time[ind]:
                    need_to_delete.append(node)
                    if omega[node] == -1:
                        if node in incoming_ripples.keys():
                            if init_radius[ind] > incoming_ripples[node]['radius']:
                                incoming_ripples[node] = {
                                    'path': [node],
                                    'radius': init_radius[ind],
                                }
                        else:
                            incoming_ripples[node] = {
                                'path': [node],
                                'radius': init_radius[ind],
                            }
            for node in need_to_delete:
                start_flag.remove(node)

        # Step 2.6 Trigger new ripples
        for node in incoming_ripples.keys():
            new_ripple = incoming_ripples[node]
            path_set.append(new_ripple['path'])
            epicenter_set.append(node)
            radius_set.append(new_ripple['radius'])
            active_set.append(nr)
            omega[node] = nr
            if node in destination:
                dest_ripple[node] = {
                    'radius': new_ripple['radius'],
                    'time': t,
                    'path': new_ripple['path'],
                }
            nr += 1

        # Step 2.7 Active -> inactive
        remove_ripple = []
        for ripple in active_set:
            epicenter = epicenter_set[ripple]
            flag = True
            for node in neighbor[epicenter]:
                if omega[node] == -1:
                    flag = False
                    break
            if flag:
                remove_ripple.append(ripple)
        for ripple in remove_ripple:
            active_set.remove(ripple)

    # Step 3. Sort the results
    dest_time = []
    dest_radius = []
    dest_path = []
    for node in destination:
        temp_item = dest_ripple[node]
        dest_time.append(temp_item['time'])
        dest_radius.append(temp_item['radius'])
        dest_path.append(temp_item['path'])
    return dest_time, dest_radius, dest_path


def cal_cost(network, path):
    """
    calculate the cost
    :param network:
    :param path:
    :return:
    """
    cost = 0
    for i in range(len(path) - 1):
        cost += network[path[i]][path[i + 1]]
    return cost


def main(network, node_subset):
    """
    The main function
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param node_subset: the disjoint subsets of nodes
    :return:
    """
    # Step 1. Initialization
    neighbor = find_neighbor(network)  # the neighbor set
    v = find_speed(network, neighbor)  # the ripple-spreading speed
    new_network = {}  # reverse the network
    for i in range(len(network)):
        new_network[i] = {}
    for i in range(len(network)):
        for j in neighbor[i]:
            new_network[j][i] = network[i][j]
    new_subset = copy.deepcopy(node_subset)  # reverse the node subsets
    new_subset.reverse()
    init_radius = [0 for i in range(len(new_subset[0]))]
    init_time = [0 for i in range(len(new_subset[0]))]
    temp_path = {}

    # Step 2. The main loop
    for i in range(len(new_subset) - 1):
        source = new_subset[i]
        destination = new_subset[i + 1]
        init_time, init_radius, dest_path = subRSA(new_network, neighbor, source, destination, init_time, init_radius, v)
        for j in range(len(destination)):
            temp_path[destination[j]] = dest_path[j]

    # Step 3. Process the results
    result1 = {}
    for key in new_subset[-1]:
        path_set = []
        temp_node = key
        while key not in new_subset[0]:
            temp_result = copy.deepcopy(temp_path[key])
            key = temp_result[0]
            temp_result.pop(0)
            path_set.insert(0, temp_result)
        result = [new_subset[0][0]]
        for path in path_set:
            result.extend(path)
        cost = cal_cost(new_network, result)
        result.reverse()
        result1[temp_node] = {'path': result, 'length': cost}
    return result1


if __name__ == '__main__':
    test_network = {
        0: {1: 2, 2: 3, 3: 3},
        1: {0: 2, 3: 2},
        2: {0: 3, 3: 3},
        3: {0: 3, 1: 2, 2: 3, 4: 2, 5: 3, 6: 3},
        4: {3: 2, 6: 2},
        5: {3: 3, 6: 3},
        6: {3: 3, 4: 2, 5: 3},
    }
    subset = [[0, 2], [1, 3], [5, 6]]
    print(main(test_network, subset))
