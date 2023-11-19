from requests import request
from models import Game, Genre, Theme, Keyword
from . import db


def fetch_games_data():
    url = "https://api.igdb.com/v4/games"
    payload = "fields name, url, summary, cover.url, total_rating, genres, themes, keywords, screenshots.url; limit 200; where total_rating > 50 & category = 0; sort total_rating_count desc; "
    headers = {
        'Authorization': 'Bearer 7uasv2bw3iyqjavppma1c5yntc1geo',
        'Client-ID': 't6vglpbbejgf6vm4ptt5q5lsrlros2',
    }
    response = request("POST", url, headers=headers, data=payload)
    api_data = response.json()
    for game_json in api_data:
        genre_ids = game_json.get("genres", [])
        genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
        theme_ids = game_json.get("themes", [])
        themes = Theme.query.filter(Theme.id.in_(theme_ids)).all()
        keywords_ids = game_json.get("keywords", [])
        keywords = Keyword.query.filter(Keyword.id.in_(keywords_ids)).all()

        game_data = Game(
            api_id=game_json['id'],
            name=game_json['name'],
            url=game_json['url'],
            summary=game_json['summary'],
            cover=game_json.get("cover", {}).get("url"),
            total_rating=round(game_json['total_rating']),
            genres=genres,
            themes=themes,
            keywords=keywords,
            screenshots=[item["url"] for item in game_json.get("screenshots", [])]
        )
        db.session.add(game_data)
    db.session.commit()


def fetch_items(items_name):
    url = "https://api.igdb.com/v4/" + items_name
    payload = "fields id, name; limit 500;"
    headers = {
        'Authorization': 'Bearer 7uasv2bw3iyqjavppma1c5yntc1geo',
        'Client-ID': 't6vglpbbejgf6vm4ptt5q5lsrlros2',
    }
    response = request("POST", url, headers=headers, data=payload)
    return response.json()


def fetch_all_classification_data():
    genres = fetch_items("genres")
    for genre in genres:
        genre_data = Genre(
            id=genre['id'],
            name=genre['name'],
        )
        db.session.add(genre_data)
    themes = fetch_items("themes")
    for theme in themes:
        theme_data = Theme(
            id=theme['id'],
            name=theme['name'],
        )
        db.session.add(theme_data)
    keywords = fetch_items("keywords")
    for keyword in keywords:
        keyword_data = Keyword(
            id=keyword['id'],
            name=keyword['name'],
        )
        db.session.add(keyword_data)
    db.session.commit()
