from matplotlib.patches import Rectangle, PathPatch
from scipy.special import comb
import matplotlib.pyplot as plt
import matplotlib.path as p
import pandas as pd
import numpy as np

df = pd.read_csv("third.csv")

example_colors = [
    "#a50026",
    "#d73027",
    "#f46d43",
    "#fdae61",
    "#fee090",
    "#e0f3f8",
    "#abd9e9",
    "#74add1",
    "#4575b4",
    "#313695",
]


class Alluvial:

    def __init__(self, df, left, right):
        self.fig, self.ax = plt.subplots(figsize=(5, 5), layout="constrained")

        self.left = left
        self.right = right

        self.data = df[[self.left, self.right]]
        sizes = self.size(self.right)

        self.left_heights = self.data.groupby([self.left]).size().values[::-1]
        self.right_heights = self.data.groupby([right]).size().values[::-1]

        self.rect_width = 0.1
        self.fontsize = 16
        self.gap = 0.2
        self.text_offset = 0.01
        self.flow_offset = 0.2
        self.x_values = range(0, len(sizes) + 1, len(sizes))

        self.colors = example_colors[: len(self.right_heights) + 1]

        self.draw_rectangles()
        self.draw_flow(hi_lo_y=(9, 5), cumulative_gap=2 * self.gap)
        self.draw_flow(hi_lo_y=(5, 2), cumulative_gap=1 * self.gap)
        self.draw_flow(hi_lo_y=(2, 0), cumulative_gap=0 * self.gap)
        self.add_labels()

        plt.axis("off")
        plt.savefig("first.png", dpi=300)

    def size(self, col):
        return self.data.groupby(col).size()[::-1].values

    def draw_rectangles(self):
        left_x, right_x = self.x_values

        self.draw_one_side(
            x=left_x,
            heights=self.left_heights,
            colors=self.colors[-len(self.left_heights) :],
        )
        self.draw_one_side(
            x=right_x,
            heights=self.right_heights,
            colors=self.colors[: len(self.right_heights) + 1],
        )

    def draw_one_side(self, x, heights, colors):

        cumulative_height = 0
        for height, fc in zip(heights, colors):
            self.ax.add_patch(
                Rectangle(
                    xy=(x, cumulative_height),
                    width=self.rect_width,
                    height=height,
                    fc=fc,
                )
            )
            cumulative_height += height + self.gap

    def add_labels(self):

        left_x, right_x = self.x_values

        self.add_labels_one_side(
            x=left_x,
            col=self.left,
            heights=self.left_heights,
            alignment="right",
            offset=-self.text_offset,
        )

        self.add_labels_one_side(
            x=right_x,
            col=self.right,
            heights=self.right_heights,
            alignment="left",
            offset=self.rect_width + self.text_offset,
        )

    def add_labels_one_side(self, x, col, heights, offset, alignment):

        cumulative_height = 0
        for s, h in zip(self.data[col].unique(), heights):

            self.ax.text(
                s=s,
                x=x + offset,
                y=cumulative_height + h / 2,
                ha=alignment,
                va="center",
                fontsize=self.fontsize,
            )
            cumulative_height += h + self.gap

    def draw_flow(self, hi_lo_y, cumulative_gap):

        left_x = self.x_values[0] + self.rect_width
        right_x = self.x_values[1]
        mid_x = (left_x + right_x) / 3

        hi_y, lo_y = hi_lo_y

        verts_top = [
            (left_x, hi_y),
            (mid_x, hi_y),
            (2 * mid_x, hi_y - self.flow_offset),
            (right_x, hi_y + cumulative_gap),
        ]
        verts_bottom = [
            (left_x, lo_y),
            (mid_x, lo_y),
            (2 * mid_x, lo_y + self.flow_offset),
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
