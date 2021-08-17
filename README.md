# MELLODDY - Public Data Preparation
Work files for the preparation of public data used to test the federative learning pipelines.


## 1. Extraction
The starter CSV is extracted from the ChEMBL25 database by running a SQL query. The relevant files can be found in the `extraction` directory.

## 2. Processing and Formatting
The notebooks and helper `python` modules in the `processing` directory perform:
+ assay filtering to satisfy the selection criteria,
+ assay fusion (statistical for binding and functional assays, type-based for physicochemical assays),
+ binning of continues values into categories,
+ computation of descriptive statistics for the resulting dataset,
+ formatting of the final dataset into `T2`, `T3`, and `T4` files,
+ building a reference for assay IDs in case the original (pre-fusion) IDs are needed.

## 3. Data Files
Raw data extracts and processed files can be found here:
https://zenodo.org/record/5045055

The archive includes:
+ the `T2`, `T3`, and `T4` files required for the federative learning pipeline,
+ the initial dataset `chembl_extract.csv` extracted from the ChEMBL25 database,
+ the assay ID reference `assay_reference.csv`,
+ summary statistics on the final dataset in the `README` file.

## 4. Related packages
The extracted an processed output files can be used to to prepare  files with MELLODDY-TUNER (https://github.com/melloddy/MELLODDY-TUNER) as inputs for SparseChem (https://github.com/melloddy/SparseChem).

## 5. Related datasets 
All datasets can be found on MELLODDY Zenodo Community:

https://zenodo.org/communities/melloddy/?page=1&size=20

### Datasets extracted and processed from ChEMBL
ChEMBL v25 output files extracted and processed with the public data preparation code 
https://zenodo.org/record/5045055#.YRqAVpMzZTZ
## Datasets for MELLODDY-TUNER

#### Release v1.0

Public data from ChEMBL (version 25) for running MELLODDY-TUNER release v1.0:

https://doi.org/10.5281/zenodo.4778423

#### Release v2.0

Public data from ChEMBL (version 25) and PubChem for running MELLODDY-TUNER release v2.0:

https://doi.org/10.5281/zenodo.4835669
