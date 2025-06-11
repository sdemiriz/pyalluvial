from matplotlib.patches import Rectangle, PathPatch
import matplotlib.pyplot as plt
import matplotlib.path as p
import pandas as pd

df = pd.read_csv("first.csv")


class Alluvial:

    def __init__(self, df, left, right):
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

        plt.axis("off")

        self.data = df[[left, right]]
        sizes = self.size(right)

        self.ax.set_xlim(0, 2.2)
        self.ax.set_ylim(0, 5.1)

        self.draw_rectangles()
        self.draw_flows()
        self.add_labels()

        plt.savefig("first.png", dpi=300)

    def size(self, col):
        return self.data.groupby(col).size()[::-1].values

    def draw_rectangles(self):
        width = 0.1
        self.ax.add_patch(
            Rectangle(
                xy=(0, 0),
                width=width,
                height=5,
                facecolor="#ff00007f",
            )
        )
        self.ax.add_patch(
            Rectangle(xy=(2, 0), width=width, height=2, facecolor="#00ff007f")
        )
        self.ax.add_patch(
            Rectangle(xy=(2, 2), width=width, height=3, facecolor="#0000ff7f")
        )

    def add_labels(self):
        fontsize = 16

        self.ax.text(
            s="one",
            x=-0.01,
            y=5 / 2,
            ha="right",
            fontsize=fontsize,
        )
        self.ax.text(s="two", x=2.11, y=2 / 2, ha="left", fontsize=fontsize)
        self.ax.text(
            s="three",
            x=2.11,
            y=2 + 3 / 2,
            ha="left",
            fontsize=fontsize,
        )

    def draw_flows(self):
        verts = [(0.1, 2), (1, 2), (1, 2), (2, 2)]
        path1 = p.Path(
            vertices=verts,
            codes=[p.Path.MOVETO, p.Path.CURVE4, p.Path.CURVE4, p.Path.CURVE4],
        )
        patch = PathPatch(path1, color="none", fc="none", lw=2)
        self.ax.add_patch(patch)

        verts = [(0.1, 0), (1, 0), (1, 0), (2, 0)]
        path2 = p.Path(
            vertices=verts,
            codes=[p.Path.MOVETO, p.Path.CURVE4, p.Path.CURVE4, p.Path.CURVE4],
        )
        patch = PathPatch(path2, color="none", fc="none", lw=2)
        self.ax.add_patch(patch)

        self.ax.fill_between(
            path1.vertices[:, 0],
            path1.vertices[:, 1],
            path2.vertices[:, 1],
            color="#00ff007f",
        )

        verts = [(0.1, 2), (1, 2), (1, 2), (2, 2)]
        path1 = p.Path(
            vertices=verts,
            codes=[p.Path.MOVETO, p.Path.CURVE4, p.Path.CURVE4, p.Path.CURVE4],
        )
        patch = PathPatch(path1, color="none", fc="none", lw=2)
        self.ax.add_patch(patch)

        verts = [(0.1, 5), (1, 5), (1, 5), (2, 5)]
        path2 = p.Path(
            vertices=verts,
            codes=[p.Path.MOVETO, p.Path.CURVE4, p.Path.CURVE4, p.Path.CURVE4],
        )
        patch = PathPatch(path2, color="none", fc="none", lw=2)
        self.ax.add_patch(patch)

        self.ax.fill_between(
            path1.vertices[:, 0],
            path1.vertices[:, 1],
            path2.vertices[:, 1],
            color="#0000ff7f",
        )


Alluvial(df=df, left="a", right="b")
