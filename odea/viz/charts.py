import matplotlib.pyplot as plt
import numpy as np


def bar_chart(result, save=False, file_format='pdf'):
    plt.figure(figsize=(10, 6))

    width = 0.30
    scenario = range(1, len(result) + 1)
    cr = [res[0] for res in result]
    tcr = [res[1] for res in result]
    x = np.arange(1, len(scenario)+1)

    # plot data in grouped bars
    plt.bar(x-0.2, cr, width, color='orange', label='ECR')
    plt.bar(x+0.2, tcr, width, label='TCR')

    plt.title('Complexity Reduction')
    plt.xlabel('Scenario')
    plt.ylabel('ECR/TCR')

    plt.legend()
    plt.xticks(range(1, len(scenario), 5))
    plt.grid('on', axis='y', linestyle='--', linewidth=1)

    if save:
        dist = max([res[3] for res in result])
        supp = max([res[4] for res in result])
        file_name = 'scenario_bar_1_{:d}_{:d}_serif.{:s}'.format(
            dist, supp, file_format)
        plt.savefig(file_name, format=file_format, bbox_inches='tight')

    plt.show()


def scatter_chart(result, save=False, file_format='pdf'):
    marker = ['o', 'v', 'x']
    colors = ['#1f77b4', 'red', 'green']

    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6)

    for res in result:
        # select marker based on distance
        if res[3] <= 1:
            ma = 0
        elif res[3] <= 2:
            ma = 1
        else:
            ma = 2

        # select color based on support
        if res[4] <= 8:
            c = 0
        elif res[4] <= 16:
            c = 1
        else:
            c = 2

        ax.scatter(res[1], res[2], s=100, marker=marker[ma],
                   color=colors[c], alpha=0.5)

    plt.title('Total Complexity Reduction/# of High-level Concepts')
    plt.xlabel('TCR')
    plt.ylabel('# of High-level Concepts')
    ax.set_yticks(range(0, 22, 2))
    plt.grid('on', axis='y', linestyle='--', linewidth=1)

    # ============
    # custom artists for legend
    triangleArtist = plt.Line2D(
        (0, 0), (0, 0), color='gray', marker='o', linestyle='')
    dotArtist = plt.Line2D((0, 0), (0, 0), color='gray',
                           marker='v', linestyle='')
    crossArtist = plt.Line2D(
        (0, 0), (0, 0), color='gray', marker='x', linestyle='')

    # Create legend from custom artist/label lists
    ax.legend([triangleArtist, dotArtist, crossArtist],
              ['dist ≤ 1', 'dist ≤ 2', 'dist ≤ 3'])

    # ============
    if save:
        file_name = 'scenario_1_tcr_over_ca_dist_and_supp_serif' + file_format
        plt.savefig(file_name, format=file_format, bbox_inches='tight')

    plt.show()
