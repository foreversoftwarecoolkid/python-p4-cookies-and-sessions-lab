#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Placeholder for listing articles
    pass

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Initialize session['page_views'] if it doesn't exist
    session['page_views'] = session.get('page_views', 0)
    
    # Increment the page view count
    session['page_views'] += 1
    
    # Check if the user has reached the maximum page view limit
    if session['page_views'] > 3:
        # If the limit is reached, return an error message and a 401 status code
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
    # If the limit is not reached, retrieve and return the article data
    article = Article.query.get(id)
    if article is None:
        abort(404, description="Article not found")
    
    # Convert the article object to a dictionary for JSON serialization
    article_data = {
        "id": article.id,
        "title": article.title,
        "content": article.content
    }
    
    return jsonify(article_data)

if __name__ == '__main__':
    app.run(port=5555)
