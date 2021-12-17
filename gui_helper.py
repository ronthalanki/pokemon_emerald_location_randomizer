from graph_helper import connect_nodes, draw_graph, shortest_path
import icecream as ic
import PySimpleGUI as sg
from thefuzz import process


def fuzzy_search_results_pretty_print(list_of_tuples):
    """
    Prints out the results of a fuzzy search.
    """
    return_str = ''
    for i, item in enumerate(list_of_tuples):
        return_str += f'{i}. Location: {item[0]}, Score: {item[1]}\n'

    return return_str


def gui_layout():
    left_column = __left_column_layout_helper('start') + __left_column_layout_helper('end') + [
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

    return sg.Window(
        'Pokemon Emerald Location Randomizer Helper', layout, margins=(200, 200))


def __left_column_layout_helper(input_type: str):
    return [
        [sg.Text(input_type)]
        [sg.In(size=(50, 1), enable_events=True,
               key=f'-INPUT-{input_type.upper()}-')],
        [sg.Text(size=(100, 20), key=f'-TEXT-{input_type.upper()}-')],
    ]


def gui_loop(window, G, playthrough_id):
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
