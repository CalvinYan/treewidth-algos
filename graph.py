import random

class UndirectedGraph:
    def __init__(self, size: int):
        # assume graph is 1-indexed  vertices numbered 1...size
        assert size >= 1, "You need a graph of with at least 1 vertex"
        self.size = size
        self.edges = {i: set() for i in range(1,size+1)}
        self.edge_list = []

    def add_edge(self, vertex1: int, vertex2: int):
        assert vertex1 <= self.size and vertex2 <= self.size, f"Vertices have to be in the range [0 - {self.size}]"
        if(vertex1 == vertex2): return # we don't ban self-loops but will not be taken into account
        self.edges[vertex1].add(vertex2)
        self.edges[vertex2].add(vertex1)
        self.edge_list.append((vertex1, vertex2))

    def delete_edge(self, vertex1: int, vertex2: int):
        self.edges[vertex1].remove(vertex2)
        self.edges[vertex2].remove(vertex1)
    
    def __str__(self):
        string_rep = "Undirected graph with {} vertices\n".format(self.size)
        for i in range(self.size):
            curr_edges = sorted(list(self.edges[i]))
            string_rep += str(i) + ": "
            for edge in curr_edges:
                string_rep += str(edge) + ", "
            string_rep += "\n"
        return string_rep

class TreeDecomposition(UndirectedGraph):
    def __init__(self, size: int):
        super.__init__(self, size)
        self.bags = {i: set() for i in range(1,size+1)}
        self.width = 0

    def add_to_bag(self, vertex1: int, vertex2: int):
        assert vertex1 <= self.size and vertex2 <= self.size, f"Vertices have to be in the range [0 - {self.size}]"
        self.bags[vertex1].add(vertex2)
        if len(self.bags[vertex1]) - 1 > self.width:
            self.width = len(self.bags[vertex1]) - 1

    def width(self):
        return self.width


def generateRandomGraph(vertices: int, edges: int) -> UndirectedGraph:
    n = vertices
    # actually edges //= 2, because each edge generates 2 directed edges but ignore it for now
    assert edges <= (n*(n-1))//2, "Maximum number of edges exceeded"
    graph = UndirectedGraph(n)

    # generate all edges
    all_edges = []
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            if i == j: continue
            all_edges.append((i,j))

    random.shuffle(all_edges)

    for i in range(edges):
        new_edge = all_edges.pop()
        v1, v2 = new_edge
        graph.add_edge(v1,v2)
    
    return graph



def test_instances():
    # in the format (edge_list, vertices, answer)
    tests = [
        ([(1, 2), (1, 3), (1, 4), (3, 5), (4, 6)], 6, 1),
        ([(1, 2), (1, 3), (2, 3), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (4, 5), (5, 7), (5, 8), (6, 7), (7, 8)], 8, 2),
        ([(1, 2), (1, 4), (2, 3), (2, 5), (3, 6), (4, 5), (4, 7), (5, 6), (5, 8), (6, 9), (7, 8), (8, 9)],9,3),
        ([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)],5,4),
        
        # series parallel graph -> treewidth <= 2
        ([(1,2),(2,3),(2,4),(2,5),(3,6),(4,6),(5,6),(6,8),(1,7),(7,8)], 8 , 2)

        # complete graph of 5 edges -> treewidth 4
        ([(1, 2),(1, 3),(1, 4),(1, 5),(2, 3),(2, 4),(2, 5),(3, 4),(3, 5),(4, 5)], 5, 4)

        # long test case 
        ([(1, 13),(1, 17),(1, 19),(1, 6),(2, 15),(2, 18),(2, 19),(2, 20),(13, 16),(13, 20),(13, 21),(15, 17),(15, 21),(15, 3),(16, 18),(16, 3),(16, 4),(17, 4),(17, 5),(18, 5),(18, 6),(19, 8),(19, 14),(20, 7),(20, 9),(21, 8),(21, 10),(3, 9),(3, 11),(4, 10),(4, 12),(5, 11),(5, 14),(6, 7),(6, 12),(7, 10),(7, 11),(8, 11),(8, 12),(9, 12),(9, 14),(10, 14)], 21, 8)
    ]

    correct = 0
    wrong = []
    for idx,(test, n, answer) in  enumerate(tests):
        graph = UndirectedGraph(n)
        for x,y in test: graph.add_edge(x,y)
        
        ans = None
        # call treewidth solver
        # ans = treewidth(graph)
        if ans == answer:
            correct += 1
        else:
            wrong.append(idx)
    
    print(f"Passed {correct}/{len(tests)} test cases")
    if len(wrong):
        for i in wrong:
            print(f"Failed test case {i}: {tests[i][0]}" )
    
if __name__ == "__main__":
    g1 = generateRandomGraph(5,10)
    g2 = generateRandomGraph(8,16)