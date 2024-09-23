import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np


def pout(a, limit=5):
    if len(a) > limit:
        print(f'Rodoma {limit} eilutės iš {len(a)}')
    for k,i in enumerate(a):
        if k > limit-1:
            break
        l = []
        for n in i:
            f = f'{str(n):^14.14}'
            l.append(f)
        t = f'|{k:^3}|'+'|'.join(l)+'|'
        print(t)
        
        
# PieOfPie
def pieOfPie(pie, pie_s, labels=None, labels_s=None, **kwargs):
    '''
    pie: array or list of numbers
    labels: labels for main pie
    pie_s: second pie
    labels_s: labels for second pie
    kwargs : additional parameters for pies
    return : matplotlib figure (whole)
    '''
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
    fig.subplots_adjust(wspace=0)

    # pie chart parameters
    ratios = pie
    labels = labels
    explode = kwargs.get('explode', None)
    # rotate so that first wedge is split by the x-axis
    o_r = list(map(lambda x: x/sum(ratios), ratios))
    angle = -180 * o_r[0]
    if o_r[0] > 0.5:
        angle = kwargs.get('angle',-90)
    print(f'{angle=}, {o_r[0]=}')
    wedges, *_ = ax1.pie(ratios, autopct='%1.1f%%', startangle=angle,
                        labels=labels, explode=explode)

    # pie chart parameters
    pies_ratios = pie_s
    pies_labels = labels_s
    width=0.2
    ax2.pie(pies_ratios, labels=pies_labels, autopct='%1.1f%%', radius=0.5)
    
    # lines
    # use ConnectionPatch to draw lines between the two plots
    # get the wedge data
    theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
    center, r = ax1.patches[0].center, ax1.patches[0].r

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, .5), xyB=(x, y),
                        coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    con.set_linewidth(2)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(- width / 2, -.5), xyB=(x, y), coordsA="data",
                        coordsB="data", axesA=ax2, axesB=ax1)
    con.set_color([0, 0, 0])
    ax2.add_artist(con)
    con.set_linewidth(2)
    return fig
    pass