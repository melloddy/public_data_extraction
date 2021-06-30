## Binning notes
+ when applying the binning procedure, if no threshold leads to a balanced classification dataset, the assay is dropped.

## P Assays (manual fusion)
The original assay IDs for physicochemical assays are overwritten by the grouping procedure.
+ solubility
    - 118 "assays" (grouped by pH and solvant)
    - 52 classification tasks from 18 assays
+ logD
    - 44 "assays" (grouped by pH)
    - 20 classification tasks from 9 assays
+ logP:
    - 1 "assay" (all grouped together)
    - 5 classification tasks from 1 assay

## B & F Assays (statistics-based fusion)
+ 2979 assays
+ 3919 classification tasks from 2876 assays

## A & T Assays (no fusion)
+ 120 assays
+ 87 classification tasks from 74 assays

## Globally
+ 2978 assays remaining
+ 4083 classification tasks
+ 508635 distinct SMILES
+ 4345069 activities

## Classification task counts per assay
+ 1 task: 2268
+ 2 tasks: 391
+ 3 tasks: 256
+ 4 tasks: 50
+ 5 tasks: 13
