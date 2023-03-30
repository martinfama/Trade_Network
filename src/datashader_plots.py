import datashader as ds
import datashader.transfer_functions as tf
from datashader.layout import random_layout, circular_layout, forceatlas2_layout
from datashader.bundling import connect_edges, hammer_bundle

G_2000_pd_nodes = pd.DataFrame()
# make a dataframe of the nodes, by having the node names in the one and only column. have the index start at 1
G_2000_pd_nodes['name'] = list(G_Years['2000'].nodes)
#G_2000_pd_nodes.index = G_2000_pd_nodes.index + 1

country_index_map = dict(zip(G_2000_pd_nodes['name'], G_2000_pd_nodes.index))

G_2000_pd_edges = pd.DataFrame(columns=['source', 'target'])
# make a dataframe of the edges, by having the source and target in the columns. use the indeces of the nodes, not the names
G_2000_pd_edges['source'] = [country_index_map[edge[0]] for edge in list(G_Years['2000'].edges)]
G_2000_pd_edges['target'] = [country_index_map[edge[1]] for edge in list(G_Years['2000'].edges)]
G_2000_pd_edges['weight'] = [G_Years['2000'][edge[0]][edge[1]]['weight'] for edge in list(G_Years['2000'].edges)]

 # create a layout. it will be circular, with the nodes ordered by degree
G_2000_circ_layout = {}
# get the nodes ordered by degree
nodes = sorted(G_Years['2000'].nodes, key=lambda x: G_Years['2000'].degree(x), reverse=True)
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
        G_2000_circ_layout[node] = (radius * np.cos(np.pi/2 + idx * angle), radius * np.sin(np.pi/2 + idx * angle))
    else:
        G_2000_circ_layout[node] = (radius * np.cos(np.pi/2 - idx * angle), radius * np.sin(np.pi/2 - idx * angle))

# copy the G_2000_nodes dataframe, and add the x and y coordinates from the layout
G_2000_pd_nodes_circ = G_2000_pd_nodes.copy()
G_2000_pd_nodes_circ['x'] = [G_2000_circ_layout[node][0] for node in G_2000_pd_nodes_circ['name']]
G_2000_pd_nodes_circ['y'] = [G_2000_circ_layout[node][1] for node in G_2000_pd_nodes_circ['name']]

cvsopts = dict(plot_height=800, plot_width=800)

def nodesplot(nodes, name=None, canvas=None, cat=None):
    canvas = ds.Canvas(**cvsopts) if canvas is None else canvas
    aggregator=None if cat is None else ds.count_cat(cat)
    agg=canvas.points(nodes,'x','y',aggregator)
    return tf.spread(tf.shade(agg, cmap=["#FF3333"]), px=3, name=name)

def edgesplot(edges, name=None, canvas=None):
    canvas = ds.Canvas(**cvsopts) if canvas is None else canvas
    return tf.shade(canvas.line(edges, 'x','y', agg=ds.count()), name=name)
    
def graphplot(nodes, edges, name="", canvas=None, cat=None):
    if canvas is None:
        xr = nodes.x.min(), nodes.x.max()
        yr = nodes.y.min(), nodes.y.max()
        canvas = ds.Canvas(x_range=xr, y_range=yr, **cvsopts)
        
    np = nodesplot(nodes, name + " nodes", canvas, cat)
    ep = edgesplot(edges, name + " edges", canvas)
    return tf.stack(ep, np, how="over", name=name)

cd_b = graphplot(G_2000_pd_nodes_circ, hammer_bundle(G_2000_pd_nodes_circ, G_2000_pd_edges), "Force-directed, bundled")