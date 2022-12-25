import json
import numpy as np


def task(json_string):
    data = json.loads(json_string)
    matrixes = []
    for i in range(len(data)):
        matrixes.append([])
        for j in range(len(data[0])):
            matrixes[i].append([0]*len(data[0]))
    for idx, expert in enumerate(data):
        for i in range(len(expert)):
            for j in range(len(expert)):
                value = 0.5
                if expert[i] > expert[j]:
                    value = 1
                elif expert[i] < expert[j]:
                    value = 0
                matrixes[idx][i][j] = value
    mean_matrix = []
    for i in range(len(data[0])):
        mean_matrix.append([0]*len(data[0]))
        for j in range(len(data[0])):
            temp = 0.0
            temp = sum([matrixes[k][i][j] for k in range(len(matrixes))])
            temp /= len(matrixes)
            mean_matrix[i][j] = temp

    m_matrix = np.array(mean_matrix)
    m_matrix = np.transpose(m_matrix)

    k_0 = [1/len(data) for _ in range(len(data))]
    k = k_0
    one_arr = np.array([1 for _ in range(len(data))])
    e = 0.001

    is_first = True
    while is_first or max(abs(k-k_0)) >= e:
        is_first = False
        k_0 = k
        y = np.dot(m_matrix, k_0)
        l = np.dot(one_arr, y)
        k = np.dot(1/l, y)

    return k
