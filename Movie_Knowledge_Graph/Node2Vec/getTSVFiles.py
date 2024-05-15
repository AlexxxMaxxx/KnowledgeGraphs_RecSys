from gensim.models import KeyedVectors
import additionalFunctions as af
import pandas as pd
import io

def getTSV(embeddings, start, end, nameCase, vertex_df):
    embTsv = folder_tsv + '/embeddings_' + nameCase + strCombination + '.tsv'
    metaTsv = folder_tsv + '/metadata_' + nameCase + strCombination + '.tsv'

    out_emb = io.open(embTsv, "w", encoding="utf-8")
    out_meta = io.open(metaTsv, "w", encoding="utf-8")    # до сюда все хорошо

    for i in range(start, end):
        vector = embeddings[str(i)]
        out_emb.write("\t".join([str(x) for x in vector]) + "\n")

        title = vertex_df.loc[vertex_df['id'] == i, 'label'].values[0]
        if i <= SIZE_DF and (nameCase == 'movies_' or nameCase == 'vertex_'):
            title = title.split('_')[0]
        out_meta.write(title + "\n")

    out_emb.close()
    out_meta.close()


# тут менять
strCombination = '64_50_30_2'
df = 'df1'
comb = 'comb1'

fileName_merged_dataset = '../../Datasets/merged/' + comb + '/' + df + '_dataset.csv'


# по умолчанию
merged_df = pd.read_csv(fileName_merged_dataset)
SIZE_DF = len(merged_df)

filePath_vertex = '../../Datasets/visualization_vertex_edge/vertex/vertex_' + df + '_' + comb + '.csv'
vertex_df = pd.read_csv(filePath_vertex)

folder_tsv = '../../Datasets/emb_data/' + comb + '_' + df + '/tsv'
af.folderExists(folder_tsv)

#folder_cmbn = folder_tsv + '/cmbn_' + strCombination
folder_emb = '../../Datasets/emb_data/' + comb + '_' + df + '/emb'
embPath = folder_emb + '/emb_' + strCombination
embeddings = KeyedVectors.load_word2vec_format(embPath)

#af.folderExists(folder_cmbn)

getTSV(embeddings, 1, SIZE_DF + 1, 'movies_', vertex_df)    # только фильмы
getTSV(embeddings, SIZE_DF + 1, len(embeddings) + 1, 'atributes_', vertex_df)    # только атрибуты
getTSV(embeddings, 1, len(embeddings) + 1, 'vertex_', vertex_df)    # все вершины

print('success')