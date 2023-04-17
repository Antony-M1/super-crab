import re
import bson
from flask import (
    Flask, render_template, request, jsonify, send_from_directory,
    redirect, url_for, send_file
)
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


# mongo_uri = f"mongodb+srv://{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASSWORD')}@cluster0.s8odi72.mongodb.net/?retryWrites=true&w=majority"
mongo_uri = f"mongodb://{os.environ.get('MONGODB_USERNAME_LOCAL')}:{os.environ.get('MONGODB_PASSWORD_LOCAL')}@localhost:27017/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

db = client['crab']  # database name
sites = db['sites']  # collection name


app = Flask(__name__, static_url_path='/static')


@app.route('/static/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)


@app.route('/')
def home():
    _sites = sites.find()
    data = []
    for site in _sites:
        data.append(site)
    return render_template('site2.html', site_data=data)


def get_name_from_url(url: str) -> str:
    # use regex to extract the host name
    match = re.search(r"(?P<protocol>https?://)?(?P<host>[^/]+)", url)

    # get the host name from the match object
    host = match.group("host")

    return host


def get_allowed_domains_and_start_urls() -> list[str]:
    _sites = sites.find()
    allowed_domains = []
    start_urls = []
    data = []
    for site in _sites:
        allowed_domains.append(site.get('name'))
        start_urls.append(site.get('url'))
        data.append(site)
    return allowed_domains, start_urls, data


@app.route('/site', methods=['GET', 'POST', 'DELETE'])
def site():
    if request.method == 'POST':

        data = {
            'name': get_name_from_url(request.form.get('url')),
            'url': request.form.get('url'),
            'is_login_required': bool(request.form.get('is_login_required', False)),
            'credentials': {
                'username': request.form.get('username', None),
                'password': request.form.get('password', None),
            }
        }

        sites.insert_one(data)
        data['_id'] = str(data['_id'])

        return redirect(url_for('home'))  # put the funtion name

    if request.method == 'DELETE':
        c = 1
    return redirect(url_for('home'))


@app.route('/favicon.ico')
def favicon():
    return send_file('static/images/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/oops')
def oops():
    return render_template('something_wrong.html')


@app.route('/delete-site', methods=['POST'])
def delete_site():
    id = bson.ObjectId(request.form.get('site_id'))
    result = sites.delete_one({'_id': id})
    if not result.deleted_count:
        return redirect(url_for('oops'))
    return redirect(url_for('home'))


@app.route('/check-url', methods=['GET'])
def check_url():
    url = request.args.get('url')
    name = get_name_from_url(url)
    result = sites.find_one({'name': name})
    if result is not None:
        return jsonify({'status': 'error', 'message': 'URL already exists'})
    else:
        return jsonify({'status': 'success', 'message': 'URL is available'})


@app.route('/view/<name>')
def view_site_data(name: str):
    return render_template('progress.html')


if __name__ == '__main__':
    app.run(debug=True)
