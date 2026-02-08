<h1 align="center">
  Zerofy's Graph Coverage Tool
</h1>


## 📄 Overview
This is a freely available tool for computing graph coverage in directed graphs used in path-based software testing.

## ⚙ Usage
The tool is available as a GitHub Page [here](https://zerofyy.github.io/Graph-Coverage/) with instructions on the site.

Alternatively, the algorithms can be found in [this script](graph_coverage.py) which can be used like so:
```python
from graph_coverage import parse_graph, compute_prime_paths, compute_edge_pairs, format_output


# Read input from file
with open('graph_input.txt', 'r') as file:
    graph = parse_graph(file.read())

# Read input from terminal
graph = parse_graph(input())

# Compute prime paths
paths = compute_prime_paths(graph)

# Compute edge pairs
pairs = compute_edge_pairs(graph)

# Print paths or pairs formatted into a Num,Len,Path table.
print(format_output(paths))
print(format_output(pairs))

# Print raw paths or pairs, as lists of nodes.
for path in paths:
    print(path)
    
for pair in pairs:
    print(pair)
```

## TODO
- Implement tests generation.
