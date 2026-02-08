def parse_graph(input_text: str) -> dict[str, list[str]]:
    """
    Create an internal representation of a graph from the given text input.

    Supported input formats:
        - Each line represents a directed edge between two nodes separated with a space ( `node1 node2` ).
        - Each line represents a node and all of its neighbors separated with spaces ( `node1 nb1 nb2 ...` ).

    Lines starting with `#` are ignored.

    ------

    Arguments:
        input_text: String containing graph information.

    ------

    Returns:
        A directed graph in dictionary form where each key is a node and each value is a list of neighbors.

    ------

    Raises:
        ValueError: If the input is invalid.
    """

    graph = {}

    for num, line in enumerate(input_text.strip().split('\n'), start = 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        nodes = line.split(' ')
        if not nodes:
            raise ValueError(f'Invalid input format at line {num}: {line}')

        node, neighbors = nodes[0], nodes[1:]
        if node not in graph:
            graph[node] = []

        for neighbor in neighbors:
            graph[node].append(neighbor)
            if neighbor not in graph:
                graph[neighbor] = []

    if not graph:
        raise ValueError('Invalid input.')

    return graph


def format_output(paths: list[list[str]]) -> str | None:
    """
    Format the given paths for display on the site.

    ------

    Arguments:
         paths: A list of paths.

    ------

    Returns:
        A formatted string of the same paths, or None if the given list is empty.
    """

    if not paths:
        return None

    output = f'Num\tLen\tPath\n'
    for idx, path in enumerate(paths, start = 1):
        pstr = ' → '.join(map(str, path))
        output += f'{idx:3}\t{len(path):3}\t{pstr}\n'

    return output


def init_computation_state(graph: dict[str, list[str]]) -> dict[str, ...]:
    """
    Initialize the computation state for graph coverage.

    ------

    Arguments:
        graph: A directed graph, as returned from `parse_graph()`.

    ------

    Returns:
        A newly initialized computation state.
    """

    return {
        'graph' : graph,
        'paths' : [],
        'iteration' : 0,
        'progress' : ''
    }


def _step_prime_paths(state: dict[str, ...], max_iters: int = 100) -> dict[str, ...]:
    """
    Execute one iteration of the prime paths computation.

    ------

    Arguments:
        state: The computation state from the previous step.
        max_iters: Maximum number of iterations before raising an error. Set to -1 to remove
                   the limit. Defaults to 100.

    ------

    Returns:
        The updated state.

    ------

    Raises:
        RuntimeError: If the maximum number of iterations is reached.
    """

    if state['progress'] in ['computed', 'cleaned']:
        return state

    graph, paths, iteration = state['graph'], state['paths'], state['iteration']

    if iteration == 0:
        paths = [[node] for node in graph]

    iteration += 1
    if iteration == max_iters:
        raise RuntimeError('Maximum iterations reached.')

    made_changes = False
    for idx in range(len(paths)):
        path = paths[idx]
        pcpy = path.copy()
        pset = set(path)

        if len(pset) != len(path):
            continue  # Path contains duplicate nodes, skip.

        node = path[-1]
        neighbors = graph[node]
        has_one_neighbor = len(neighbors) == 1
        split_path = False

        for neighbor in neighbors:
            if neighbor in pset and neighbor != path[0]:
                continue  # path + neighbor creates a cycle, skip.

            if has_one_neighbor:
                path.append(neighbor)

            elif split_path:
                paths.append(pcpy + [neighbor])

            else:
                path.append(neighbor)
                split_path = True

            made_changes = True

    state['paths'], state['iteration'] = paths, iteration
    state['progress'] = 'computed' if not made_changes else f'Iteration {iteration}: Found {len(paths)} prime paths.'

    return state


def _cleanup_prime_paths(state: dict[str, ...]) -> dict[str, ...]:
    """
    Remove all sub-paths from the computed prime paths.

    ------

    Arguments:
        state: The state after computing prime paths.

    ------

    Returns:
        The final state with prime paths.
    """

    if state['progress'] == 'cleaned':
        return state

    paths = state['paths']
    paths = sorted([' '.join(path) for path in paths], key = len)

    for i in range(len(paths)):
        path = paths[i]

        for j in range(i + 1, len(paths)):
            if path in paths[j]:
                paths[i] = ''  # paths[i] is a sub-path of paths[j], remove it.
                break

    paths = [path.split(' ') for path in paths if path]
    paths.sort(key = lambda x: (len(x), x))

    state['paths'], state['progress'] = paths, 'cleaned'
    return state


def compute_prime_paths(graph: dict[str, list[str]], max_iters: int = 100) -> list[list[str]]:
    """
    Compute prime paths for the given directed graph.

    ------

    Arguments:
        graph: A dictionary representing a directed graph where each key is a node and each
               value is a list of neighbors.
        max_iters: Maximum number of iterations before raising an error. Set to -1 to remove
                   the limit. Defaults to 100.

    ------

    Returns:
        A list with all prime paths.

    ------

    Raises:
        RuntimeError: If the maximum number of iterations is reached.
    """

    state = init_computation_state(graph)

    while True:
        state = _step_prime_paths(state, max_iters)

        if state['progress'] == 'computed':
            print('Finished computing potential prime paths.')
            break

        print(state['progress'])

    print('Removing sub-paths...')
    state = _cleanup_prime_paths(state)
    print('Finished removing sub-paths.')

    paths = state['paths']
    print(f'\nFound a total of {len(paths)} prime paths:')
    print(format_output(paths))

    return state['paths']


def _step_edge_pairs(state: dict[str, ...], max_iters: 100):
    """
    Execute one iteration of the edge pairs computation.

    ------

    Arguments:
        state: The computation state from the previous step.
        max_iters: Maximum number of iterations before raising an error. Set to -1 to remove
                   the limit. Defaults to 100.

    ------

    Returns:
        The updated state.

    ------

    Raises:
        RuntimeError: If the maximum number of iterations is reached.
    """

    if state['progress'] in ['computed', 'cleaned']:
        return state

    graph, paths, iteration = state['graph'], state['paths'], state['iteration']

    if iteration == 0:
        state['remaining_nodes'] = list(graph)

    iteration += 1
    if iteration == max_iters:
        raise RuntimeError('Maximum iterations reached.')

    node = state['remaining_nodes'][0]
    for neighbor1 in graph[node]:
        for neighbor2 in graph[neighbor1]:
            paths.append([node, neighbor1, neighbor2])

    state['remaining_nodes'].pop(0)

    state['paths'], state['iteration'] = paths, iteration
    state['progress'] = 'computed' if not state['remaining_nodes'] \
                        else f'Iteration {iteration}: Found {len(paths)} edge pairs.'

    return state


def compute_edge_pairs(graph: dict[str, list[str]], max_iters: int = 100) -> list[list[str]]:
    """
    Compute edge pairs for the given directed graph.

    ------

    Arguments:
        graph: A dictionary representing a directed graph where each key is a node and each
               value is a list of neighbors.
        max_iters: Maximum number of iterations before raising an error. Set to -1 to remove
                   the limit. Defaults to 100.

    ------

    Returns:
        A list with all edge pairs.

    ------

    Raises:
        RuntimeError: If the maximum number of iterations is reached.
    """

    state = init_computation_state(graph)

    while True:
        state = _step_edge_pairs(state, max_iters)

        if state['progress'] == 'computed':
            print('Finished computing edge pairs.')
            break

        print(state['progress'])

    paths = state['paths']
    print(f'\nFound a total of {len(paths)} edge pairs:')
    print(format_output(paths))

    return state['paths']
