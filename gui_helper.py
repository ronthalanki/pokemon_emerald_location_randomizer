from graph_helper import connect_nodes, draw_graph, find_unexplored_accessible_nodes, shortest_path
import PySimpleGUI as sg
from helper import save_filename_template
from thefuzz import process


CONNECT_BUTTON_KEY = 'key.button.connect'
FIND_PATH_BUTTON_KEY = 'key.button.find_path'
MORE_INFO_TEXT_KEY = 'key.text.more_info'
ONE_WAY_BUTTON_KEY = 'key.button.one_way'
FIND_UNEXPLORED_ACCESSIBLE_WARPS = 'key.button.find_unexplored_accessible_warps'
VIEW_GRAPH_BUTTON_KEY = 'key.button.view_graph'

RIGHT_LAYOUT_MAX_ITEMS = 20


def fuzzy_search_results_pretty_print(list_of_tuples):
    """
    Prints out the results of a fuzzy search.
    """
    return_str = ''
    for i, item in enumerate(list_of_tuples):
        return_str += f'{i + 1}. Location: {item[0]}, Score: {item[1]}\n'

    return return_str


def list_pretty_print(list):
    return_str = ''
    for i, item in enumerate(list):
        return_str += f'{i + 1}. {item}\n'

    return return_str


def gui_layout():
    left_column = __left_column_layout_helper('start') + __left_column_layout_helper('end') + [
        [sg.Button('Connect Locations', key=CONNECT_BUTTON_KEY)],
        [sg.Checkbox('One Way', key=ONE_WAY_BUTTON_KEY)],
        [sg.Button('Find Path', key=FIND_PATH_BUTTON_KEY)],
        [sg.Button('Find Accessible & Unexplored Warps',
                   key=FIND_UNEXPLORED_ACCESSIBLE_WARPS)],
        [sg.Button('DEBUG ONLY - View Graph', key=VIEW_GRAPH_BUTTON_KEY)],
    ]

    right_column = [
        [sg.Text(size=(100, 20), key=MORE_INFO_TEXT_KEY)],
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
        [sg.Text(input_type)],
        [sg.In(size=(50, 1), enable_events=True,
               key=f'key.input.{input_type}')],
        [sg.Text(size=(100, 20), key=f'key.text.{input_type}')],
    ]


def gui_loop(window, G, unexplored_locations, playthrough_id):
    current_best_fuzzy_results_start = None
    current_best_fuzzy_results_end = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'key.input.start':
            current_best_fuzzy_results_start = __handle_fuzzy_input_helper(
                window, values, G, 'start')
        elif event == 'key.input.end':
            current_best_fuzzy_results_end = __handle_fuzzy_input_helper(
                window, values, G, 'end')
        elif event == CONNECT_BUTTON_KEY:
            connect_nodes(
                G, unexplored_locations, current_best_fuzzy_results_start, current_best_fuzzy_results_end, values[ONE_WAY_BUTTON_KEY])
            f = open(save_filename_template(playthrough_id), 'a')
            f.write(
                current_best_fuzzy_results_start + ',' + current_best_fuzzy_results_end + '\n')
            f.close()

            draw_graph(G)
        elif event == FIND_PATH_BUTTON_KEY:
            path = shortest_path(
                G, current_best_fuzzy_results_start, current_best_fuzzy_results_end)
            window[MORE_INFO_TEXT_KEY].update(f'Shortest Path: {path}')
        elif event == FIND_UNEXPLORED_ACCESSIBLE_WARPS:
            unexplored_accessible_nodes = find_unexplored_accessible_nodes(
                G, unexplored_locations, current_best_fuzzy_results_start)
            window[MORE_INFO_TEXT_KEY].update(list_pretty_print(
                unexplored_accessible_nodes[:RIGHT_LAYOUT_MAX_ITEMS]))
        elif event == VIEW_GRAPH_BUTTON_KEY:
            draw_graph(G)

    window.close()


def __handle_fuzzy_input_helper(window, values, G, input_type: str):
    if values[f'key.input.{input_type}']:
        fuzzy_search_results = process.extract(
            values[f'key.input.{input_type}'], list(G.nodes), limit=10)
        window[f'key.text.{input_type}'].update(
            fuzzy_search_results_pretty_print(fuzzy_search_results))
        return fuzzy_search_results[0][0]
