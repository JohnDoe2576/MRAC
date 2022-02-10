import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

class Plot_Data():

    def __init__(self, **kwargs):
        # title: 
        # label: multiple labels in list
        self.__dict__.update(kwargs)

    def plot_twin(self, t, u, y):
        clr = self.colors()
        mpl.rc('font',family="Garamond")
        plt.figure(figsize=np.array([24, 10])/2.54,dpi=150)
        plt.plot(t,u, '-', color=clr['dodger_blue'], linewidth=0.6, label=self.legend[0])
        plt.plot(t,y, '-', color=clr['crimson'], linewidth=0.6, label=self.legend[1])
        plt.xlim(np.min(t), np.max(t))
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        self.fig_defaults(plt)
        plt.show()

    def fig_defaults(self, fh):
        clr = self.colors()
        fh.xticks(fontname="Garamond",fontsize=12)
        fh.yticks(fontname="Garamond",fontsize=12)
        fh.box("on")
        fh.legend(ncol=2,frameon=False)
        ax=fh.gca()
        ax.set_facecolor(clr['my_grey'])
        ax.grid(True,color='w',linewidth=0.5)

    @staticmethod
    def colors():
        clr = {'my_grey': np.array([245, 245, 245])/255,
        'muted_blue': np.array([31, 119, 180])/255,
        'safety_orange': np.array([255, 127, 14])/255,
        'cooked_asparagus_green': np.array([44, 160, 44])/255,
        'brick_red': np.array([214, 39, 40])/255,
        'muted_purple': np.array([148, 103, 189])/255,
        'chestnut_brown': np.array([140, 86, 75])/255,
        'raspberry_yogurt_pink': np.array([227, 119, 194])/255,
        'middle_grey': np.array([127, 127, 127])/255,
        'curry_yellow_green': np.array([188, 189, 34])/255,
        'blue_teal': np.array([23, 190, 207])/255,
        'SeqGnBu3': np.array([ 168, 221, 181 ]) / 255,
        'SeqGreens2': np.array([ 199, 233, 192 ]) / 255,
        'SeqBuGn4': np.array([ 102, 194, 164 ]) / 255,
        'SeqBuGn5': np.array([ 65, 174, 118 ]) / 255,
        'SeqBuGn7': np.array([ 0, 109, 44 ]) / 255,
        'SeqPuBuGn1': np.array([ 236, 226, 240 ]) / 255,
        'SeqPuBuGn3': np.array([ 166, 189, 219 ]) / 255,
        'SeqPuBuGn4': np.array([ 103, 169, 207 ]) / 255,
        'SeqPuBuGn7': np.array([ 1, 108, 89 ]) / 255,
        'SeqRdBu5': np.array([ 247, 247, 247 ]) / 255,
        'SeqRdBu6': np.array([ 209, 229, 240 ]) / 255,
        'CyclicalPhase6': np.array([ 95, 127, 228 ]) / 255,
        'CyclicalTwilight6': np.array([ 142, 44, 80 ]) / 255,
        'light_sky_blue': np.array([ 135, 206, 250 ])/255,
        'medium_purple': np.array([ 147, 112, 219 ])/255,
        'slate_blue': np.array([ 106, 90, 205 ])/255,
        'dodger_blue': np.array([ 30, 144, 255 ])/255,
        'medium_sea_green': np.array([ 60, 179, 113 ])/255,
        'fire_brick': np.array([ 178, 34, 34 ])/255,
        'crimson': np.array([ 220, 20, 60 ])/255,
        'white': np.array([ 255, 255, 255 ])/255
        }

        return clr