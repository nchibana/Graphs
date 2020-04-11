from graph import Graph

def earliest_ancestor(ancestors, starting_node):
    vertices = list(set(list(sum(ancestors, ()))))
    graph = Graph()
    for vertex in vertices:
        graph.add_vertex(vertex)
    
    for edge in ancestors:
        graph.add_edge(edge[1], edge[0])
    
    paths = []

    for vertex in vertices:
        if vertex != starting_node and graph.dfs(starting_node, vertex):
            paths.append(graph.dfs(starting_node, vertex))

    if len(paths) > 0:
        longest_path = max(paths, key=len)
        return longest_path[-1]
    else:
        return -1
