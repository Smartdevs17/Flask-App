from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testpassword@localhost:5432/smartdeveloper'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class BlogPost(db.Model):
    # __tablename__ = "blogs"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(50), nullable=False, default="Smart Developer")
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost id={self.id} title={self.title} >'



@app.route("/")
def index():
    return "Hello World"

@app.route("/home/<string:name>")
def home(name):
    return "Hello World " + name

@app.route("/blog/posts")
def blog():
    # data = [{
    #     "id":1,
    #     "title": "Post I",
    #     "author": "Testone author",
    # },
    # {
    #     "id":2,
    #     "title": "Post II",
    #     "author": "Testtwo author",
    # },
    # {
    #     "id":3,
    #     "title": "Post III",
    #     "author": "Testthree author",
    # }]
    all_post = BlogPost.query.order_by(BlogPost.date_created).all()
    # print(all_post)
    return render_template("posts.html", posts=all_post)

@app.route("/posts/create_post",methods = ['GET'])
def new_post():
    return render_template("/create_post.html") 

@app.route("/posts/create_post",methods=["POST"])
def create_post():
    # print(request.form)
    try:
        title = request.form["title"]
        author = request.form["author"]
        content = request.form["content"]
        new_post = BlogPost(title=title,author=author,content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blog"))
    except:
        db.session.rollback()
        print(sys.exc_info())
    return "Thanks for submitting new blog post"

@app.route("/posts/delete/<int:id>")
def delete_post(id):
    try:
        post = BlogPost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
    except:
        print(sys.exc_info())
    return redirect("/blog/posts")


@app.route("/posts/edit/<int:id>", methods=["GET","POST"])
def edit_post(id):
    try:
        post = BlogPost.query.get_or_404(id)
        if request.method == "GET":
            return render_template("edit_post.html",post=post)
        elif request.method == "POST":
            title = request.form["title"]
            author = request.form["author"]
            content = request.form["content"]
            post.title = title
            post.author = author
            post.content = content
            db.session.commit()
            return redirect("/blog/posts")
    except:
        db.session.rollback()
        print(sys.exec_info())
    return redirect("/blog/posts")
        

if __name__ == "__main__":
    app.run(debug=True)