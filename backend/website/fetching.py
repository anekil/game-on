from requests import request
import time
from . import db
from .models import Game, Genre, Theme, Keyword, Mode, Platform
from .secrets import TOKEN, CLIENT_ID


def clean_and_join(row):
    words = sorted(["".join(filter(str.isalpha, i)) for i in row])
    words = ' '.join([w for w in words if len(w) > 3])
    return words.strip()


def extract_name(items):
    return [x.name for x in items]


def fetch_games_data():
    all_games_counter = 0
    games_counter = 1
    offset = 0
    while games_counter > 0:
        time.sleep(0.5)
        url = "https://api.igdb.com/v4/games"
        payload = (f"fields id, name, slug, url, summary, storyline, cover.url, total_rating, total_rating_count, "
                   f"hypes, genres, themes, keywords, game_modes, platforms, screenshots.url, similar_games; limit 500;"
                   f" where total_rating_count > 0 & category = 0; sort total_rating_count desc; offset {offset};")
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Client-ID': CLIENT_ID,
        }
        response = request("POST", url, headers=headers, data=payload)
        api_data = response.json()

        games_counter = 0
        game_info_dict = {}
        for game_json in api_data:
            game_id = int(game_json['id'])

            genres = Genre.query.filter(Genre.id.in_(game_json.get("genres", []))).all()
            themes = Theme.query.filter(Theme.id.in_(game_json.get("themes", []))).all()
            keywords = Keyword.query.filter(Keyword.id.in_(game_json.get("keywords", []))).all()

            game_info_dict[game_id] = {
                'name': game_json['name'],
                'slug': game_json['slug'],
                'url': game_json['url'],
                'summary': str(game_json.get('summary')).replace("\n", ""),
                'storyline': str(game_json.get('storyline')).replace("\n", ""),
                'cover': game_json.get('cover', {}).get('url'),
                'total_rating': round(game_json.get('total_rating')),
                'total_rating_count': game_json.get('total_rating_count'),
                'hypes': game_json.get('hypes'),
                'genres': genres,
                'themes': themes,
                'keywords': keywords,
                'modes': Mode.query.filter(Mode.id.in_(game_json.get("game_modes", []))).all(),
                'platforms': Platform.query.filter(Platform.id.in_(game_json.get("platforms", []))).all(),
                'screenshots': [item["url"] for item in game_json.get("screenshots", [])],
                'similar_games': game_json.get("similar_games", []),
                'recommendation_form': clean_and_join(extract_name(genres) + extract_name(themes) + extract_name(keywords))
            }

        for game_id, game_info in game_info_dict.items():
            existing_game = Game.query.get(game_id)

            if existing_game:
                for key, value in game_info.items():
                    setattr(existing_game, key, value)
                db.session.merge(existing_game)
                games_counter += 1
            else:
                new_game = Game(id=game_id, **game_info)
                db.session.add(new_game)
                games_counter += 1

        db.session.commit()
        offset += 500
        all_games_counter += games_counter
    print(f'Successfully added {all_games_counter} games')


def fetch_items(items_name, filters="", offset=0):
    time.sleep(0.25)
    url = "https://api.igdb.com/v4/" + items_name
    payload = f"fields id, name; limit 500; offset {offset};" + filters
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Client-ID': CLIENT_ID
    }
    response = request("POST", url, headers=headers, data=payload)
    return response.json()


def fetch_all_classification_data():
    genres_counter = 0
    for item in fetch_items("genres"):
        if db.session.get(Genre, item['id']) is None:
            data = Genre(
                id=int(item['id']),
                name=item['name'],
            )
            db.session.add(data)
            genres_counter += 1

    themes_counter = 0
    for item in fetch_items("themes"):
        if db.session.get(Theme, item['id']) is None:
            data = Theme(
                id=item['id'],
                name=item['name'],
            )
            db.session.add(data)
            themes_counter += 1

    all_keywords_counter = 0
    keywords_counter = 1
    offset = 0
    while keywords_counter > 0:
        keywords_counter = 0
        for item in fetch_items("keywords", offset=offset):
            if db.session.get(Keyword, item['id']) is None:
                data = Keyword(
                    id=item['id'],
                    name=item['name'],
                )
                db.session.add(data)
                keywords_counter += 1
        db.session.commit()
        offset += 500
        all_keywords_counter += keywords_counter

    modes_counter = 0
    for item in fetch_items("game_modes"):
        if db.session.get(Mode, item['id']) is None:
            data = Mode(
                id=item['id'],
                name=item['name'],
            )
            db.session.add(data)
            modes_counter += 1

    platforms_counter = 0
    for item in fetch_items("platforms", " fields platform_logo.url; "
                                         "where id = (39, 34, 6, 3, 14, 163, 162, 11, 7, 41);"):
        if db.session.get(Platform, item['id']) is None:
            data = Platform(
                id=item['id'],
                name=item['name'],
                platform_logo=item.get('platform_logo', {}).get('url'),
            )
            db.session.add(data)
            platforms_counter += 1
    db.session.commit()
    print(f'Successfully added {genres_counter} genres, {themes_counter} themes, {all_keywords_counter} keywords, '
          f'{modes_counter} modes and {platforms_counter} platforms')
