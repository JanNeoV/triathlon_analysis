# this is simply a helper python file containing all functions I will re-use so I dont have to copy-paste code all that much
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from math import pi


def load_results(path: Path) -> pd.DataFrame: ### function returns data frame
    df = pd.read_csv(path)

    ### get only stem

    base = path.stem

    ### split data accordingly since they have always names like ironman70.3aix-en-provence2011__1181
    # the last 4 digits represent the file number from my scraping job(we can safely cut that)
    # the last 4 digits before the underscore represent the year
    # otherwise, I would keep it simple as is because the race name and location are not always clear

    race_year = base.split("__")[0]

    ### last 4 characters are always race year

    year = int(race_year[-4:])
    race = race_year[:-4]

    df["race"] = race
    df["year"] = year

    # create unique id (file name)
    df["event_id"] = base
    # now extract if race was 70.3 or full distance
    stem_lower = base.lower()
    if "70.3" in stem_lower or "70_3" in stem_lower:
        df["distance"] = "70.3"
    else:
        df["distance"] = "full-distance"
    return df


def add_relative_strength(df):
    df = df.copy()
    group_cols = ["race", "year", "gender", "event_id"] ## actually, gender and event_id should be enough

    ### overall percetile
    df["overall_rel"] = (
        df.groupby(group_cols)["Overall Time (s)"]
        .rank(method="average", pct = True, ascending = True)
    )

    ### lowest time is best

    df["overall_rel"] = 1 - df["overall_rel"]

    for col, new_col in [
        ("Swim Time (s)", "swim_rel"),
        ("Bike Time (s)", "bike_rel"),
        ("Run Time (s)", "run_rel"),
    ]:
        perc = (
            df.groupby(group_cols)[col]
            .rank(method="average", pct = True, ascending = True)
        )
        df[new_col] = 1 - perc
    
    return df

def cluster_diagnostics(
        X,
        k_range = DEFAULT_K_RANGE,
        random_state = RANDOM_STATE,
        title_suffix="",
):
    # this is obviously an optionated choice and may be adjusted if needed
    # however, we only have 2M data points in total and silhoutte score scales with ~ O(n^2)
    X_sample = X.sample(50000, random_state=random_state)

    inertias = []
    sil_scores = []

    # here we are fitting k-means on the sample we use for each k in the range
    for k in k_range:
        km = KMeans(
            n_clusters = k,
            random_state = random_state,
            n_init="auto"
        )
        labels = km.fit_predict(X_sample)
        inertias.append(km.inertia_) # fill empty array

        # now approximate silhouette

        sil_score = silhouette_score(
            X_sample,
            labels,
        )
        
        sil_scores.append(sil_score) # fill empty array

    # now plot everything
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(list(k_range), inertias, marker="o")
    axes[0].set_xlabel("Number of clusters k")
    axes[0].set_ylabel("Inertia (within-cluster SSE)")
    axes[0].set_title(f"Elbow method{(' – ' + title_suffix) if title_suffix else ''}")

    axes[1].plot(list(k_range), sil_scores, marker="o")
    axes[1].set_xlabel("Number of clusters k")
    axes[1].set_ylabel("Silhouette score")
    axes[1].set_title(f"Silhouette scores{(' – ' + title_suffix) if title_suffix else ''}")

    plt.tight_layout()
    plt.show()

    return {
        "k": list(k_range),
        "inertia": inertias,
        "silhouette": sil_scores,
    }

def fit_kmeans_and_add_labels(
    df,
    feature_cols,
    n_clusters,
    random_state=RANDOM_STATE,
    label_col="cluster_all",
    row_mask=None,
):

    df_out = df.copy()

    # default would be all the data with all features
    if row_mask is None:
        mask = df_out[feature_cols].notna().all(axis=1)
    else:
        # otherwise masked data, e.g. subset + all features
        # this simply ensures that we only label what is relevent
        mask = row_mask & df_out[feature_cols].notna().all(axis=1)

    X_clean = df_out.loc[mask, feature_cols]

    km = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init="auto",
    )
    labels = km.fit_predict(X_clean)

    # write back labels to columns and drop irrelevant rows
    # e.g., if we look only at top 10%, we dont have to consider 90% of the data for mapping
    df_out[label_col] = np.nan
    df_out.loc[mask, label_col] = labels

    return df_out, km

def make_cluster_summary(df, cluster_col="cluster_all"):
    df = df.dropna(subset=[cluster_col]).copy()
    df[cluster_col] = df[cluster_col].astype(int)

    n_total = len(df)

    summary = (
        df
        .groupby(cluster_col)
        .agg(
            n=(cluster_col, "size"),
            mean_swim=("swim_rel", "mean"),
            mean_bike=("bike_rel", "mean"),
            mean_run=("run_rel", "mean"),
            median_overall_rel=("overall_rel", "median"),
            mean_overall_rel=("overall_rel", "mean"),
        )
        .reset_index()
    )

    summary["share"] = summary["n"] / n_total
    return summary

### creating a radar chart
def plot_cluster_radar(summary_df, cluster_col, name_map, title="Archetype profiles"):
    disciplines = ["Swim", "Bike", "Run"]
    num_vars = len(disciplines)

    # angle for axes
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # close cricle

    fig = plt.figure(figsize=(6, 6)) ## standard plot sizes below another 
    ax = plt.subplot(111, polar=True)

    ax.set_ylim(0, 1)

    for _, row in summary_df.iterrows():
        cid = int(row[cluster_col])
        name = name_map.get(cid, f"Cluster {cid}")

        values = [row["mean_swim"], row["mean_bike"], row["mean_run"]]
        values += values[:1]

        ax.plot(angles, values, marker="o", label=name)
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(disciplines)
    ax.set_title(title)
    ax.set_rlabel_position(0)

    plt.legend(loc="upper right", bbox_to_anchor=(1.4, 1.1))
    plt.show()