from flask import Flask, render_template, request, redirect
import datetime

app = Flask(__name__)

articles = []

@app.route("/")
def home():
    return render_template("home.html", articles=articles)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/sections")
def sections():
    return render_template("sections.html")

@app.route("/new-article", methods=['GET', 'POST'])
def new_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        date = datetime.datetime.now().strftime("%B %d, %Y")
        
        article = {
            'title': title,
            'content': content,
            'author': author,
            'date': date
        }
        articles.append(article)
        
        return redirect('/')
    
    return render_template("new_article.html")

@app.route("/delete/<int:index>")
def delete(index):
    if index < len(articles):
        articles.pop(index)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5002)
    