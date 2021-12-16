
def fuzzy_search_results_pretty_print(list_of_tuples):
    """
    Prints out the results of a fuzzy search.
    """
    return_str = ''
    for i, item in enumerate(list_of_tuples):
        return_str += f'{i}. Location: {item[0]}, Score: {item[1]}\n'
    
    return return_str
