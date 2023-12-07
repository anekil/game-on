from requests import request
from sqlalchemy import update


from . import db
from .models import Game, Genre, Theme, Keyword, Mode, Platform, Rating


def fetch_games_data():
    all_games_counter = 0
    games_counter = 1
    offset = 0
    while games_counter > 0:
        url = "https://api.igdb.com/v4/games"
        payload = f"fields id, name, slug, url, summary, cover.url, total_rating, hypes, genres, themes, keywords, game_modes, platforms, screenshots.url; limit 500; where total_rating > 50 & category = 0; sort total_rating_count desc; offset {offset};"
        headers = {
            'Authorization': 'Bearer 7uasv2bw3iyqjavppma1c5yntc1geo',
            'Client-ID': 't6vglpbbejgf6vm4ptt5q5lsrlros2',
        }
        response = request("POST", url, headers=headers, data=payload)
        api_data = response.json()

        games_counter = 0
        for game_json in api_data:
            if Game.query.get(int(game_json['id'])) is None:
                genre_ids = game_json.get("genres", [])
                genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()
                theme_ids = game_json.get("themes", [])
                themes = Theme.query.filter(Theme.id.in_(theme_ids)).all()
                keywords_ids = game_json.get("keywords", [])
                keywords = Keyword.query.filter(Keyword.id.in_(keywords_ids)).all()
                modes_ids = game_json.get("game_modes", [])
                modes = Mode.query.filter(Mode.id.in_(modes_ids)).all()
                platforms_ids = game_json.get("platforms", [])
                platforms = Platform.query.filter(Platform.id.in_(platforms_ids)).all()

                game_data = Game(
                    id=game_json['id'],
                    name=game_json['name'],
                    slug=game_json['slug'],
                    url=game_json['url'],
                    summary=game_json.get('summary'),
                    storyline=game_json.get('storyline'),
                    cover=game_json.get('cover', {}).get('url'),
                    total_rating=round(game_json.get('total_rating')),
                    total_rating_count=game_json.get('total_rating_count'),
                    hypes=game_json.get('hypes'),
                    genres=genres,
                    themes=themes,
                    keywords=keywords,
                    modes=modes,
                    platforms=platforms,
                    screenshots=[item["url"] for item in game_json.get("screenshots", [])]
                )
                db.session.add(game_data)
                games_counter += 1
        db.session.commit()
        offset += 500
        all_games_counter += games_counter
    print(f'Successfully added {all_games_counter} games')


def fetch_items(items_name, filters="", offset=0):
    url = "https://api.igdb.com/v4/" + items_name
    payload = f"fields id, name; limit 500; offset {offset};" + filters
    headers = {
        'Authorization': 'Bearer 7uasv2bw3iyqjavppma1c5yntc1geo',
        'Client-ID': 't6vglpbbejgf6vm4ptt5q5lsrlros2',
    }
    response = request("POST", url, headers=headers, data=payload)
    return response.json()


def fetch_all_classification_data():
    genres_counter = 0
    for item in fetch_items("genres"):
        if Genre.query.get(int(item['id'])) is None:
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
    for item in fetch_items("platforms", "where id = (39, 34, 6, 3, 14, 163, 162, 11, 7, 41);"):
        if db.session.get(Platform, item['id']) is None:
            data = Platform(
                id=item['id'],
                name=item['name'],
            )
            db.session.add(data)
            keywords_counter += 1
    db.session.commit()
    print(f'Successfully added {genres_counter} genres, {themes_counter} themes, {keywords_counter} keywords, {modes_counter} modes and {platforms_counter} platforms')


def get_all_games():
    return db.session.execute(db.select(Game).order_by(Game.total_rating)).scalars()


def get_game(slug):
    return db.session.execute(db.select(Game).where(Game.slug.in_([slug]))).scalars().first()


def get_game_rating(user_id, game_id):
    return Rating.query.filter_by(user_id=user_id, game_id=game_id).first()


def save_user_rating(user_id, game_id, new_rating):
    rating = db.session.execute(db.select(Rating).where(Rating.game_id == game_id, Rating.user_id == user_id)).scalar()
    if rating is None:
        rating = Rating(
            rating=new_rating,
            user_id=user_id,
            game_id=game_id
        )
        db.session.add(rating)
    else:
        db.session.execute(update(Rating).where(Rating.id == rating.id).values(rating=new_rating))
    db.session.commit()


def delete_rating(rating_id, user):
    rating = Rating.query.get(rating_id)
    if rating:
        if rating.user_id == user.id:
            db.session.delete(rating)
            db.session.commit()
