from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return "Users %r" %self.id


@app.route('/')
def index():
    return render_template('welcome.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        text = request.form['text']
        users = Users(name=name, email=email, text=text)

        try:
            db.session.add(users)
            db.session.commit()
            return redirect('/comments')
        except:
            return "Error! Try again later!"

    else:
        return render_template('comments.html')


@app.route('/comments_for_reading')
def comments_for_reading():
    users = Users.query.all()
    return render_template('comments_for_reading.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)
