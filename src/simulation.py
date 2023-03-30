import copy
import networkx as nx

def run_sim(G, initial_values, steps):
    G_sim = G.copy()

    # add a node attribute called total_exports, calculated by summing the weights of all outgoing edges
    G_sim

    # add a node attribute called total_exports, calculated by summing the weights of all outgoing edges
    t_e = {}
    for country in G_sim.nodes():
        total_exports = 0
        for neighbor in G_sim.neighbors(country):
            total_exports += G_sim[country][neighbor]['weight']
        t_e[country] = total_exports
    nx.set_node_attributes(G_sim, t_e, 'total_exports')
    country_vals = {}
    for country in G_sim.nodes():
        if country in initial_values:
            country_vals[country] = [initial_values[country]]
        else:
            country_vals[country] = [0]

    for i in range(steps):
        country_vals_copy = copy.deepcopy(country_vals)
        for country in G_sim.nodes():
            # to each neighbor, add the fraction of the country's total exports
            for neighbor in G_sim.neighbors(country):
                country_vals[neighbor].append(country_vals_copy[neighbor][-1] + \
                                              country_vals_copy[country][-1] * G_sim[country][neighbor]['weight'] / G_sim.nodes[country]['total_exports'])

    return country_vals