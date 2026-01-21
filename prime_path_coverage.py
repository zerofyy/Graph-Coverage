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
    """

    graph = {}

    for num, line in enumerate(input_text.strip().split('\n'), start = 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        nodes = line.split(' ')
        if not nodes:
            raise Exception(f'Invalid input format at line {num}: {line}')

        node, neighbors = nodes[0], nodes[1:]
        if node not in graph:
            graph[node] = []

        for neighbor in neighbors:
            graph[node].append(neighbor)
            if neighbor not in graph:
                graph[neighbor] = []

    if not graph:
        raise Exception(f'Invalid input.')

    return graph


def compute_prime_paths(graph: dict[str, list[str]]) -> dict[str, str | list[list[str]]]:
    """
    Compute prime paths for the given directed graph.

    ------

    Arguments:
        graph: A dictionary representing a directed graph
               where each key is a node and each value is a list of neighbors.

    ------

    Returns:
        A dictionary containing the prime paths and debug information.
    """

    debug, counter = '', 0
    paths = [[node] for node in graph]

    while True:
        counter += 1
        debug += f'Iteration {counter}:\n'

        if counter == 100_000:
            raise Exception('Maximum iterations reached.')

        made_changes = False
        for idx in range(len(paths)):
            path = paths[idx]
            pcpy = path.copy()
            pset = set(path)

            if len(pset) != len(path):
                debug += f'| {pcpy} contains duplicate nodes, skipped.\n'
                continue

            node = path[-1]
            neighbors = graph[node]
            has_one_neighbor = len(neighbors) == 1
            split_path = False

            for neighbor in neighbors:
                if neighbor in pset and neighbor != path[0]:
                    debug += f'| {pcpy} + [\'{neighbor}\'] creates a cycle, skipped.\n'
                    continue

                if has_one_neighbor:
                    path.append(neighbor)
                    debug += f'| {pcpy} ──▶ {path}\n'

                elif split_path:
                    paths.append(pcpy + [neighbor])
                    debug += f'| {" " * len(str(pcpy))} └─▶ {paths[-1]}\n'

                else:
                    path.append(neighbor)
                    split_path = True
                    debug += f'| {pcpy} ──▶ {path}\n'

                made_changes = True

        debug += '\n'
        if not made_changes:
            debug += 'Done.\n\n'
            break

    debug += 'Removing sub-paths...\n'
    num_paths = len(paths)
    for i in range(num_paths):
        path = str(paths[i])[1 : -1]

        for j in range(num_paths):
            if i == j:
                continue

            if path in str(paths[j]):
                debug += f'| {paths[i]} ──▶ {paths[j]}\n'
                paths[i].clear()
                break
    debug += '\nDone.'

    paths = [path for path in paths if path]
    paths.sort(key = lambda x: (len(x), x))
    return {'paths' : paths, 'debug' : debug}


def format_output(paths: list[list[str]]) -> str:
    """
    Format the given prime paths for display on the site.

    ------

    Arguments:
         paths: A list of prime paths.

    ------

    Returns:
        A formatted string of the same prime paths.
    """

    if not paths:
        return 'No prime paths found.'

    output = f'Found {len(paths)} prime path(s):\n' \
             f'Num\tLen\tPath\n'
    for idx, path in enumerate(paths, start = 1):
        pstr = ' → '.join(map(str, path))
        output += f'{idx:3}\t{len(path):3}\t{pstr}\n'

    return output
