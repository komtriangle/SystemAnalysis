from pathlib import Path
from itertools import permutations


def parse_edge(line: str):
    nodes = line.split(",")
    if len(nodes) != 2:
        raise Exception("Error while parsing edge")
    return nodes


def csv_reader(csv_bytes: str):
    data = csv_bytes.decode('utf-8').splitlines()
    return [parse_edge(line) for line in data]


def permutations_nodes(nodes: []):
    return [[a, b] for a, b in permutations(nodes, 2)]


def permutations_subordinations(control_node: int, nodes:[]):
    return [[node, control_node] for node in nodes]


def permutations_management(control_node: int, nodes:[]):
    return [[control_node, node] for node in nodes]


def all_subordinations(subordination: [],  nodes: [], submission_dict: {}):
    for node in nodes:
        if node not in subordination:
            subordination.append(node)
            if node in submission_dict:
                all_subordinations(subordination, submission_dict[node], submission_dict)


def indirect_subordination(subordination: [], nodes: [], submission_dict: {}):
    for node in nodes:
        if node in submission_dict:
            all_subordinations(subordination, submission_dict[node], submission_dict)


def format_couples(couples: []):
    return ", ".join(["({0}, {1})".format(couple[0], couple[1]) for couple in couples])


def print_results(relationships: []):
    for i in range(len(relationships)):
        print("r{0} {1}".format(i+1, format_couples(relationships[i])))


def process_edges(edges: []):
    #0 - прямое усправление
    #1 - прямое подчинение
    #2 - опосредственное управление
    #3 - опосредственное подчинение
    #4 - соподчиненность
    relationships = [[] for i in range(5)]
    submission_dict = {}
    for edge in edges:
        relationships[0].append(edge)
        relationships[1].append([edge[1], edge[0]])
        if edge[0] in submission_dict:
            submission_dict[edge[0]].append(edge[1])
        else:
            submission_dict[edge[0]] = [edge[1]]
    for key in submission_dict:
        nodes = submission_dict[key]
        if len(nodes) > 1:
            relationships[4].extend(permutations_nodes(nodes))
        subordination = []
        indirect_subordination(subordination, submission_dict[key], submission_dict)
        relationships[2].extend(permutations_management(key, subordination))
        relationships[3].extend(permutations_subordinations(key, subordination))

    print_results(relationships)


def serialize_csv(path_to_file: str):
    csv_file = Path(path_to_file)
    if not csv_file.is_file():
        raise Exception("File {0} doesn't exist".format(path_to_file))
    stream = open(path_to_file, "rb")
    return stream.read()


def task(serialized_file: str):
    edges = csv_reader(serialized_file)
    process_edges(edges)


def main():
    try:
        path_to_csv = "./csv_samples/1.csv"
        serialized_file = serialize_csv(path_to_csv)
        task(serialized_file)
    except Exception as e:
        print(e)


main()
