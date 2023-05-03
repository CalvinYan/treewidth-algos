import random
from typing import List, Tuple, Set, Dict

class UndirectedGraph:
    def __init__(self, size: int):
        # assume graph is 1-indexed  vertices numbered 1...size
        assert size >= 1, "You need a graph of with at least 1 vertex"
        self.size = size
        self.vertices = set(range(1,size+1))
        self.edges = {i: set() for i in range(1,size+1)}
        self.edge_list = set()

    def add_edge(self, vertex1: int, vertex2: int):
        assert vertex1 in self.vertices and vertex2 in self.vertices, f"Valid vertices are only: {self.vertices}"
        if(vertex1 == vertex2): return # we don't ban self-loops but will not be taken into account
        self.edges[vertex1].add(vertex2)
        self.edges[vertex2].add(vertex1)
        if(vertex1 > vertex2):
            vertex1, vertex2 = vertex2, vertex1
        self.edge_list.add((vertex1, vertex2))
    
    def __str__(self) -> str:
        string_rep = "Undirected graph with {} vertices\n".format(self.size)
        for i in self.vertices:
            curr_edges = sorted(list(self.edges[i]))
            string_rep += str(i) + ": "
            for edge in curr_edges:
                string_rep += str(edge) + ", "
            string_rep += "\n"
        return string_rep
    
    def vertex_degrees(self) -> Dict[int, int]:
        deg = {}
        for v in self.vertices:
            deg[v] = len(self.edges[v])
        return deg
    
    # 2-approximation greedy algorithm
    def maximal_matching(self) -> Set[Tuple[int, int]]:
        seen = set()
        matching = set()
        for u,v in self.edge_list:
            if(u not in seen and v not in seen):
                matching.add((u,v))
                seen.add(u)
                seen.add(v)
        return matching
    
    # contract graph given a matching
    def contract_graph(self, matching: Set[Tuple[int, int]]) -> "UndirectedGraph":
        # u merges with v to become a big node
        mapping = {u: v for u,v in matching}
        new_size = self.size - len(matching)
        g = UndirectedGraph(new_size)

        # number new edges appropriately
        new_edges = {}
        curr_num = 1
        for i in self.vertices:
            if(i not in mapping):
                new_edges[i] = curr_num
                curr_num += 1

        # create new edges
        for node, neighbors in self.edges.items():
            # get new index, accounts for if node has been contracted 
            if node in mapping:
                node1 = new_edges[mapping[node]]
            else:
                node1 = new_edges[node]
            

            for neigh in neighbors:
                # contracted edge does not appear in new graph
                if (node, neigh) in matching:
                    continue

                if neigh in mapping:
                    node2 = new_edges[mapping[neigh]]
                else:
                    node2 = new_edges[neigh]
                
                g.add_edge(node1, node2)
        
        return g
    
    # definition: neighbors form a clique
    def get_simplicial_vertices(self) -> List[int]:
        # TO IMPROVE: currently O(V^3) -> can use a queue and 2 bucket sorts to make it linear
        simplicial_vertices = []
        for u in self.vertices:
            neighbors = self.edges[u] 
            if all(v in self.edges[w] for v in neighbors for w in neighbors if v != w):
                simplicial_vertices.append(u)
        return simplicial_vertices
    

    def is_simplicial(self) -> bool:
        return len(self.get_simplicial_vertices()) == self.size
    

    def subgraph(self, nodes: Set[int]) -> "UndirectedGraph":
        num_v = len(nodes)
        sub_g = UndirectedGraph(num_v)
        mapping = {}
        curr = 1
        for node in nodes:
            mapping[node] = curr
            curr += 1
        
        for node in nodes:
            for neighbor in self.edges[node]:
                if neighbor not in nodes: continue
                u,v = mapping[node], mapping[neighbor]
                sub_g.add_edge(u,v)
        return sub_g

    # create deep copy of current graph
    def copy(self) -> "UndirectedGraph":
        new_graph = UndirectedGraph(self.size)
        for u,v in self.edge_list:
            new_graph.add_edge(u,v)
        return new_graph
    
    # will throw an error if edge does not exist
    def remove_edge(self, u: int, v:int):
        assert u in self.vertices and v in self.vertices, f"{u} or {v} are not valid vertices"
        assert u in self.edges[v] and v in self.edges[u], f"{u}-{v} is not a valid edge"
        if u > v: u,v = v,u
        assert (u,v) in self.edge_list, f"Something probably went wrong if it only threw an error here"
        self.edges[u].remove(v)
        self.edges[v].remove(u)
        self.edge_list.remove((u,v))


    def remove_node(self, node: int):
        assert node in self.vertices, "Not valid vertex"
        for neighbor in self.edges[node]:
            if node > neighbor:
                u,v = neighbor, node
            else:
                u,v = node, neighbor
            
            # only need to remove the neighbor, as we will completely delete the self.edges[node] after
            self.edges[neighbor].remove(node)
            self.edge_list.remove((u,v))
        
        del self.edges[node]
        self.vertices.remove(node)
        self.size -= 1


        


class TreeDecomposition(UndirectedGraph):
    def __init__(self, size: int):
        super.__init__(self, size)
        self.bags = {i: set() for i in self.vertices}
        self.width = 0

    def add_to_bag(self, vertex1: int, vertex2: int):
        assert vertex1 <= self.size and vertex2 <= self.size, f"Vertices have to be in the range [0 - {self.size}]"
        self.bags[vertex1].add(vertex2)
        if len(self.bags[vertex1]) - 1 > self.width:
            self.width = len(self.bags[vertex1]) - 1

    def get_width(self):
        return self.width
    
    def reconstruct_parent_tree(self, matching: Set[Tuple[int,int]]) -> "TreeDecomposition":
        # TODO: for jon to implement
        # matching contains u,v that were contracted, 
        return 




def generateRandomGraph(vertices: int, probability: float) -> UndirectedGraph:
    assert 0 < probability <= 1, "Probability has to be within 0-1"
    n = vertices
    graph = UndirectedGraph(n)

    # generate all edges
    all_edges = []
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            if i == j: continue
            all_edges.append((i,j))

    for u,v in all_edges:
        if random.random() < probability:
            graph.add_edge(u,v)
    
    return graph



def test_instances(is_exact = True, approx_ratio = None):
    
    # the approx ratio has to be given if its not exact
    if(not is_exact): assert approx_ratio

    # in the format (edge_list, vertices, answer)
    tests = [
        ([(1, 2), (1, 3), (1, 4), (3, 5), (4, 6)], 6, 1),
        ([(1, 2), (1, 3), (2, 3), (2, 5), (2, 6), (2, 7), (3, 4), (3, 5), (4, 5), (5, 7), (5, 8), (6, 7), (7, 8)], 8, 2),
        ([(1, 2), (1, 4), (2, 3), (2, 5), (3, 6), (4, 5), (4, 7), (5, 6), (5, 8), (6, 9), (7, 8), (8, 9)],9,3),
        ([(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)],5,4),
        
        # series parallel graph -> treewidth <= 2
        ([(1,2),(2,3),(2,4),(2,5),(3,6),(4,6),(5,6),(6,8),(1,7),(7,8)], 8 , 2),

        # complete graph of 5 edges -> treewidth 4
        ([(1, 2),(1, 3),(1, 4),(1, 5),(2, 3),(2, 4),(2, 5),(3, 4),(3, 5),(4, 5)], 5, 4),

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
        if (is_exact and ans == answer) or (not is_exact and ans <= approx_ratio * answer):
            correct += 1
        else:
            wrong.append(idx)
    
    
    kind_string = "exact" if is_exact else f"{approx_ratio}-approximation"
    print(f"Treewidth estimation ({kind_string})")
    print(f"Passed {correct}/{len(tests)} test cases")
    if len(wrong):
        for i in wrong:
            print(f"Failed test case {i}: {tests[i][0]}" )
    
if __name__ == "__main__":
    g1 = generateRandomGraph(5,0.6)
    g2 = generateRandomGraph(8,0.5)