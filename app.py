import re
from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


mongo_uri = f"mongodb+srv://{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASSWORD')}@cluster0.s8odi72.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)

db = client['crab']  # database name
sites = db['sites']  # collection name


app = Flask(__name__)


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


@app.route('/site', methods=['GET', 'POST'])
def site():
    if request.method == 'POST':

        data = {
            'name': get_name_from_url(request.form.get('url')),
            'url': request.form.get('url'),
            'is_login_required': request.form.get('is_login_required', False),
            'credentials': {
                'username': request.form.get('username', None),
                'password': request.form.get('password', None),
            }
        }

        sites.insert_one(data)
        data['_id'] = str(data['_id'])

        return jsonify(data)
    return render_template('site.html')


if __name__ == '__main__':
    app.run(debug=True)
