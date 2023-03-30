import networkx as nx
import pycountry

def load_pajek(filename):
    """
        loads a Pajek file. the format of the relevant Partek file is:
        *Vertices N
        1 "Country 1" x y z
        2 "Country 2" x y z
        ...
        *Arcs
        1 2 Weight
        1 3 Weight
        ...

        args: filename: the path to the pajek file
        returns: a networkx DiGraph
    """

    G = nx.DiGraph()
    name_index_map = {}
    with open(filename) as f:
        lines = f.readlines()
        # read the vertices
        N = int(lines[0].split()[1])
        for i in range(1, N+1):
            line = lines[i]
            line = line.split()
            idx, alpha_3, x, y, z = int(line[0]), line[1].strip('"'), float(line[2]), float(line[3]), float(line[4])
            G.add_node(idx, name=alpha_3, attr_dict=dict(alpha_2=pycountry.countries.get(alpha_3=alpha_3).alpha_2.lower(), x=x, y=y))
            name_index_map[idx] = alpha_3
        # read the edges
        for line in lines[N+2:]:
            line = line.split()
            try:
                idx1, idx2, weight = int(line[0]), int(line[1]), float(line[2])
            except:
                print(line)
            G.add_edge(idx1, idx2, weight=weight)
    nx.relabel_nodes(G, name_index_map, copy=False)
    return G