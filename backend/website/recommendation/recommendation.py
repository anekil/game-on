import polars as pl
import numpy as np
from website.scripts import get_all_games, get_liked_games, get_disliked_games, get_games
from tensorflow.keras.models import load_model


def recommend_something(user_id):
    print("recommending...")
    all_games = get_all_games()
    liked_games = get_liked_games(user_id)
    disliked_games = get_disliked_games(user_id)

    data = {
        'id': [g.id for g in all_games],
        'features': [g.recommendation_form for g in all_games]
    }

    df = pl.DataFrame(data)
    liked_df = df.filter(pl.col('id').is_in(liked_games))
    df = df.filter(~pl.col('id').is_in(liked_df + disliked_games))

    model = load_model('siamese_model_v3.keras')

    recommendations = []

    THRESHOLD = 1
    iterations = 0
    for anchor in liked_df.iter_rows(named=True):
        similarity = 0
        game = None
        anchor = np.array(anchor['features'])
        searching_df = df.clone()
        while similarity < THRESHOLD:
            game = searching_df.sample(1)
            searching_df = searching_df.filter(pl.col('id') != game['id'])
            game_f = np.array(game['features'])
            similarity = model.predict([anchor, game_f])
            iterations += 1
        if game:
            recommendations.append(game['id'])

    print(f'Found in {iterations} iterations')
    return get_games(recommendations)
