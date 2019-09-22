from jinja2 import Template
from flask import Flask
import numpy as np
import io
import random
from flask import Response, render_template, request
import matplotlib
import sqlalchemy
from sqlalchemy import Table, Column, Float, Integer, String, MetaData, ForeignKey, DateTime, CHAR, Time, Boolean, Float, VARCHAR
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


matplotlib.use('Agg')
db = SQLAlchemy()


class blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    author = db.Column(db.VARCHAR())
    header = db.Column(db.VARCHAR()) 
    post = db.Column(db.VARCHAR())
    date = db.Column(db.DateTime())


    def __repr__(self):
        return "<blog(id='%s',post='%s')>" % (self.id, self.post)


    def GetPost(id_):
        #return blog.query.filter(id = id).first()
        return blog.query.filter(blog.id == id_).first()


    def GetAll():
        #return blog.query.filter(id = id).first()
        return blog.query.all()


class Data():
    def __init__(self):
        self.d = 0

    def GetData(self):
        return np.arange(0, 10)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'Database URI'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


try:
    with app.app_context():
        db.create_all()
except Exception as e:
    print(e)


@app.route('/plot')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot_')
def plot_png2():
    fig = create_figure()
    fig.savefig('/matplotlibdemo.png')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return render_template('image.html')


@app.route('/')
def blog_():
    post = blog.query.all()
    return render_template('index.html', post = post, _post_length_ = len(post))


@app.route('/about')
def About():
    return render_template('about.html')


@app.route('/contact')
def Contact():
    return render_template('contact.html')


@app.route('/resume')
def root():
    return app.send_static_file('Resume.pdf')


@app.route('/post')
def Post():
    _post_ = request.args.get('Post_id')
    post = blog.GetPost(_post_)
    return render_template('post.html', post = str(post.post), header = post.header)


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x = Data()
    y = Data()
    f = plt.figure(figsize=(5, 5))
    axis.scatter(x.GetData(), y.GetData())
    return fig


if __name__ == "__main__":
    app.run()


