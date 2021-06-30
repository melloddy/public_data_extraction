from typing import List
from itertools import combinations
from pathos.multiprocessing import Pool
from pandas import DataFrame
from numpy import zeros, where
from scipy.stats import ks_2samp
from sklearn.cluster import DBSCAN


def cluster_assays(df: DataFrame) -> List:
    assays = df.assay_id.unique()
    nb_assays = len(assays)
    distances = zeros((nb_assays, nb_assays))

    # for i, j in combinations(range(nb_assays), 2):
    #     assay_i = assays[i]
    #     values_i = df[df['assay_id'] == assay_i]['pchembl_value']
    #     assay_j = assays[j]
    #     values_j = df[df['assay_id'] == assay_j]['pchembl_value']
    #     distances[i, j] = ks_2samp(values_i, values_j)[0]

    assay_data = [
        {
            'index': i,
            'id': assay_id,
            'values': df[df['assay_id'] == assay_id]['pchembl_value']
        }
        for i, assay_id in enumerate(assays)
    ]

    with Pool() as pool:
        distances_ = pool.starmap(
            lambda x, y: (x['index'], y['index'], ks_2samp(x['values'], y['values'])[0]),
            combinations(assay_data, 2),
        )
    for i, j, d in distances_:
        distances[i, j] = d

    clusters = DBSCAN(eps=.5, min_samples=1, n_jobs=-1).fit(distances)
    assay_groups = list()
    for k in range(max(clusters.labels_)):
        indexes = where(clusters.labels_ == k)[0]
        assay_groups.append(assays[indexes])
    return assay_groups


def merge_assays(df: DataFrame, assay_groups: List) -> DataFrame:
    df_ = df.copy()
    for batch in assay_groups:
        df_['assay_id'][df_['assay_id'].isin(batch)] = batch.min()
    return df_


# def merge_assays_(
#     assay_batches: List[Tuple],
#     df: DataFrame,
#     column_name: str = 'assay_id',
# ) -> DataFrame:
#     df_ = df.copy()
#     df_[column_name+'_merged'] = df_[column_name]
#     for batch in assay_batches:
#         batch_label = '-'.join(map(str, batch))
#         df_[column_name+'_merged'][df_[column_name].isin(batch)] = batch_label
#     return df_
