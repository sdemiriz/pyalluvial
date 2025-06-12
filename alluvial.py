from matplotlib.patches import Rectangle, PathPatch
from scipy.special import comb
import matplotlib.pyplot as plt
import matplotlib.path as p
import pandas as pd
import numpy as np

df = pd.read_csv("first.csv")


class Alluvial:

    def __init__(self, df, left, right):
        self.fig, self.ax = plt.subplots(figsize=(5, 5), layout="constrained")

        self.data = df[[left, right]]
        sizes = self.size(right)

        self.right_heights = self.data.groupby([left, right]).size().values[::-1]

        self.rect_width = 0.1
        self.fontsize = 16
        self.gap = 0.2
        self.x_values = range(0, len(sizes) + 1, len(sizes))

        self.colors = ["#00ff00ff", "#0000ffff"]

        self.draw_rectangles()
        self.draw_flow(hi_lo_y=(5, 2), cumulative_gap=self.gap)
        self.draw_flow(hi_lo_y=(2, 0), cumulative_gap=0)
        self.add_labels()

        plt.axis("off")
        plt.savefig("first.png", dpi=300)

    def size(self, col):
        return self.data.groupby(col).size()[::-1].values

    def draw_rectangles(self):
        left_x, right_x = self.x_values

        cumulative_height = 0
        for height, fc in zip(self.right_heights, self.colors):
            self.ax.add_patch(
                Rectangle(
                    xy=(right_x, cumulative_height),
                    width=self.rect_width,
                    height=height,
                    fc=fc,
                )
            )
            cumulative_height += height + self.gap

        self.ax.add_patch(
            Rectangle(
                xy=(left_x, 0),
                width=self.rect_width,
                height=sum(self.right_heights)
                + (len(self.right_heights) - 1) * self.gap,
                facecolor="#ff0000ff",
            )
        )

    def add_labels(self):

        self.ax.text(
            s="one",
            x=-0.01,
            y=5 / 2,
            ha="right",
            fontsize=self.fontsize,
        )
        self.ax.text(s="two", x=2.11, y=2 / 2, ha="left", fontsize=self.fontsize)
        self.ax.text(
            s="three",
            x=2.11,
            y=2 + 3 / 2,
            ha="left",
            fontsize=self.fontsize,
        )

    def draw_flow(self, hi_lo_y, cumulative_gap):

        left_x = self.x_values[0] + self.rect_width
        right_x = self.x_values[1]
        mid_x = (left_x + right_x) / 3

        hi_y, lo_y = hi_lo_y

        verts_top = [
            (left_x, hi_y + cumulative_gap),
            (mid_x, hi_y),
            (2 * mid_x, hi_y),
            (right_x, hi_y + cumulative_gap),
        ]
        verts_bottom = [
            (left_x, lo_y),
            (mid_x, lo_y),
            (2 * mid_x, lo_y),
            (right_x, lo_y + cumulative_gap),
        ]

        curve1 = self.bezier_curve(verts_top, num_points=50)
        curve2 = self.bezier_curve(verts_bottom, num_points=50)

        self.ax.fill_between(
            x=curve1[:, 0],
            y1=curve1[:, 1],
            y2=curve2[:, 1],
            color="#0000ff7f",
            edgecolor="none",
        )

    @staticmethod
    def bezier_curve(points, num_points):
        n = len(points) - 1
        t = np.linspace(0, 1, num_points)
        curve_points = np.zeros((num_points, 2))

        for i in range(n + 1):
            bernstein = comb(n, i) * (t**i) * ((1 - t) ** (n - i))
            curve_points += np.outer(bernstein, points[i])

        return curve_points


Alluvial(df=df, left="a", right="b")
