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
    __add_edge(G, 'Mirage Tower 2F N', 'Mirage Tower 1F')
    __add_edge(G, 'Mirage Tower 2F S', 'Mirage Tower 1F')
    __add_edge(G, 'Mirage Tower 3F E', 'Mirage Tower 2F N')
    __add_edge(G, 'Mirage Tower 3F E', 'Mirage Tower 1F')
    __add_edge(G, 'Mt Pyre 1F Ceiling', 'Mt Pyre 1F')
    __add_edge(G, 'Mt Pyre 2F Ceiling 1', 'Mt Pyre 2F')
    __add_edge(G, 'Mt Pyre 2F Ceiling 2', 'Mt Pyre 2F')
    __add_edge(G, 'Mt Pyre 3F Ceiling', 'Mt Pyre 3F')
    __add_edge(G, 'Mt Pyre 4F Ceiling', 'Mt Pyre 4F')
    __add_edge(G, 'Mt Pyre 5F Ceiling', 'Mt Pyre 5F')
    __add_edge(G, 'Magma Hideout 1F C', 'Magma Hideout 1F SE')
    __add_edge(G, 'Seafloor Cavern R3 NW', 'Seafloor Cavern R3')
    __add_edge(G, 'Seafloor Cavern R3 NW', 'Seafloor Cavern R3 S')
    __add_edge(G, 'Seafloor Cavern R3', 'Seafloor Cavern R3 S')
    __add_edge(G, 'Seafloor Cavern R6', 'Seafloor Cavern R6 SW')
    __add_edge(G, 'Sky Pillar 4F Down', 'Sky Pillar 3F C')
    __add_edge(G, 'Sky Pillar 4F', 'Sky Pillar 3F')
    __add_edge(G, 'Victory Road B1F SW Room NE', 'Victory Road B1F SW Room SW')
    __add_edge(G, 'Victory Road B1F SE', 'Victory Road B1F')
    __add_edge(G, 'Victory Road B2F NE', 'Victory Road B2F SE')
    __add_edge(G, 'R115 Meteor Falls Exit', 'Rustboro')

    return G


def update_graph_with_gogoggles(G):
    __add_edge(G, 'Lavaridge', 'Desert')
    __add_edge(G, 'Fallarbor', 'Desert')


def update_graph_with_surf(G):
    __add_edge(G, 'Pacifidlog', 'Slateport')
    __add_dedge(G, 'Lilycove', 'Lilycove Aqua Hideout')
    __add_dedge(G, 'Lilycove', 'Mossdeep')
    __add_dedge(G, 'Mossdeep', 'Pacifidlog')

    __add_dedge(G, 'Sootopolis')
    __add_dedge(G, 'Sootopolis', 'Sootopolis West')
    __add_dedge(G, 'Sootopolis', 'Sootopolis Gym')

    __add_dedge(G, 'Meteor Falls B1F Right N', 'Meteor Falls B1F Right S')
    __add_dedge(G, 'Meteor Falls B1F Right N', 'Meteor Falls B1F Right W')
    __add_dedge(G, 'Meteor Falls B1F Right S', 'Meteor Falls B1F Right W')

    __add_dedge(G, 'Slateport/Mauville/Verdanturf', 'Route 119/123')

    __add_dedge(G, 'Seafloor Cavern R5 N', 'Seafloor Cavern R5 S')
    __add_edge(G, 'Seafloor Cavern R5 N', 'Seafloor Cavern R5 C')
    __add_edge(G, 'Seafloor Cavern R5 S', 'Seafloor Cavern R5 C')

    __add_dedge(G, 'Victory Road B2F SW', 'Victory Road B2F C')
    __add_edge(G, 'Victory Road B2F SE', 'Victory Road B2F NE')

    __add_edge(G, 'Pacifidlog', 'Slateport', weight=100)
    __add_dedge(G, 'Western Waters', 'Dewford', weight=100)
    __add_dedge(G, 'Western Waters', 'Slateport', weight=100)
    __add_dedge(G, 'Western Waters', 'Petalburg', weight=100)
    __add_dedge(G, 'Eastern Waters', 'Pacifidlog', weight=100)
    __add_dedge(G, 'Eastern Waters', 'Mossdeep', weight=100)
    __add_dedge(G, 'Eastern Waters', 'Lilycove', weight=100)
    __add_dedge(G, 'Western Waters', 'R105 Regice', weight=100)
    __add_dedge(G, 'Western Waters', 'R108 Abandoned Ship', weight=100)
    __add_dedge(G, 'Eastern Waters', 'R131 Sky Pillar', weight=100)

    __add_dedge(G, 'Slateport/Mauville/Verdanturf', 'R110 New Mauville')
    __add_edge(G, 'Rustboro', 'R115 Meteor Falls Exit')
    __add_dedge(G, 'Eastern Waters', 'R124 Treasure Hunter')
    __add_dedge(G, 'Fortree/Lilycove', 'R120 Scorched Slab')
    __add_dedge(G, 'Fortree/Lilycove', 'R122 Mt. Pyre')


def update_graph_with_rock_smash(G):
    __add_dedge(G, 'Slateport/Mauville/Verdanturf', 'R112')
    __add_dedge(G, 'Rusturf Tunnel W', 'Rusturf Tunnel')
    __add_dedge(G, 'Mirage Tower 3F E', 'Mirage Tower 3F W')


def update_graph_with_strength(G):
    __add_edge(G, 'Magma Hideout 1F C', 'Magma Hideout 1F SW')
    __add_dedge(G, 'Magma Hideout 1F SE', 'Magma Hideout 1F SW')
    __add_dedge(G, 'Seafloor Cavern R4 NW', 'Seafloor Cavern R4 SW')
    __add_edge(G, 'Seafloor Cavern R6 SW', 'Seafloor Cavern R6')


def update_graph_with_rock_smash_and_strength(G):
    __add_dedge(G, 'Seafloor Cavern R1 SW', 'Seafloor Cavern R1')
    __add_dedge(G, 'Seafloor Cavern R2 N', 'Seafloor Cavern R2 S')
    __add_dedge(G, 'Seafloor Cavern R2 N', 'Seafloor Cavern R2 SE')
    __add_dedge(G, 'Seafloor Cavern R2 S', 'Seafloor Cavern R2 SE')
    __add_dedge(G, 'Seafloor Cavern R4 SE', 'Seafloor Cavern R4 SW')
    __add_dedge(G, 'Seafloor Cavern R4 SE', 'Seafloor Cavern R4 NW')
    __add_edge(G, 'Seafloor Cavern R4 SE', 'Seafloor Cavern R4 NE')
    __add_edge(G, 'Seafloor Cavern R4 NW', 'Seafloor Cavern R4 NE')
    __add_dedge(G, 'Victory Road B1F SW Room NE', 'Victory Road B1F SW Room E')
    __add_edge(G, 'Victory Road B1F SW Room E', 'Victory Road B1F SW Room SW')


def update_graph_with_bike(G):
    __add_dedge(G, 'Granite Cave B1F Ledge NE', 'Granite Cave B1F Ledge N')
    __add_dedge(G, 'Granite Cave B1F Ledge N', 'Granite Cave B1F Ledge NW')
    __add_edge(G, 'Granite Cave B1F', 'Granite Cave B1F Ledge NW')
    __add_edge(G, 'Jagged Pass S', 'Jagged Pass')
    __add_edge(G, 'Mirage Tower 2F N', 'Mirage Tower 2F S')


def update_graph_with_dive(G):
    __add_dedge(G, 'Eastern Waters', 'Sootopolis', weight=100)
    __add_dedge(G, 'Eastern Waters', 'R128 Seafloor Cavern', weight=100)


def update_graph_with_waterfall(G):
    __add_edge(G, 'Meteor Falls 1F', 'Meteor Falls 1F N')
    __add_dedge(G, 'Victory Road B2F SW', 'Victory Road B2F NE')
    __add_dedge(G, 'Victory Road B2F SW', 'Victory Road B2F SE')
    __add_dedge(G, 'Victory Road B2F C', 'Victory Road B2F NE')
    __add_dedge(G, 'Victory Road B2F C', 'Victory Road B2F SE')

    __add_dedge(G, 'Eastern Waters', 'Ever Grande', weight=100)


def update_graph_with_teleport(G):
    __add_edge(G, 'Oldale Pokecenter', 'Oldale')
    __add_edge(G, 'Petalburg Pokecenter', 'Petalburg')
    __add_edge(G, 'Rustboro Pokecenter', 'Rustboro')
    __add_edge(G, 'Dewford Pokecenter', 'Dewford')
    __add_edge(G, 'Slateport Pokecenter', 'Slateport')
    __add_edge(G, 'Mauville Pokecenter', 'Mauville')
    __add_edge(G, 'Verdanturf Pokecenter', 'Verdanturf')
    __add_edge(G, 'Fallarbor Pokecenter', 'Fallarbor')
    __add_edge(G, 'Fortree Pokecenter', 'Fortree')
    __add_edge(G, 'Lilycove Pokecenter', 'Lilycove')
    __add_edge(G, 'Mossdeep Pokecenter', 'Mossdeep')
    __add_edge(G, 'Sootopolis Pokecenter', 'Sootopolis')
    __add_edge(G, 'Pacifidlog Pokecenter', 'Pacifidlog')


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
