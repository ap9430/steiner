import math
import copy


class Node:
    def __init__(self):
        # neighbors
        self.edges = {}
        self.value = None
        self.location = []

    def Node(self, edges, value, location):
        self.edges = edges
        self.value = value
        self.location = location

    def __str__(self):
        return self.value


class Edge:
    def __init__(self, a, b, w):
        self.n = a
        self.nprime = b
        self.w = w

    def __str__(self):
        return str(self.n.value), str(self.nprime.value), self.w


class Graph:
    def __init__(self, nodes, edges, routes):
        self.nodes = nodes
        self.edges = edges
        self.routes = routes

    def __str__(self):
        verts = ''
        for node in self.nodes:
            verts += node.value
        return verts


# fill in missing edges of the graph
def add_edges(n, nodes, edges):
    for node in nodes:
        if n != node:
            if n.value < node.value:
                if (str(n), str(node)) not in edges:
                    edges[(str(n), str(node))] = math.inf
            else:
                if (str(node), str(n)) not in edges:
                    edges[(str(node), str(n))] = math.inf
    return


# shorted paths within subtree
def sp_in_subtree(subtree, graph):
    for i in subtree.nodes:
        for j in subtree.nodes:
            if i != j:
                subtree.edges[key(i, j)] = graph.edges[key(i, j)]


# shorted path from a node to a subtree
def sp_between_subtree(node, subtree2, graph):
    min = math.inf
    if node in subtree2.nodes:
        if min > 0:
            min = 0
    else:
        for j in subtree2.nodes:
            if node != j:
                if min > graph.edges[key(node, j)]:
                    min = graph.edges[key(node, j)]
    return min


# Floyd-Warshall algorithm
def floyds(graph):
    for k in graph.nodes:
        for i in graph.nodes:
            for j in graph.nodes:
                if k != i and i != j and k != j:
                    if graph.edges[key(i, j)] > graph.edges[key(i, k)] + graph.edges[key(k, j)]:
                        graph.edges[key(i, j)] = graph.edges[key(i, k)] + graph.edges[key(k, j)]


# keying function for dictionary
def key(i, j):
    if i.value < j.value:
        return (str(i), str(j))
    else:
        return (str(j), str(i))


# non revised hueristic function
def hueristic(node, tree, graph):
    min_h = []
    for t in tree:
        new_n = math.inf
        # if the node is in the tree already, distance is 0
        if node in t.nodes:
            new_n = 0
        else:
            for n in t.nodes:
                # if the node is in the graph alone
                if key(n, node) in graph.edges:
                    if new_n > graph.edges[key(n, node)]:
                        new_n = graph.edges[key(n, node)]
                else:
                    if new_n > graph.edges[(str(node), str(t))]:
                        new_n = graph.edges[(str(node), str(t))]
        min_h.append(new_n)

    # get the smallest distance
    min_h = sorted(min_h)
    h = math.inf
    for i in range(1, len(min_h)):
        new_h = sum(min_h[0:i + 1]) / i
        if new_h < h:
            h = new_h
    return h

# examples 1 - 2 from the paper
def example1_2():
    # initialization of graph
    a, b, c, d, e, f, g, h, i = Node(), Node(), Node(), Node(), Node(), Node(), Node(), Node(), Node()
    a.value = 'a'
    b.value = 'b'
    c.value = 'c'
    d.value = 'd'
    e.value = 'e'
    f.value = 'f'
    g.value = 'g'
    h.value = 'h'
    i.value = 'i'

    nodes = [a, b, c, d, e, f, g, h, i]
    for node in nodes:
        add_edges(node, nodes, node.edges)

    phy_edges = set()

    # create edges and neighbors
    a.edges[(str(a), str(b))] = 4
    a.edges[(str(a), str(d))] = 3
    phy_edges.add((str(a), str(b)))
    phy_edges.add((str(a), str(d)))

    b.edges[(str(b), str(c))] = 2
    b.edges[(str(b), str(d))] = 5
    b.edges[(str(b), str(e))] = 3
    b.edges[(str(b), str(f))] = 3
    b.edges[(str(b), str(g))] = 4
    phy_edges.add((str(b), str(c)))
    phy_edges.add((str(b), str(d)))
    phy_edges.add((str(b), str(e)))
    phy_edges.add((str(b), str(f)))
    phy_edges.add((str(b), str(g)))

    c.edges[(str(c), str(g))] = 1
    phy_edges.add((str(c), str(g)))

    d.edges[(str(d), str(e))] = 1
    d.edges[(str(d), str(f))] = 2
    d.edges[(str(d), str(h))] = 1
    d.edges[(str(d), str(i))] = 1
    phy_edges.add((str(d), str(e)))
    phy_edges.add((str(d), str(f)))
    phy_edges.add((str(d), str(h)))
    phy_edges.add((str(d), str(i)))

    e.edges[(str(e), str(f))] = 1
    phy_edges.add((str(e), str(f)))

    f.edges[(str(f), str(g))] = 2
    f.edges[(str(f), str(i))] = 2
    phy_edges.add((str(f), str(g)))
    phy_edges.add((str(f), str(i)))

    g.edges[(str(g), str(i))] = 3
    phy_edges.add((str(g), str(i)))

    h.edges[(str(h), str(i))] = 2
    phy_edges.add((str(h), str(i)))

    Graph1 = Graph(nodes, {}, {})

    # switch the edges over to the graph
    for node in nodes:
        for k in node.edges.keys():
            if k not in Graph1.edges:
                Graph1.edges[k] = node.edges[k]

    floyds(Graph1)

    Graph2 = copy.deepcopy(Graph1)

    # steiner nodes
    tb = Graph([b], {}, {})
    tc = Graph([c], {}, {})
    te = Graph([e], {}, {})
    th = Graph([h], {}, {})
    ti = Graph([i], {}, {})
    tree_nodes = [tb, tc, te, th, ti]
    Tree = tree_nodes
    m_list = set()
    Tree2 = []
    Tree2_routes = []

    # algorithm
    x = 0
    while True:
        x += 1
        # step 1
        hue = []
        for node in nodes:
            hue.append((node, hueristic(node, Tree, Graph2)))
        hue = sorted(hue, key=lambda k: [k[1], k[0].value])
        for h in range(len(hue)):
            if hue[h][0] not in m_list:
                m = hue[h][0]
                m_list.add(m)
                break

        # step 2
        Tree2.append(m)
        min_d = []
        for t in Tree:
            for n in t.nodes:
                if n != m:
                    min_d.append((n, Graph1.edges[key(n, m)]))
        min_d = sorted(min_d, key=lambda k: [k[1], k[0].value])
        # if the closest nodes aren't already in our tree
        if (min_d[0][0]) not in Tree2:
            Tree2.append(min_d[0][0])
        if (min_d[1][0]) not in Tree2:
            Tree2.append(min_d[1][0])

        if tuple(sorted((str(m), str(min_d[0][0])))) in phy_edges:
            Tree2_routes.append(tuple(sorted((str(m), str(min_d[0][0])))))
        if tuple(sorted((str(m), str(min_d[1][0])))) in phy_edges:
            Tree2_routes.append(tuple(sorted((str(m), str(min_d[1][0])))))

        # step 3
        remove_list = []
        for t in Tree:
            if min_d[0][0].value == t.nodes[0].value or min_d[1][0].value == t.nodes[0].value or m.value == t.nodes[0].value:
                remove_list.append(t)
        for t in remove_list:
            Tree.remove(t)

        # step 4
        if len(Tree) == 1:
            break

        TG2 = Graph(Tree2, {}, {})
        Tree.append(TG2)
        Tree2 = TG2.nodes
        edges = {}
        # key = (node, tree) = distance between them
        for node in nodes:
            for tk in Tree:
                dist = sp_between_subtree(node, tk, Graph1)
                edges[(str(node), str(tk))] = dist
        Graph2.edges = edges

    # print final tree
    for t in Tree:
        print('[', end='')
        for j in t.nodes:
            print(j.value, end='')
        print(']', end='')
    print()

    # print paths in tree
    for i in Tree2_routes:
        print(i, end='')
    print()


def main():
    example1_2()


if __name__ == '__main__':
    main()
