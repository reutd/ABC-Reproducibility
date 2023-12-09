import scipy
import scib as scIB


# most of the code was dapted from the published pipeline at
# https://github.com/theislab/scib-pipeline/blob/main/scripts/metrics/metrics.py
def evaluate_integration(orig_dataset, integ_dataset, eval_params, batch_key, label_key='celltype',
                         data_type='RNA', organism='mouse', bio_con_w=0.5):
    """Evaluates the integration using the scib package according to the selected metrics in the eval_params dictionary.

    Parameters:
        orig_dataset (anndata): The anndata object holding the original dataset.
        integ_dataset (anndata): The anndata object holding the integrated dataset.
        eval_params (dictionary): A dictionary holding the name of the metric as key and a boolean value to indicate
            if this metric is to be calculated or not.
        batch_key (String): The batch label key in adata.obs.
        label_key (String): The cell type label key in adata.obs. Default: 'celltype'.
        data_type (String): Either 'RNA" for scRNA seq data or 'ATAC' for ATAC seq data.
        organism (String): Either 'mouse' or 'human'. Used for cell cycle evaluation. Default: 'mouse'.
        bio_con_w (float): The weight of the biological variance conservation score should have in the final score.

    Returns:
        metrics: A dataframe holding the metric names as row names and the metric score in the first column.

    """

    precompute_pca = True
    recompute_neighbors = True
    embed = 'X_pca'
    n_hvgs = integ_dataset.n_vars

    # define the groups of metrics types
    bio_con_metrics = ['ARI_cluster/label', 'cell_cycle_conservation', 'cLISI',
                       'hvg_overlap', 'isolated_label_silhouette', 'isolated_label_F1',
                       'NMI_cluster/label', 'ASW_label', 'trajectory']
    batch_corr_metrics = ['graph_conn', 'iLISI', 'ASW_label/batch']

    # make sure the data is not sparse
    if scipy.sparse.issparse(orig_dataset.X):
        print("The given orig_dataset.X matrix is sparse. Converting to dense.")
        orig_dataset.X = orig_dataset.X.todense()

    if scipy.sparse.issparse(integ_dataset.X):
        print("The given integ_dataset.X matrix is sparse. Converting to dense.")
        integ_dataset.X = integ_dataset.X.todense()


    # don't calculate cell cycle score and HVG for ATAC dataset
    if data_type == 'ATAC':
        eval_params['cell_cycle_'] = False
        eval_params['hvg_overlap'] = False
    else:
        eval_params['cell_cycle_'] = True
        eval_params['hvg_overlap'] = True

    # if pseudotime information does not exist, do not compute trajectory score
    if 'dpt_pseudotime' not in orig_dataset.obs or 'dpt_pseudotime' not in integ_dataset.obs:
        eval_params['trajectory_'] = False
    else:
        eval_params['trajectory_'] = True


    # preprocess data (PCA, neighbors graph and HVG)
    scIB.preprocessing.reduce_data(integ_dataset, n_top_genes=n_hvgs, neighbors=recompute_neighbors, use_rep=embed,
                                   batch_key=batch_key, pca=precompute_pca, umap=False)

    metrics = scIB.me.metrics(orig_dataset, integ_dataset, verbose=True, batch_key=batch_key, label_key=label_key,
                              hvg_score_=eval_params['hvg_score_'],
                              nmi_=eval_params['nmi_'],
                              ari_=eval_params['ari_'],
                              nmi_method='arithmetic',
                              silhouette_=eval_params['silhouette_'],
                              pcr_=False,
                              cell_cycle_=eval_params['cell_cycle_'],
                              organism=organism,
                              isolated_labels_=eval_params['isolated_labels_'],
                              graph_conn_=eval_params['graph_conn_'],
                              kBET_=False,
                              lisi_graph_=eval_params['lisi_graph_'],
                              trajectory_=eval_params['trajectory_'],
                              type_='full',
                              )

    # calculate averages
    bio_con_rows = metrics.loc[bio_con_metrics]
    bio_con_score = bio_con_rows[0].mean()
    batch_corr_rows = metrics.loc[batch_corr_metrics]
    batch_corr_score = batch_corr_rows[0].mean()

    # add to dataframe
    metrics.loc['Bio_Conservation_avg'] = bio_con_score
    metrics.loc['Batch_Correction_avg'] = batch_corr_score
    metrics.loc['Final_Score'] = (1-bio_con_w) * batch_corr_score + bio_con_w * bio_con_score


    return metrics