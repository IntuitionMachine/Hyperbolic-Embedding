"""
Plots for product embeddings
"""

import utils
from sklearn.manifold import TSNE
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from numpy import linspace


def tsne_plot(X, y):
    """
    use a 2d tsne embedding of X to produce a plot with labels y
    :param X: feature matrix np.array of shape (n_examples, n_features)
    :param y: label vector np.array of shape (n_examples)
    :return:
    """
    model = TSNE(n_components=2, random_state=0)
    print 'fitting tsne model'
    tsne = model.fit_transform(X)
    # sb.set_context("notebook", font_scale=1.1)
    sns.set_style("ticks")
    df = pd.DataFrame(data=tsne, index=None, columns=['x', 'y'])
    df['label'] = y
    sns.lmplot('x', 'y',
               data=df,
               fit_reg=False,
               hue="label",
               scatter_kws={"marker": "D",
                            "s": 20})
    plt.show()


def plot_error_bars(ax, data, sde):
    xvals = np.arange(0, 9, 1)
    for idx in range(data.shape[1]):
        if idx == 0:
            col = 'b'
        else:
            col = 'r'
        ax.fill_between(xvals.T, data[:, idx] - sde[:, idx], data[:, idx] + sde[:, idx], interpolate=True, alpha=0.1,
                        color=col)
    return ax


def plot_lines_from_df(name, meanpath, errpath, outpath):
    styles = ['bo-', 'ro--', 'ro-.', 'ro:', 'rs-', 'rs--', 'rs-.', 'rs:']
    if name == 'football':
        legend = True
    else:
        legend = False
    # errors_t = errors.transpose()
    # means_t = means.transpose()
    # errpath = '../../results/all/{}_errors.csv'.format(name)
    # meanpath = '../../results/all/{}_means.csv'.format(name)
    errors_t = pd.read_csv(errpath, index_col=0).transpose()
    means_t = pd.read_csv(meanpath, index_col=0).transpose()
    ax = means_t.plot(style=styles, legend=legend, kind='line')
    # ax = means.transpose().plot(yerr=errors.transpose(), kind='line', legend=False)
    # ax.legend(bbox_to_anchor=(1.3, 1.05))
    ax = plot_error_bars(ax, means_t.values, errors_t.values)
    ax.set_xlabel("fraction of labeled data")
    ax.set_ylabel("macro F1")
    plt.savefig(outpath)


def plot_rfcev(rfecv, outpath):
    """
    Plot the rfcev grid scores produced by a greedy optimisation of the number of features in a random forest
    :param rfecv: The ouput of the scikit-learn RFECV function
    :param outpath: path to write the figure to
    :return:
    """
    # Plot number of features VS. cross-validation scores
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.savefig(outpath, bbox_inches='tight')


def plot_embedding(embedding, labels, path):
    colours = labels

    plt.scatter(embedding[:, 0], embedding[:, 1], c=colours, alpha=0.4)
    vert_labs = xrange(1, len(labels) + 1)
    for vert_lab, x, y in zip(vert_labs, embedding[:, 0], embedding[:, 1]):
        plt.annotate(
            vert_lab,
            xy=(x, y), xytext=(-2, 2),
            textcoords='offset points', ha='right', va='bottom', fontsize=8)
    plt.savefig(path)
    plt.clf()


def plot_poincare_embedding(embedding, labels, outpath, annotate=True):
    """
    plots the hyperbolic embedding on the Poincare disc
    :param embedding: A numpy array of size (ndata, 2) with columns (r, theta)
    :param labels: A numpy array of size (ndata, 1)
    :param outpath: The path to save the figure
    :return:
    """
    # labels = np.array(labels)
    try:
        if labels.shape[1] > 1:
            labels = get_first_label(labels)
    except IndexError:
        pass

    if len(np.unique(labels)) < 3:
        colours = labels
    else:
        # these values use the entire colour map, adjusting them selects just a subsection of the map.
        start = 0.0
        stop = 1.0
        cm_subsection = linspace(start, stop, max(labels) + 1)
        # use the jet colour map
        colour_selection = np.array([cm.jet(idx) for idx in cm_subsection])
        colours = colour_selection[labels, :]

    x = embedding[:, 0]
    y = embedding[:, 1]

    # for plotting circle line:
    a = np.linspace(0, 2 * np.pi, 500)
    cx, cy = np.cos(a), np.sin(a)

    fg, ax = plt.subplots(1, 1)
    ax.plot(cx, cy, '-', alpha=.5)  # draw unit circle line
    ax.scatter(x, y, c=colours, alpha=0.5, s=200)  # plot random points
    if annotate:
        vert_labs = xrange(1, len(labels) + 1)
        for vert_lab, x, y in zip(vert_labs, x, y):
            plt.annotate(
                vert_lab,
                xy=(x, y), xytext=(-2, 2),
                textcoords='offset points', ha='right', va='bottom', fontsize=20)
    ax.axis('equal')
    ax.grid(True)
    # fg.canvas.draw()
    plt.savefig(outpath)
    plt.clf()


def plot_deepwalk_embedding(embedding, labels, path, annotate=True):
    """
    plots the hyperbolic embedding on the Poincare disc
    :param embedding: A numpy array of size (ndata, 2) with columns (r, theta)
    :param labels: A numpy array of size (ndata, 1)
    :param path: The path to save the figure
    :return:
    """
    # labels = np.array(labels)
    try:
        if labels.shape[1] > 1:
            labels = get_first_label(labels)
    except IndexError:
        pass

    if len(np.unique(labels)) < 3:
        colours = labels
    else:
        # these values use the entire colour map, adjusting them selects just a subsection of the map.
        start = 0.0
        stop = 1.0
        cm_subsection = linspace(start, stop, max(labels) + 1)
        # use the jet colour map
        colour_selection = np.array([cm.jet(idx) for idx in cm_subsection])
        colours = colour_selection[labels, :]

    x = embedding[:, 0]
    y = embedding[:, 1]

    fg, ax = plt.subplots(1, 1)
    ax.scatter(x, y, c=colours, alpha=0.5, s=200)  # plot points
    if annotate:
        vert_labs = xrange(1, len(labels) + 1)
        for vert_lab, x, y in zip(vert_labs, x, y):
            plt.annotate(
                vert_lab,
                xy=(x, y), xytext=(-3, 3),
                textcoords='offset points', ha='right', va='bottom', fontsize=20)
    ax.axis('equal')
    ax.grid(True)
    # fg.canvas.draw()
    plt.savefig(path)
    plt.clf()


def get_first_label(labels):
    """
    A hack to colour multilabel data by choosing the first label. Might be better to choose the rarest label
    :param labels: A scipy sparse matrix of labels
    :return:
    """
    return np.array(np.argmax(labels, axis=1)).flatten()


def MF_embedding_TSNE():
    """

    :return:
    """
    path = '../../local_resources/0_001sample.csv'
    data = pd.read_csv(path)
    emd = pd.read_csv('../../local_resources/roberto_emd.csv', header=None, index_col=0)
    cust_data = data[['customerId', 'target_churned']].groupby('customerId', squeeze=True).first()
    del cust_data.index.name
    all_data = emd.join(cust_data)
    X = all_data.values[:, :-1]
    y = all_data.values[:, -1]
    tsne_plot(X, y)


if __name__ == '__main__':
    emd_path = '../../local_resources/karate/karate2.emd'
    x_path = '../../local_resources/karate/X.p'
    y_path = '../../local_resources/karate/y.p'
    X, y = utils.read_data(x_path, y_path)
    emd = pd.read_csv(emd_path, header=None, index_col=0, skiprows=1, sep=" ")
    emdv = emd.values
    outpath = '../../results/karate/karate2.pdf'
    plot_poincare_embedding(emdv, y, outpath, annotate=True)
