import networkx as nx
import matplotlib.pyplot as plt
import re


def generate_graph():
    """
    Generates a graph based on the locations.txt file.
    """
    G = nx.DiGraph()
    regions = []
    with open('./locations.txt') as f:
        for line in f:
            line = __remove_whitespace(line)
            line = line.split(',')
            regions.append(line)

    for region in regions:
        __add_node(G, region[0])
        for warp in region[1:]:
            __add_node(G, warp)

            # Add edges between warps that are in the same region
            __add_dedge(G, region[0], warp)

    # Hardcoded rules (this is to handle one-way cases)
    __add_edge(G, 'Lavaridge', 'R112')
    __add_edge(G, 'Desert', 'R112')
    __add_edge(G, 'Desert', 'Lavaridge')
    __add_edge(G, 'Desert', 'Fallarbor')
    __add_edge(G, 'Granite Cave B2F E', 'Granite Cave B2F W')
    __add_edge(G, 'Granite Cave 1F Ledge', 'Granite Cave 1F')
    __add_edge(G, 'Granite Cave B1F Ledge NE', 'Granite Cave B2F E')
    __add_edge(G, 'Granite Cave B1F Ledge N', 'Granite Cave B2F W')
    __add_edge(G, 'Granite Cave B1F Ledge NW', 'Granite Cave B2F W')
    __add_edge(G, 'Granite Cave B1F Ledge NW', 'Granite Cave B1F')
    __add_edge(G, 'Jagged Pass', 'Jagged Pass S')
    __add_edge(G, 'Meteor Falls 1F N', 'Meteor Falls 1F')

    return G


def update_graph_with_gogoggles(G):
    __add_edge(G, 'Lavaridge', 'Fallarbor')
    __add_edge(G, 'Lavaridge', 'Desert')
    __add_edge(G, 'Fallarbor', 'Desert')


def update_graph_with_surf(G):
    __add_edge(G, 'Pacifidlog', 'Slateport')
    __add_dedge(G, 'Lilycove', 'Lilycove Aqua Hideout')
    __add_dedge(G, 'Lilycove', 'Mossdeep')
    __add_dedge(G, 'Mossdeep', 'Pacifidlog')

    __add_dedge(G, 'Sootopolis East', 'Sootopolis West')
    __add_dedge(G, 'Sootopolis East', 'Sootopolis Gym')
    __add_dedge(G, 'Sootopolis West', 'Sootopolis Gym')

    __add_dedge(G, 'Meteor Falls B1F Right N', 'Meteor Falls B1F Right S')
    __add_dedge(G, 'Meteor Falls B1F Right N', 'Meteor Falls B1F Right W')
    __add_dedge(G, 'Meteor Falls B1F Right S', 'Meteor Falls B1F Right W')


def update_graph_with_rock_smash(G):
    __add_dedge(G, 'Slateport/Mauville/Verdanturf', 'R112')
    __add_dedge(G, 'Rusturf Tunnel W', 'Rusturf Tunnel')


def update_graph_with_bike(G):
    __add_dedge(G, 'Granite Cave B1F Ledge NE', 'Granite Cave B1F Ledge N')
    __add_dedge(G, 'Granite Cave B1F Ledge N', 'Granite Cave B1F Ledge NW')
    __add_edge(G, 'Granite Cave B1F', 'Granite Cave B1F Ledge NW')
    __add_edge(G, 'Jagged Pass S', 'Jagged Pass')


def update_graph_with_waterfall(G):
    __add_edge(G, 'Meteor Falls 1F', 'Meteor Falls 1F N')


def connect_nodes(G, start, end, one_way=False):
    start = __remove_whitespace(start)
    end = __remove_whitespace(end)

    if one_way:
        __add_edge(G, start, end)
    else:
        __add_dedge(G, start, end)


def shortest_path(G, start, end):
    # TODO: remove main region name from the path list
    start = __remove_whitespace(start)
    end = __remove_whitespace(end)

    return nx.shortest_path(G, start, end)


def draw_graph(graph):
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()


def __remove_whitespace(string):
    # return re.sub(r'\s+', '', string)
    return string.strip()

def __add_node(G, node):
    node = __remove_whitespace(node)
    G.add_node(node)

def __add_edge(G, node1, node2):
    node1 = __remove_whitespace(node1)
    node2 = __remove_whitespace(node2)
    G.add_edge(node1, node2)


def __add_dedge(G, node1, node2):
    """
    Adds bidirectional edge between two nodes.
    """
    node1 = __remove_whitespace(node1)
    node2 = __remove_whitespace(node2)
    G.add_edge(node1, node2)
    G.add_edge(node2, node1)
