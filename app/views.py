from flask import render_template, flash, request, redirect
from sqlalchemy import false
from app import app, db, models, admin, logging
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
import json

from .forms import LoginForm, RegistrationForm, RatingForm

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Album, db.session))
admin.add_view(ModelView(models.Artist, db.session))
admin.add_view(ModelView(models.Genre, db.session))
admin.add_view(ModelView(models.Rating, db.session))

# take an album's id, and recalculate the overall rating for it based on all of its ratings 
def update_overall_rating(album_id):
    album = models.Album.query.filter_by(id=album_id).first()
    ratings=album.ratings
    count=0
    sum=0
    for rating in ratings:
        count+=1
        sum+=rating.rating
    new_rating = sum/count
    album.rating=round(new_rating, 2)
    logging.info('Updated overall rating to {}/10'.format(album.rating))
    db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/'
        logging.info('Login successful!')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        logging.info('User #{} now registered'.format(user.id))
        
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)

@app.route('/')
def index():
    return render_template('index.html',
                           title='TrackTracker')

@app.route('/top', methods=['GET', 'POST'])
def top():
    # order albums in descending order of overall rating
    albums = models.Album.query.order_by(models.Album.rating.desc()).all()
    return render_template('top_albums.html', title='Top albums', albums=albums)
    
@app.route('/top-reviews', methods=['GET', 'POST'])
def featured_reviews():
    # order reviews in descending order of most-liked
    ratings = models.Rating.query.order_by(models.Rating.likes.desc()).all()
    return render_template('top_reviews.html', title='Top albums', ratings=ratings)

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    albums = models.Album.query.all()
    return render_template('albums.html', title='Albums', albums=albums)

@app.route('/album', methods=['GET', 'POST'])
def album():
    # Get the album ID from the GET paramater - this allows bookmarking of individual album pages
    album_id = request.args.get('id')
    if ('rating' in request.form):
        return redirect('/add_rating?id=' + album_id)
    if not album_id:
        # With no ID provided, default to N/A and set Album to False to provide an error page
        logging.error('Album not found!')
        album_id = 'N/A'
        album = False
    else:
        # Select the album entry corresponding to the ID
        album = models.Album.query.filter_by(id=album_id)

        # Get the entry from the query's returned entries (there should only be one) and default to False if no entries available
        if album.first() is not None:
            album=album[0]
        else:
            album=False
    logging.info('Viewing album #{}'.format(album_id))
    return render_template('album.html',
                           title='View album #' + album_id,
                           album=album)


@app.route('/add_rating', methods=['GET', 'POST'])
@login_required
def add_rating():
    album_id = request.args.get('id')
    form = RatingForm()
    if form.validate_on_submit():
        rating = models.Rating(rating=form.rating.data,
        review=form.review.data,
        likes=0,
        user_id=current_user.id,
        album_id=album_id
        )
        db.session.add(rating)
        db.session.commit()
        logging.info('Added new rating to database: user #{} rated album #{} a {}/10'.format(current_user.id, album_id, form.rating.data ))
        update_overall_rating(album_id)
        flash('Added new rating')
    return render_template('add_rating.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    ratings = models.Rating.query.filter_by(user_id=current_user.id).all()
    logging.info('Retrieved all ratings for user#{}'.format(current_user.id))
    return render_template('profile.html', title='Profile', ratings=ratings)

@app.route('/rating', methods=['GET', 'POST'])
def rating():
    # Get the rating ID from the GET paramater - this allows bookmarking of individual rating pages
    rating_id = request.args.get('id')
    if not rating_id:
        # With no ID provided, default to N/A and set rating to False to provide an error page
        rating_id = 'N/A'
        rating = False
        logging.error('Rating not found!')
    else:
        # Select the album entry corresponding to the ID
        rating = models.Rating.query.filter_by(id=rating_id)

        # Get the entry from the query's returned entries (there should only be one) and default to False if no entries available
        if rating.first() is not None:
            rating=rating[0]
            logging.info('Rating found!')
        else:
            rating=False
            logging.error('Rating not found!')

    return render_template('rating.html',
                           title='View rating #' + rating_id,
                           rating=rating)

@app.route('/like', methods=['POST'])
def like():
    if not current_user.is_authenticated:
        return None
    # Load the JSON data and use the ID of the idea that was clicked to get the object
    data = json.loads(request.data)
    rating_id = int(data.get('rating_id'))
    rating = models.Rating.query.get(rating_id)
    rating.likes += 1
    logging.info('Incremented likes for rating #{}'.format(rating_id))

    # Save the updated vote count in the DB
    db.session.commit()
    # Tell the JS .ajax() call that the data was processed OK
    return json.dumps({'status':'OK','likes': rating.likes })