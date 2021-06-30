from typing import List
from pandas import Series, DataFrame, cut, concat
from numpy import log10, power


def categorize_assay(assay_type: str) -> str:
    if assay_type in ['A', 'P']:
        return 'ADME'
    if assay_type == 'T':
        return 'PANEL'
    return 'OTHER'


def nanmol_to_log(value: float) -> float:
    return -log10(value * (10**-9))


def log_to_nanomol(value: float) -> float:
    return power(10, 9 - value)


def bin_assay_values(
    values: Series,
    ascending: bool = False,
    from_median: bool = False,
    min_bin_size: int = 25,
    max_splits: int = 5,
) -> (List[float], List[DataFrame]):
    thresholds = list()
    binned_dataframes = list()

    if from_median:
        median = values.median()
        max_splits_ = max_splits - 1
        potential_thresholds_ = [median]
        max_splits_upper = max_splits_ // 2 + max_splits_ % 2
        max_splits_lower = max_splits_ - max_splits_upper
        potential_thresholds_.extend([median + i for i in range(1, 1 + max_splits_upper)])
        potential_thresholds_.extend([median - i for i in range(1, 1 + max_splits_lower)])
    else:
        if ascending:
            start = values.min()
            step = 1
        else:
            start = values.max()
            step = -1
        potential_thresholds_ = [start + i * step for i in range(1, 1 + max_splits)]

    potential_thresholds = filter(
        lambda x:  x < values.max() and x > values.min(),
        potential_thresholds_
    )
    for threshold in potential_thresholds:
        bins = cut(
            values,
            bins=[values.min(), threshold, values.max()],
            labels=[0, 1],
            include_lowest=True,
        )
        nb_ones = bins.astype(int).sum()
        if nb_ones >= min_bin_size and len(values) - nb_ones >= min_bin_size:
            thresholds.append(threshold)
            binned_dataframes.append(
                DataFrame({'values': values, f'bins': bins})
            )
    return thresholds, binned_dataframes


def regression_extract(df: DataFrame) -> (List, List):
    # Getting the mapping assay_id => regression_task_id
    task_ids = {assay: i for i, assay in enumerate(df.assay_id.unique())}
    temp_df = df.rename(columns={'chembl_id': 'input_compound_id'})
    temp_df['regression_task_id'] = temp_df['assay_id'].map(task_ids)

    # Extracting T4
    t4_df = temp_df[[
        'input_compound_id',
        'regression_task_id',
        'standard_value',
        'standard_relation',
        'standard_units',
        'standard_type',
    ]]

    # Extracting T3
    t3_df = temp_df[['assay_id', 'regression_task_id', 'assay_type', 'target_id']]\
        .rename(columns={'assay_id': 'input_assay_id'})\
        .drop_duplicates(subset=['regression_task_id'])\
        .reset_index(drop=True)
    t3_df['assay_type'] = t3_df['assay_type'].apply(categorize_assay)

    return t3_df, t4_df


def bin_assays(df: DataFrame) -> (List, List, List):
    assays = df.assay_id.unique()
    t3_data = list()
    t4_data = list()
    assay_ids_to_drop = list()
    task_counter = 0
    for assay in assays:
        df_ = df[df['assay_id'] == assay]
        category = categorize_assay(df_.iloc[0].assay_type)
        target_id = df_.iloc[0].target_id
        df_ = df_[['chembl_id', 'standard_value']].set_index('chembl_id')
        df_['log_values'] = df_.standard_value.apply(nanmol_to_log)
        thresholds, binned_dfs = bin_assay_values(df_.log_values, from_median=True)
        nb_splits = len(thresholds)
        if nb_splits > 0:
            weight = 1 / nb_splits
            for threshold, binned_df in zip(thresholds, binned_dfs):
                task_counter += 1
                t4_data.append({
                    'input_compound_id': binned_df.index,
                    'classification_task_id': [task_counter]*binned_df.shape[0],
                    'class_label': binned_df.bins,
                })
                t3_data.append({
                    'classification_task_id': task_counter,
                    'input_assay_id': assay,
                    'assay_type': category,
                    'target_id': target_id,
                    'threshold_column': 'standard_value',
                    'threshold_value': log_to_nanomol(threshold),
                    'threshold_operator': '>=',
                    'weight': weight,
                })
        else:
            assay_ids_to_drop.append(assay)
    return t3_data, t4_data, assay_ids_to_drop


def delete_assays(
    ids_to_delete: List[int],
    df: DataFrame,
    column_name: str = 'assay_id',
) -> DataFrame:
    df_to_drop = df[df[column_name].isin(ids_to_delete)]
    return df.drop(df_to_drop.index)


def build_t2(df: DataFrame) -> DataFrame:
    t2_df = df[['chembl_id', 'canonical_smiles']].rename(
        columns={
            'chembl_id': 'input_compound_id',
            'canonical_smiles': 'smiles',
        }
    )
    t2_df.drop_duplicates(inplace=True)
    return t2_df


def build_t3(t3_data: List) -> DataFrame:
    t3_df = DataFrame(t3_data)
    return t3_df


def build_t4(t4_data: List) -> DataFrame:
    t4_df = concat([DataFrame(d) for d in t4_data])
    return t4_df
