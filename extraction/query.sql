\c chembl_25;

CREATE EXTENSION rdkit;
/* -------------------------------------------------------------------------- */
CREATE TABLE assay_filter AS
    SELECT
        activities.assay_id AS assay_id,
        assays.assay_type AS assay_type,
        COUNT(activities.assay_id) AS assay_count

    FROM activities

    LEFT JOIN compound_structures
    ON activities.molregno = compound_structures.molregno

    LEFT JOIN assays
    ON activities.assay_id = assays.assay_id

    WHERE COALESCE(mol_numheavyatoms(mol_from_smiles(canonical_smiles :: cstring)), -1) <= 100
    AND (
        (assay_type = 'A' AND confidence_score >= 0)
        OR
        (assay_type IN ('B', 'F') AND confidence_score >= 8 AND pchembl_value IS NOT NULL)
        OR
        (assay_type = 'P' AND confidence_score >= 0)
        OR
        (assay_type = 'T' AND confidence_score >= 0)
    )
    GROUP BY activities.assay_id, assays.assay_type
    HAVING (
        (COUNT(activities.assay_id) >= 50 AND assay_type IN ('B', 'F', 'T'))
        OR
        (COUNT(activities.assay_id) > 0 AND assay_type IN ('P', 'A'))
    )
;
/* -------------------------------------------------------------------------- */
CREATE TABLE melloddy AS

SELECT
    activities.assay_id AS assay_id,

    assays.tid AS target_id,
    target_dictionary.pref_name AS target_pref_name,

    assays.confidence_score AS assay_confidence_score,
    assays.assay_type AS assay_type,
    assays.description AS assay_description,
    assays.assay_tax_id AS assay_tax_id,
    assays.assay_strain AS assay_strain,
    assays.assay_tissue AS assay_tissue,
    assays.assay_cell_type AS assay_cell_type,
    assays.assay_subcellular_fraction AS assay_subcellular_fraction,

    assay_filter.assay_count AS assay_count,

    drug_mechanism.action_type AS action_type,

    compound_structures.canonical_smiles AS canonical_smiles,
    activities.molregno AS chembl_id,
    COALESCE(
        mol_numheavyatoms(mol_from_smiles(compound_structures.canonical_smiles :: cstring)),
        -1
    ) AS num_heavy_atoms,

    activities.pchembl_value AS pchembl_value,
    activities.standard_value AS standard_value,
    activities.standard_units AS standard_units,
    activities.standard_type AS standard_type,
    activities.standard_relation AS standard_relation,
    activities.type AS activity_type,
    LOWER(activities.activity_comment) AS activity_comment

FROM activities

LEFT JOIN assay_filter
ON activities.assay_id = assay_filter.assay_id

LEFT JOIN compound_structures
ON activities.molregno = compound_structures.molregno

LEFT JOIN assays
ON activities.assay_id = assays.assay_id

LEFT JOIN target_dictionary
ON assays.tid = target_dictionary.tid

LEFT JOIN drug_mechanism
ON activities.molregno = drug_mechanism.molregno
AND assays.tid = drug_mechanism.tid

WHERE assay_filter.assay_id IS NOT NULL
AND compound_structures.molregno IS NOT NULL
AND target_dictionary.tid IS NOT NULL
AND activities.standard_value IS NOT NULL

;
