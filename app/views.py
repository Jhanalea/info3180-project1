"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from app.form import AddPropertyForm
from app.models import Property


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties')
def properties():
    properties = db.session.execute(db.select(Property)).scalars()
    return render_template('properties.html', properties=properties)

@app.route('/properties/create', methods=['POST', 'GET'])
def new_property():
    form = AddPropertyForm()
    file_folder = app.config['UPLOAD_FOLDER']

    if form.validate_on_submit():
        # save photo
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(file_folder, filename))

        # create property
        property_data = form.data
        property_data['photo'] = filename
        property_data.pop('csrf_token', None)
        property = Property(**property_data)

        # save property to database
        db.session.add(property)
        db.session.commit()

        flash('Property Successfully Added', 'success')
        return redirect(url_for('properties'))

    return render_template('new_property.html', form=form)


@app.route('/properties/<int:property_id>', methods=['GET', 'POST'])
def view_property(property_id):
    property = Property.query.get(property_id)
    print(str(property))
    return render_template('property.html', property=property)

@app.route('/properties/create/<filename>')
def get_photo(filename):
    upload_folder_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
    return send_from_directory(upload_folder_path, filename)

def get_photo_names():
    file_names = []
    upload_folder_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])

    for root, dirs, files in os.walk(upload_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_names.append(os.path.basename(file_path))

    return file_names

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
