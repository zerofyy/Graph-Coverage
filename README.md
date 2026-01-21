<h1 align="center">
  Zerofy's Prime Path Coverage Tool
</h1>


## 📄 Overview
This is a freely available tool for computing prime path coverage in directed graphs used in path-based software testing.

## ⚙ Usage
The tool is available as a GitHub Page [here](https://zerofyy.github.io/Prime-Path-Coverage/) with instructions on the site.

Alternatively, the algorithm can be found in [this script](prime_path_coverage.py) which can be used like so:
```python
# ...code from the script...

# Read input from file
with open('graph_input.txt', 'r') as file:
    graph = parse_graph(file.read())
    
# Read input from console
graph = parse_graph(input())

# Compute prime paths
result = compute_prime_paths(graph)
paths = result['paths']

# Print paths formatted into a Num,Len,Path table.
print(format_output(paths))

# Print raw paths, as lists of nodes.
for path in paths:
    print(path)
```

## TODO
- Look into implementing an algorithm to generate test cases from prime paths.