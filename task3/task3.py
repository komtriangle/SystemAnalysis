from pathlib import Path
from itertools import permutations
from io import StringIO
import csv

def parse_edge(line: str):
    if len(line) != 2:
        raise Exception("Error while parsing edge")
    return [int(node) for node in line]


def csv_reader(csvString: str):
    f = StringIO(csvString)
    reader = csv.reader(f, delimiter=',')
    return [parse_edge(line) for line in reader]


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
    '''
    0 - прямое усправление
    1 - прямое подчинение
    2 - опосредственное управление
    3 - опосредственное подчинение
    4 - соподчиненность
    '''
    relationships = [[] for i in range(5)]
    submission_dict = {}
    for edge in edges:
        if edge[0] not in relationships[0]:
            relationships[0].append(edge[0])
        if edge[1] not in relationships[1]:
            relationships[1].append(edge[1])
        if edge[0] in submission_dict:
            submission_dict[edge[0]].append(edge[1])
        else:
            submission_dict[edge[0]] = [edge[1]]
    for key in submission_dict:
        nodes = submission_dict[key]
        if len(nodes) > 1:
            relationships[4].extend(nodes)
        subordination = []
        indirect_subordination(subordination, submission_dict[key], submission_dict)
        if key not in relationships[2] and len(subordination) > 0:
            relationships[2].append(key)

        for node in subordination:
            if node not in relationships[3]:
                relationships[3].append(node)

    [r.sort() for r in relationships]
    return relationships


def serialize_csv(path_to_file: str):
    csv_file = Path(path_to_file)
    if not csv_file.is_file():
        raise Exception("File {0} doesn't exist".format(path_to_file))
    stream = open(path_to_file, "rb")
    return stream.read()


def task(csvString: str):
    edges = csv_reader(csvString)
    return process_edges(edges)

reference = [[1,3],[2,3,4,5],[1],[4,5],[2,3,4,5]]

with open('csv_samples/1.csv') as file:
    csvString = file.read()
    result = task(csvString)
    print(reference)
    print(result)
    print(result == reference)