from flask import Flask, request, render_template
from flask_pymongo import PyMongo
import dateutil.parser as dparser
from datetime import datetime
from ..constants import mongoURI

app = Flask(__name__)
app.config["MONGO_URI"] = mongoURI  # Enter valid mongodbURI
mongo = PyMongo(app)
db = mongo['db']
collection = db['articles']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        if len(date1) > 0:
            date1 = dparser.parse(date1, fuzzy=True)
            date1 = date1.date()
        if len(date2) > 0:
            date2 = dparser.parse(date2, fuzzy=True)
            date2 = date2.date()

        if isinstance(date1, str) and isinstance(date2, str):
            return "Select valid Date"
        elif isinstance(date1, datetime) and (date2, datetime):
            if date1 > date2:
                return "First date cannot be greater than second"
            filter = {'story_date': {'$gte': date1, '$lte': date2}}
            count = 0
            count = collection.count_documents(filter)
            result = 'Number of documents fetched between ' + \
                str(date1) + ' and ' + str(date2) + ' are ' + str(count)
            return result
        else:
            if isinstance(date1, datetime):
                date = date1
            else:
                date = date2
            filter = {'story_date': date}
            count = 0
            count = collection.count_documents(filter)
            result = 'Number of documents fetched on ' + \
                str(date) + ' are ' + str(count)
            return result
    return render_template('index.html')
