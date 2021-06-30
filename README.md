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

Further datasets can be found on the Zenodo Community page:
https://zenodo.org/communities/melloddy/