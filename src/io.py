import pandas as pd


def to_pandas(subreddit_data, seperate=False):
    dfs = dict()

    for subreddit, data in subreddit_data.items():
        dfs[subreddit] = pd.DataFrame(data)

    if seperate:
        return dfs
    else:
        return pd.concat(dfs.values(), ignore_index=True)


def update_data(csv_path, df, key="id", sort="subreddit_name", save=False):
    old_df = pd.read_csv(csv_path)
    new_df = (
        pd.concat([old_df, df], ignore_index=True)
        .drop_duplicates(subset=[key], ignore_index=True)
        .sort_values(sort, ignore_index=True)
    )

    if save:
        new_df.to_csv(csv_path, index=False)

    return new_df
