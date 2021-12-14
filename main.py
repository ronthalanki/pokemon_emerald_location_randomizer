from helper import connect_nodes, draw_graph, generate_graph, shortest_path
from icecream import ic

def main():
    G = generate_graph()
    
    connect_nodes(G, 'Oldale Mart', 'Rusturf Tunnel W')
    connect_nodes(G, 'Lilycove Contest', 'Briney\'s House')
    ic(list(G.nodes))
    ic(shortest_path(G, 'Fortree Gym', 'Rusturf Tunnel S'))
    draw_graph(G)


    """
    If you update the tools you have, we need to update the graph
    
    Teleport = Connect all Pokemon Center to city center
    Mach Bike = Connect certain warps
    Surf = Connect certain regions (Pacifidlog -> Slateport)
    Fly = Connect all cities 
    Rock Smash, Strength, Waterfall, Pokemon Level = Certain warps should now be explored
    Go-Goggles

    TODO: how to handle event where people are blocking the path for Lilycove Aqua Hideout, Mauville, near Safari Zone? I feel like we could adds weights for edges
    """

    # You can click a button and it will show you the path to the warp
    # You can click a button and it will show you the regions that you have not yet explored
    # Find nearest pokecenter
    # Click a button to figure out what location you are at

if __name__ == '__main__':
    main()
