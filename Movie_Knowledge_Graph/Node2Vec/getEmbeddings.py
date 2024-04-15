from node2vec import Node2Vec
from itertools import product
import additionalFunctions as af
import networkx as nx
import pandas as pd

def initGraph(filePath_edge):
    G = nx.Graph()
    for index, row in pd.read_csv(filePath_edge).iterrows():
        G.add_edge(row['Source'], row['Target'])
    return G

def getEmbeddings(G, dimensions, walk_length, num_walks, window, temp_folder):
    af.folderExists(temp_folder)
    node2vec = Node2Vec(G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=4, temp_folder=temp_folder)
    return node2vec.fit(window=window)

def checkCombination(modelPath, embPath):
    return af.fileExists(modelPath) and af.fileExists(embPath)

def saveAll(model, modelPath, embPath):
    model.save(modelPath)
    model.wv.save_word2vec_format(embPath)

# Тут вносим изменения ---------
# по рекомендациям
'''dimensions = [64, 128, 256, 512]
walk_length = [40, 80, 120, 160]
num_walks = [25, 50, 75, 100]
window = [5, 10, 15, 30]'''

'''dimensions = [8, 16, 32]
walk_length = [10, 20, 40]
num_walks = [10, 20, 40]
window = [2, 5, 10]'''

dimensions = [64, 128]
walk_length = [40, 80, 120]
num_walks = [25, 50, 75]
window = [5, 10, 15]

fileName_merged_dataset = '../../Datasets/merged/dataset_10694.csv'
# ------------------------------
merged_df = pd.read_csv(fileName_merged_dataset)
SIZE_DF = len(merged_df)

filePath_edge = '../../Datasets/visualization_vertex_edge/edge_' + str(SIZE_DF) + '.csv'


folder_emb = '../../Datasets/emb_data/' + str(SIZE_DF) + '/'
folder_emb_emb = folder_emb + 'emb'
folder_model = folder_emb + 'model'
print(folder_model)

filePath_times = folder_emb + 'execution_time.txt'
filePath_memory = folder_emb + 'mem_usage.txt'
filePath_graph = folder_emb + 'graph.graphml'
temp_folder = folder_emb + 'temp_folder'

print(f'SIZE_DF = {SIZE_DF}\n')      # remove
print(f'DF {fileName_merged_dataset}\n')      # remove
print(merged_df.head(5))     # remove

af.folderExists(folder_emb)

if af.fileExists(filePath_graph):
    G = nx.read_graphml(filePath_graph)
else:
    G = initGraph(filePath_edge)
    nx.write_graphml(G, filePath_graph)


af.folderExists(folder_model)    # для сохранения
af.folderExists(folder_emb_emb)

# Получаем все комбинации параметров
#all_combinations = list(product(dimensions, walk_length, num_walks, window))
#all_combinations = [[8, 55, 35, 8], [16, 55, 35, 8], [32, 55, 35, 8], [64, 55, 35, 8], [128, 55, 35, 8]]
all_combinations = [[8, 55, 35, 8], [16, 55, 35, 8]]

for combination in all_combinations:
    strCombination = '_'.join([str(x) for x in combination])
    print(f'strCombination = {strCombination}')     # remove
    modelPath = folder_model + '/model_' + strCombination
    embPath = folder_emb_emb + '/emb_' + strCombination

    if checkCombination(modelPath, embPath):
        print('next')      # remove
        continue    # след. комбинация

    start_time = af.timer()
    mem_before = af.mem()

    model = getEmbeddings(G, combination[0], combination[1], combination[2], combination[3], temp_folder)
    saveAll(model, modelPath, embPath)

    end_time = af.timer()
    mem_after = af.mem()

    af.writeExecutionTime(filePath_times, af.getExecutionTime(start_time, end_time), strCombination)
    af.writeMemUsage(filePath_memory, af.getMemUsage(mem_before, mem_after), strCombination)

print('Success')