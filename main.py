import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib.lines import Line2D

from rbf import RBF

#
# Setup matplotlib
#
matplotlib.use("QtAgg")

#
# Setup dataframe
#
df = pd.read_csv("owid-covid-data.csv")
df = df.loc[df["location"] == "Brazil"]
df["weekly_new_deaths_mean"] = df["new_deaths"].rolling(window=7).mean()
df["weekly_new_cases_mean"] = df["new_cases"].rolling(window=7).mean()
df["weekly_new_deaths_mean"] = df["weekly_new_deaths_mean"].fillna(method="ffill")
df["weekly_new_cases_mean"] = df["weekly_new_cases_mean"].fillna(method="ffill")
df.fillna(method="ffill", inplace=True)
df = df[::7]


#
# Render
#
def render(sigma, lambda_, alpha, delta):
    fig, ax_left = plt.subplots()

    plt.rcParams.update({"font.size": 12})
    fig.set_size_inches(12, 8)
    plt.title("COVID-19 in Brazil: Vaccination, Cases, and Deaths", fontsize=16)

    ax_right = ax_left.twinx()
    ax_third = ax_left.twinx()

    ax_left.plot(
        df["date"],
        df["people_vaccinated"],
        color="navy",
        linestyle="-",
        linewidth=1.00,
    )

    ax_left.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    ax_left.grid(True, linestyle="--", alpha=0.7)

    ax_right.plot(
        df["date"],
        df["weekly_new_deaths_mean"],
        color="red",
        linestyle="-",
        linewidth=1.00,
    )

    ax_third.plot(
        df["date"],
        df["weekly_new_cases_mean"],
        color="lightgreen",
        linestyle="-",
        linewidth=1.00,
    )

    xticks = []

    rbf = RBF(**{"sigma": sigma, "lambda_": lambda_, "alpha": alpha, "delta": delta})
    total_concept_changes = 0

    for index, row in df.iterrows():
        date = df["date"][index]
        value = row["weekly_new_deaths_mean"]

        rbf.add_element(value)

        if rbf.in_concept_change:
            total_concept_changes += 1
            ax_left.axvline(date, color="orange", ls="--", linewidth=1.00)
            xticks.append(date)

    ax_left.tick_params(axis="x", labelrotation=90)
    ax_right.tick_params(axis="x", labelrotation=90)

    ax_left.tick_params(axis="y", colors="navy")
    ax_right.tick_params(axis="y", colors="red")

    ax_third.tick_params(axis="y", colors="lightgreen")
    ax_third.get_yaxis().set_visible(False)

    ax_right.set_xticks(xticks)

    for tick in ax_right.xaxis.get_minor_ticks():
        tick.label1.set_horizontalalignment("right")

    plt.gcf().subplots_adjust(bottom=0.15)

    custom_legends = [
        Line2D([0], [0], color="navy", linestyle="-", linewidth=2),
        Line2D([0], [0], color="lightgreen", ls="-", linewidth=2),
        Line2D([0], [0], color="red", ls="-", linewidth=2),
        Line2D([0], [0], color="orange", ls="--", linewidth=2),
    ]
    legend = plt.legend(
        custom_legends,
        [
            "People Vaccinated",
            "Cases",
            "Deaths",
            f"Concept Drift (Deaths)",
        ],
        ncol=2,
        borderaxespad=0,
        loc="upper left",
    )
    legend.get_frame().set_alpha(None)

    # axis labels
    ax_left.set_ylabel("People Vaccinated", color="navy", fontsize=12)
    ax_right.set_ylabel("Weekly Deaths (7-day avg)", color="red", fontsize=12)
    ax_left.set_xlabel("Date", fontsize=12)

    plt.savefig(
        "plot.png",
        dpi=300,
        bbox_inches="tight",
        format="png",
        facecolor="white",
        edgecolor="none",
        transparent=False,
    )
    print(f"Total Centers: {len(rbf.centers)=}")


#
# Streamlit UI
#
st.set_page_config(layout="wide")
st.title("RMIDDM - COVID19 Experiment")
st.warning(
    "Refresh the page to reset the parameters to their default values."
)

sigma = st.slider(
    "Sigma - Width (spread) of the Gaussian function utilized during the activation process",
    min_value=0.01,
    max_value=1.0,
    value=0.01,
    step=0.01,
)
lambda_ = st.slider(
    "Lambda - Minimum activation threshold required for a group (or unit)",
    min_value=0.01,
    max_value=1.0,
    value=0.5,
    step=0.01,
)
alpha = st.slider(
    "Alpha - Increment value applied to update transition metrics upon the occurrence of a transition",
    min_value=0.01,
    max_value=1.0,
    value=0.5,
    step=0.01,
)
delta = st.slider(
    "Delta - Minimum probability threshold for the detection of concept drift",
    min_value=0.01,
    max_value=1.0,
    value=1.0,
    step=0.01,
)

if st.button("▶ Render"):
    render(**{"sigma": sigma, "lambda_": lambda_, "alpha": alpha, "delta": delta})
    st.image("plot.png")
