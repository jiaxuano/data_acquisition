# Launch with
#
# python app.py

from flask import Flask, render_template
import sys
import pickle

app = Flask(__name__)

@app.route("/")
def articles():
    """Show a list of article titles"""
    # info = [[i[2], i[1]] for i in articles]
    info = [[i[2], '/article'+'/'+'/'.join([i[1].split('/')[-2],i[1].split('/')[-1]]) ] for i in articles]
    return render_template("articles.html", articles = info)


@app.route("/article/<topic>/<filename>")
def article(topic, filename):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    ## given topic and filename
    ## get title
    ## get list of paragraphs
    ## get list of recommended articles
    key = (topic, filename)
    recommend_list = recommended[key]
    for i in articles:
        if i[0] == topic and i[1].split('/')[-1] == filename:
            text = i[3]
            paragraphs_list = text.split('\n\n')
            title_str = i[2]
    title_link = []
    for j in recommend_list:
        for k in articles:
            if j[0] == k[0] and j[1] == k[1].split('/')[-1]:
                title_link.append([j[2],'/article'+'/'+'/'.join([k[1].split('/')[-2],k[1].split('/')[-1]])])
    return render_template("article.html", title = title_str, paragraphs = paragraphs_list, recom = title_link)


f = open('articles.pkl', 'rb')
articles = pickle.load(f)
f.close()

f = open('recommended.pkl', 'rb')
recommended = pickle.load(f)
f.close()

# you may need more code here or not


# for local debug
if __name__ == '__main__':
    app.run(debug=True)

