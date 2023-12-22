import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from website import db
from website.models import Game


def recommend_something():
    print("recommending...")
    games = (db.session.query(Game).all())
             #.filter(Game.hypes.isnot(None), Game.total_rating_count.isnot(None))
             #.order_by(Game.total_rating_count.desc()).all())
    columns = ['id', 'name', 'summary', 'storyline', 'total_rating', 'total_rating_count', 'genres', 'themes', 'keywords', 'modes']
    # data = [(g.name, g.name, g.summary, g.storyline, g.total_rating, g.total_rating_count, [x.name for x in g.genres], [x.name for x in g.themes], [x.name for x in g.keywords], [x.name for x in g.modes]) for g in games]
    # df = pd.DataFrame(data, columns=columns)
    # df['description'] = df['summary'].fillna('') + df['storyline'].fillna('')
    # df['description'] = df['description'].replace('', pd.NA)
    # df = df.drop(['summary', 'storyline'], axis=1)
    # df = df.dropna()

    return ["hello"]

    ## SIMPLEST RECOMMENDATION
    # df['summary'] = df['summary'].fillna('')
    # df['storyline'] = df['storyline'].fillna('')
    #
    # df['description'] = df['summary'] + ' ' + df['storyline']
    # tfidf = TfidfVectorizer(stop_words='english')
    # tfidf_matrix = tfidf.fit_transform(df['description'])
    # cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # indices = pd.Series(df.index, index=df['name']).drop_duplicates()
    #
    # def get_recommendations(title, cosine_sim=cosine_sim, num_recommend=10):
    #     idx = indices[title]
    #     sim_scores = list(enumerate(cosine_sim[idx]))
    #     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #     top_similar = sim_scores[1:num_recommend + 1]
    #     game_indices = [i[0] for i in top_similar]
    #     return df['name'].iloc[game_indices]
    #
    # return get_recommendations('Between the Stars')


def get_statistics():
    games = db.session.query(Game).options(db.joinedload(Game.keywords)).all()

    columns = ['id', 'name', 'keywords']
    data = [(game.id, game.name, [keyword.id for keyword in game.keywords]) for game in games]

    df = pd.DataFrame(data, columns=columns)

    keyword_counts = pd.Series([keyword_id for keyword_ids in df['keywords'] for keyword_id in keyword_ids]).value_counts()

    plt.bar(keyword_counts.index, keyword_counts.values)
    plt.yscale('log')
    plt.ylim(top=150)
    plt.xlabel('Keyword IDs')
    plt.ylabel('Number of Games')
    plt.title('Number of Games for Each Keyword ID')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url