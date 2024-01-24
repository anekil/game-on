import polars as pl
from website.scripts import get_all_games, get_games


def recommend_something():
    print("recommending...")
    # games = get_games_with_features()
    # games = join_features(games)

    ids = [11, 12, 13]
    return get_games(ids)


def get_games_with_features():
    def extract_name(items):
        return [x.name for x in items]

    games = get_all_games()
    data = {
            'id': [g.id for g in games],
            'genres': [extract_name(g.genres) for g in games],
            'themes': [extract_name(g.themes) for g in games],
            'keywords': [extract_name(g.keywords) for g in games],
    }
    features_df = pl.DataFrame(data)
    return features_df


def join_features(features_df):
    def clean_and_join(row):
        return " ".join(sorted(["".join(filter(str.isalpha, i)) for i in row]))

    features = ["genres", "themes", "keywords"]
    features_df = features_df.with_columns([
            pl.col(features).map_elements(lambda row: clean_and_join(row))
    ])
    features_df = features_df.with_columns(
        pl.concat_str(
            pl.col(features), separator=" "
        ).alias("features")
    )
    features_df = features_df.drop(features)
    return features_df

