from flask import Blueprint, render_template
from .db import get_db

bp = Blueprint('music', __name__, url_prefix='/')


@bp.route('/')
def base():
    return render_template('base.html')


@bp.route('/names/')
def unique_artists_amount_view():
    db = get_db()
    artists = db.execute(
        """SELECT COUNT(DISTINCT artist) AS cnt
        FROM tracks"""
    ).fetchone()
    context = str(artists['cnt'])
    return render_template('names.html', context=context)


@bp.route('/tracks/')
def number_of_tracks_view():
    db = get_db()
    tracks_cnt = db.execute(
        """SELECT COUNT(ALL id) AS tr_cnt
         FROM tracks"""
    ).fetchone()
    context = str(tracks_cnt['tr_cnt'])
    return render_template('tracks.html', context=context)


@bp.route('/genres/')
def available_genres_view():
    cont = get_db().execute(
        'SELECT title FROM genres'
    ).fetchall()
    return render_template('genres.html', cont=cont)


@bp.route('/tracks/<genre>')
def tracks_of_genre_view(genre: str):
    db = get_db()
    tracks_by_genre = db.execute(
        """SELECT COUNT(tracks.title) AS cnt
        FROM tracks
        INNER JOIN genres ON tracks.genre_id=genres.id
        WHERE genres.title=?""", (genre,)).fetchone()
    return render_template('tracks-genres.html', trgr=tracks_by_genre, genre=genre)


@bp.route('/tracks-sec/')
def tracks_title_len_view():
    cont = get_db().execute(
        """SELECT title, length
        FROM tracks"""
    ).fetchall()
    return render_template('tracks-sec.html', cont=cont)


@bp.route('/tracks-sec/statistics/')
def tracks_stat_view():
    cont = get_db().execute(
        """SELECT SUM(length) AS sumlen, AVG(length) AS avglen
         FROM tracks"""
    ).fetchone()
    return render_template('tracks-stats.html', cont=cont)
