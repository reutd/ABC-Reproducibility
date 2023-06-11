
# All preprocessed datasets were published by Luecken, M.D., Büttner, M., 
# Chaichoompu, K. et al. Benchmarking atlas-level data integration in 
# single-cell genomics. Nat Methods 19, 41–50 (2022). 
# https://doi.org/10.1038/s41592-021-01336-8 
# and are publicly available as Anndata objects on Figshare at:
# https://doi.org/10.6084/m9.figshare.12420968

# datasets definition
datasets = {
    'small_atac_windows':
        {
            'label_key': 'final_cell_label',
            'batch_key': 'batchname',
            'organism': 'mouse',
            'subsample': 1,
            'ATAC': True,
        },

    'small_atac_peaks':
        {
            'label_key': 'final_cell_label',
            'batch_key': 'batchname',
            'organism': 'mouse',
            'subsample': 1,
            'ATAC': True,
        },

    'small_atac_gene_activity':
        {
            'label_key': 'final_cell_label',
            'batch_key': 'batchname',
            'organism': 'mouse',
            'subsample': 1,
            'ATAC': True,
        },

    'human_pancreas_norm_complexBatch':
        {
            'label_key': 'celltype',
            'batch_key': 'tech',
            'organism': 'human',
            'subsample': 1,
            'ATAC': False,            
        },

    'Lung_atlas_public':
        {
            'label_key': 'cell_type',
            'batch_key': 'batch',
            'organism': 'human',
            'subsample': 1,
            'ATAC': False,
        },

    'Immune_ALL_hum_mou':
        {
            'label_key': 'final_annotation',
            'batch_key': 'batch',
            'organism': 'human',
            'subsample': 1,
            'ATAC': False,
        },
}
