import polars as pl
import numpy as np
from website.scripts import get_all_games, get_liked_games, get_disliked_games, get_games
from tensorflow.keras.models import load_model


def recommend_something(user_id):
    print("recommending...")
    all_games = get_all_games()
    liked_games = get_liked_games(user_id)
    disliked_games = get_disliked_games(user_id)

    if len(liked_games) < 1:
        return []

    data = {
        'id': [g.id for g in all_games],
        'features': [g.recommendation_form for g in all_games]
    }

    df = pl.DataFrame(data)
    df = df.filter(pl.col('features').str.len_chars() > 1)

    ids_to_drop = [g.id for g in liked_games]
    liked_df = df.filter(pl.col('id').is_in(ids_to_drop))
    ids_to_drop += [g.id for g in disliked_games]
    df = df.filter(~pl.col('id').is_in(ids_to_drop))

    model = load_model('website/recommendation/siamese_model_v3.keras')

    recommendations = []
    THRESHOLD = 0.9999
    iterations = 0

    for _ in range(5):
        if liked_df.is_empty():
            break
        anchor = liked_df.sample(1)
        liked_df = liked_df.filter(pl.col('id') != anchor['id'])
        similarity = 0
        game = None
        anchor = np.array([anchor['features']])
        searching_df = df.filter(~pl.col('id').is_in(recommendations))
        while similarity < THRESHOLD:
            game = searching_df.sample(1)
            searching_df = searching_df.filter(pl.col('id') != game['id'])
            game_f = np.array([game['features'][0]])
            similarity = model.predict([anchor, game_f])
            iterations += 1
        recommendations.append(game['id'][0])

    print(f'Found {recommendations} in {iterations} iterations')
    return get_games(recommendations)
