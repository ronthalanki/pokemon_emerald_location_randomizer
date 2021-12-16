from graph_helper import connect_nodes, draw_graph, generate_graph, shortest_path
from gui_helper import fuzzy_search_results_pretty_print
from icecream import ic
import PySimpleGUI as sg
from thefuzz import process


def main():
    G = generate_graph()
    playthrough_id = '1'

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

    # You can click a button and it will show you the regions that you have not yet explored
    # Find nearest pokecenter
    # Click a button to figure out what location you are at
    # Click a button to load previous playthrough
    # Refresh button for shortest path
    # Button to notate what is blocking you from searching certain nodes
    # checkbox for one-way when we connect two nodes
    # find all non-explored but accessible nodes

    left_column = [
        [sg.Text('Start')],
        [sg.In(size=(50, 1), enable_events=True, key='-INPUT-START-')],
        [sg.Text(size=(100, 20), key="-TEXT-START-")],
        [sg.Text('End')],
        [sg.In(size=(50, 1), enable_events=True, key='-INPUT-END-')],
        [sg.Text(size=(100, 20), key="-TEXT-END-")],
        [sg.Button('Connect Locations', key='-CONNECT-')],
        [sg.Button('Find Path', key='-FIND-PATH-')],
    ]

    right_column = [
        [sg.Text(size=(100, 20), key='-TEXT-MORE-INFO-')],
    ]

    layout = [
        [
            sg.Column(left_column),
            sg.VSeperator(),
            sg.Column(right_column),
        ]
    ]

    window = sg.Window(
        'Pokemon Emerald Location Randomizer Helper', layout, margins=(200, 200))

    current_best_fuzzy_results_start = None
    current_best_fuzzy_results_end = None

    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WIN_CLOSED:
            break
        elif event == '-INPUT-START-':
            if values['-INPUT-START-']:
                fuzzy_search_results = process.extract(
                    values['-INPUT-START-'], list(G.nodes), limit=10)
                current_best_fuzzy_results_start = fuzzy_search_results[0]
                window['-TEXT-START-'].update(
                    fuzzy_search_results_pretty_print(fuzzy_search_results))
        elif event == '-INPUT-END-':
            if values['-INPUT-END-']:
                fuzzy_search_results = process.extract(
                    values['-INPUT-END-'], list(G.nodes), limit=10)
                current_best_fuzzy_results_end = fuzzy_search_results[0]
                window['-TEXT-END-'].update(
                    fuzzy_search_results_pretty_print(fuzzy_search_results))
        elif event == '-CONNECT-':
            ic(f'Connect {current_best_fuzzy_results_start} with {current_best_fuzzy_results_end}')

            connect_nodes(
                G, current_best_fuzzy_results_start[0], current_best_fuzzy_results_end[0])
            f = open(f'out/playthrough{playthrough_id}.csv', 'a')
            f.write(
                current_best_fuzzy_results_start[0] + ',' + current_best_fuzzy_results_end[0] + '\n')
            f.close()

            draw_graph(G)
        elif event == '-FIND-PATH-':
            ic(f'Find path from {current_best_fuzzy_results_start} to {current_best_fuzzy_results_end}')
            path = shortest_path(
                G, current_best_fuzzy_results_start[0], current_best_fuzzy_results_end[0])
            window['-TEXT-MORE-INFO-'].update(f'Shortest Path: {path}')

    window.close()


if __name__ == '__main__':
    main()
