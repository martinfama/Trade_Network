import pygal 
from pygal.style import DarkSolarizedStyle
import webbrowser
import pycountry
import matplotlib.pyplot as plt
plt.style.use('dark_background')
# set the default colors cycle to category10
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.get_cmap('tab10').colors)
plt.rcParams['font.size'] = 14
import networkx as nx

from .dataanalysis import *



def country_exports_imports_yearly_graph(G_Years=None, country=None):
    """
        Plots the yearly trade of a country. Simply uses `country_exports_imports_yearly` (same args).
        args: Same as `country_exports_imports_yearly`
        returns: fig, ax: the figure and axis objects of the plot
    """
    years = list(G_Years.keys())
    yearly_trade = country_exports_imports_yearly(G_Years=G_Years, country=country)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years, [1000*trade[0] for trade in yearly_trade], label='Imports', marker='o')
    ax.plot(years, [1000*trade[1] for trade in yearly_trade], label='Exports', marker='o')
    # plot the difference between exports and imports
    ax.plot(years, [1000*(trade[1] - trade[0]) for trade in yearly_trade], label='Balance', marker='o')
    ax.set_title(f'Imports, Exports and Balance of {country_info(country).name}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Trade (U$D)')
    ax.grid(alpha=0.5)
    ax.legend()
    return fig, ax

def cross_country_trades(G_Years=None, country_1=None, country_2=None):
    """
        Gets the yearly trade between two countries
        args: G_Years: a list of networkx DiGraphs
              country_1: the name or alpha_2 or alpha_3 code of the first country
              country_2: the name or alpha_2 or alpha_3 code of the second country
        returns: a 2D list, with the first column indicating exports from country_1 to country_2, 
                 and the second column indicating exports from country_2 to country_1, i.e.
                 Exports c1 to c2 | Imports c1 from c2
                      ...         |        ...
                      ...         |        ...
    """
    # get alpha_3 codes
    country_1 = country_info(country_1).alpha_3
    country_2 = country_info(country_2).alpha_3
    # get the yearly trade
    yearly_trade = []
    for G in G_Years.values():
        yearly_trade.append([])
        try: yearly_trade[-1].append(G[country_1][country_2]['weight'])
        except: yearly_trade[-1].append(0)
        try: yearly_trade[-1].append(G[country_2][country_1]['weight'])
        except: yearly_trade[-1].append(0)
    return yearly_trade

def cross_country_trades_graph(G_Years=None, country_1=None, country_2=None):
    """
        Plots the yearly trade between two countries. Simply uses `cross_country_trades` (same args).
        args: Same as `cross_country_trades`
        returns: fig, ax: the figure and axis objects of the plot
    """
    years = list(G_Years.keys())
    yearly_trade = cross_country_trades(G_Years=G_Years, country_1=country_1, country_2=country_2)
    country_1 = country_info(country_1).name
    country_2 = country_info(country_2).name

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years, [trade[0] for trade in yearly_trade], label=f'{country_1} to {country_2}', marker='o')
    ax.plot(years, [trade[1] for trade in yearly_trade], label=f'{country_2} to {country_1}', marker='o')
    ax.grid(alpha=0.5)
    ax.set_xlabel('Year')
    ax.set_ylabel('Trade (USD)')
    ax.legend()
    return fig, ax

def deficit_calculator(G_Years=None, country=None):
    """
        Calculate de deficit of a country by year. Given by the difference between imports and exports.
        A positive deficit indicates a net exporter, and a negative deficit indicates a net importer.
        args: G_Years: a list of networkx DiGraphs
              country: the name or alpha_2 or alpha_3 code of the country
        returns: a list of the deficit for each year
    """
    yearly_trade = country_exports_imports_yearly(G_Years=G_Years, country=country)
    return [trade[0] - trade[1] for trade in yearly_trade]

def deficit_graph(G_Years=None, country=None):
    """
        Plot the deficit of a country (or list of countries) by year.
        args: G_Years: a list of networkx DiGraphs
              country: the name or alpha_2 or alpha_3 code of the country, or a list of countries
        returns: fig, ax (matplotlib)
    """
    if type(country) == str:
        country = [country]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    years = list(G_Years.keys())
    for c in country:
        deficits = deficit_calculator(G_Years=G_Years, country=c)
        ax.plot(years, deficits, label=c, marker='o')
    ax.set_xlabel('Year')
    ax.set_ylabel('Deficit (USD)')
    ax.grid(alpha=0.5)
    ax.legend()
    return fig, ax

def centralities_distribution(e_cent, d_cent, b_cent, c_cent):
    fig, ax = plt.subplots(2, 2, figsize=(18, 12))
    # using the eigenvectors_centralities Pandas DataFrame, plot with years as the x-axis and the eigenvector centralities as the y-axis
    for year in e_cent.columns:
        years_list = [year] * len(e_cent[year])
        ax[0][0].scatter(years_list, e_cent[year], c='cornflowerblue', alpha=0.5, s=8)
        ax[0][1].scatter(years_list, d_cent[year], c='red', alpha=0.5, s=8)
        ax[1][0].scatter(years_list, b_cent[year], c='green', alpha=0.5, s=8)
        ax[1][1].scatter(years_list, c_cent[year], c='orange', alpha=0.5, s=8)

    ax[0][0].set_title('Eigenvector Centralities')
    ax[0][0].set_xlabel('Year')
    ax[0][0].set_ylabel('Eigenvector Centrality')
    ax[0][0].grid(alpha=0.5)
    ax[0][1].set_title('Degree Centralities')
    ax[0][1].set_xlabel('Year')
    ax[0][1].set_ylabel('Degree Centrality')
    ax[0][1].grid(alpha=0.5)
    ax[1][0].set_title('Betweenness Centralities')
    ax[1][0].set_xlabel('Year')
    ax[1][0].set_ylabel('Betweenness Centrality')
    ax[1][0].grid(alpha=0.5)
    ax[1][1].set_title('Closeness Centralities')
    ax[1][1].set_xlabel('Year')
    ax[1][1].set_ylabel('Closeness Centrality')
    ax[1][1].grid(alpha=0.5)

    return fig, ax

# TODO
"""
def networkx_graph():
    G = G_Years['2000']

    node_size = 40
    label_outsize_factor = 2

    # create a layout. it will be circular, with the nodes ordered by degree
    G_layout = {}
    # get the nodes ordered by degree
    nodes = sorted(G.nodes, key=lambda x: G.degree(x), reverse=True)
    # get the radius of the circle
    #radius = 0.5 * np.sqrt(len(nodes))
    radius = 1
    # get the angle between each node
    angle = 2 * np.pi / len(nodes) 
    # get the coordinates of each node. the first node will be at the top of the circle.
    # the nodes should alternate between the left and right sides of the circle. this means
    # that the second node should be on the right, the third on the left, the fourth on the right, etc.
    # this way, the node with smaller degree will be at the bottom of the circle
    for i, node in enumerate(nodes):
        idx = (i+1) // 2
        if i % 2 == 0:
            G_layout[node] = (radius * np.cos(np.pi/2 + idx * angle), radius * np.sin(np.pi/2 + idx * angle))
        else:
            G_layout[node] = (radius * np.cos(np.pi/2 - idx * angle), radius * np.sin(np.pi/2 - idx * angle))

    # draw the graph, only nodes, with labels
    fig, ax = plt.subplots(figsize=(5, 5))
    nx.draw_networkx_nodes(G, G_layout, ax=ax, node_size=node_size)
    # draw edges, making them thinner and more transparent if they have a lower weight
    for ie, edge in enumerate(G.edges):
        if ie % 100 == 0:
            print('\rdrawing edge {}/{}'.format(ie, len(G.edges)), end='')
            weight = G.edges[edge]['weight']
            nx.draw_networkx_edges(G, G_layout, edgelist=[edge], ax=ax, \
                                width=min(0.8, max(0.1, np.log10(weight)/10)), alpha=min(max(0.1, np.log10(weight)/10), 1), edge_color=[(0,0,0)], \
                                arrows=True, arrowsize=5, node_size=node_size)

    # draw the labels. increase the radius of each point in the layout, so that the labels are outside the nodes by a large margin
    G_layout_labels = {node: (label_outsize_factor*x, label_outsize_factor*y) for node, (x, y) in G_layout.items()}
    nx.draw_networkx_labels(G, G_layout_labels, ax=ax, font_size=5)

    # draw a line between the labels and the nodes
    for node, (x, y) in G_layout_labels.items():
        ax.plot([x, G_layout[node][0]], [y, G_layout[node][1]], color='black', linewidth=0.1)

    # export to pdf
    plt.savefig('2000.pdf')

def pygal_interactive_map(G, title=""):
    worldmap = pygal.maps.world.World(style=DarkSolarizedStyle)
    worldmap.title = title
    # add the countries in the network
    trade_partners_count = {}
    for node in G.nodes():
        trade_partners_count[G.nodes[node]['attr_dict']['alpha_2']] = G.degree(node)

    worldmap.add('Trade partners', trade_partners_count)

    worldmap.render_to_file('temp.svg')
    webbrowser.open('temp.svg')
"""