### The Ripple-Spreading Algorithm for the Many-to-Many Shortest Path Problem

##### Reference: 马一鸣，胡小兵，周航. 一种快速求解最短路径巡游问题的涟漪扩散算法[J]. 计算机应用研究.

The shortest path tour problem aims to find the shortest path that traverses multiple disjoint node subsets in a given order. The many-to-many shortest path tour problem has multiple sources and destinations. It aims to determine the shortest path tour for every source node to any one of the destination nodes.

----

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node1: {node2: length, node3: length, ...}, ...} |
| node_subset   | List, [[subset1], [subset2], ...]                            |
| source        | List, the source nodes of this subproblem of SPTP            |
| destination   | List, the destination nodes of this subproblem of SPTP       |
| init_time     | List, the initial time that should generate initial ripples at source nodes |
| init_radius   | List, the initial radius of initial ripples at source nodes  |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the ith ripple is epicenter_set[i] |
| path_set      | List, the path of the ith ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the ith ripple is radius_set[i]          |
| active_set    | List, active_set contains all active ripples                 |
| Omega         | Dictionary, Omega[n] = i denotes that ripple i is generated at node n |

----

#### Example

![m2mSPTP_example](C:\Users\dell\Desktop\研究生\个人算法主页\The ripple-spreading algorithm for the many-to-many shortest path tour problem\m2mSPTP_example.png)

```python
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
```

##### Output

```python
{
    0: {'path': [0, 3, 5], 'length': 6}, 
    2: {'path': [2, 3, 5], 'length': 6},
}
```

