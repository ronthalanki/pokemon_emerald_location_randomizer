import argparse
import os

from helper import get_new_playthrough_id, save_filename_template
from graph_helper import connect_nodes, generate_graph
from gui_helper import gui_layout, gui_loop


def main(playthrough_id):
    G = generate_graph()
    unexplored_locations = set(G.nodes())

    # Reconnect all the nodes found from the previous playthrough
    save_filename = save_filename_template(playthrough_id)
    if os.path.exists(save_filename):
        f = open(save_filename)
        for line in f:
            start, end = line.split(',')
            connect_nodes(G, unexplored_locations, start, end)

    """
    If you update the tools you have, we need to update the graph
    
    Teleport = Connect all Pokemon Center to city center
    Mach Bike = Connect certain warps
    Surf = Connect certain regions (Pacifidlog -> Slateport)
    Fly = Connect all cities 
    Rock Smash, Strength, Waterfall, Pokemon Level = Certain warps should now be explored
    Go-Goggles

    TODO: how to handle event where people are blocking the path for Lilycove Aqua Hideout, Mauville, near Safari Zone, Weather Instititute? I think we should immediately connect the pieces
    TODO: how to handle Sky Pillar event
    TODO: Shoal Cave
    TODO: Storage Key
    """

    # Button to notate what is blocking you from searching certain nodes
    # Find nearest pokecenter
    # Click a button to figure out what location you are at
    # Refresh button for another short path
    # View graph button
    # Add pictures for each region
    # If you already connected a node, then display a warning before connecting it again
    # Find region that has the most unexplored nodes
    # Handle user mistakes and display a warning (e.g. user tries to connect a warp to multiple other warps)
    # Currently Accessible/Inaccessible warp list
    # Click an item on the accessible but unexplored list and that will find the shortest path to that location
    # Sort the accessible but unexplored list by shortest path

    window = gui_layout()
    gui_loop(window, G, unexplored_locations, playthrough_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--playthrough_id', type=int,
                        default=get_new_playthrough_id())

    args = parser.parse_args()
    main(args.playthrough_id)
