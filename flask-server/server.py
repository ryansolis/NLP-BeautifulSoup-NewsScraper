from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Set up database connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="&aV83022RMS99"
)

@app.route('/articles')
def get_articles():
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles")
    rows = cur.fetchall()
    articles = []
    for row in rows:
        article = {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "pubdate": row[3],
            "content": row[4],
            "summary": row[5],
            "url": row[6],
            "source": row[7]
        }
        articles.append(article)
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
