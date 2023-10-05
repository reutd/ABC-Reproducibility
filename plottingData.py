import os
# import numpy as np
# import pandas as pd
# import anndata
import scanpy as sc
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy import stats
# import sklearn as sk
import matplotlib
# import random


def plot_datasets(data, categories, save_path, dpi, baseName, use_emb=False):

    # set plot params
    matplotlib.rc('ytick', labelsize=14)
    matplotlib.rc('xtick', labelsize=14)
    sc.set_figure_params(dpi_save=dpi)
    os.makedirs(save_path, exist_ok=True)
    sc.settings.figdir = save_path

    # build necessary data structures
    if use_emb:
      sc.pp.neighbors(data, n_neighbors=25, use_rep = 'X_emb')

    else:
      sc.pp.pca(data, svd_solver="arpack")
      sc.pp.neighbors(data, n_neighbors=25)

    sc.tl.umap(data, random_state=42)

    # create plots per category
    for category in categories:
        sc.pl.umap(data, palette=matplotlib.rcParams["axes.prop_cycle"], color=[category],
                   save=f"_{baseName}_datasetBy{category}.png", frameon=False, show=False, use_raw=False)
