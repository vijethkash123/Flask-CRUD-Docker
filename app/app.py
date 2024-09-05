from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword123@postgres:5432/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    __table_args__ = {"schema": "flask_app"}
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))


# db.create_all()


@app.get("/")
def home():
    users = db.session.query(Users).order_by(Users.user_id.asc()).all()
    for user in users:
        print(user.user_name)
    # return "Hello world!"
    return render_template("base.html", users_list=users)


# # @app.route("/add", methods=["POST"])
@app.post("/add")
def add():
    user_name = request.form.get("user_name")
    query = 'select user_id from flask_app.Users order by user_id desc limit 1;'
    result = db.session.execute(text(query))
    last_user_id = result.scalar()  # Extract the scalar value (user_id) from the result
    new_user_id = (last_user_id or 0) + 1  # increment and assign to highest user_id
    age = request.form.get("age")
    gender = request.form.get("gender")
    new_user = Users(user_name=user_name, user_id=new_user_id, age=age, gender=gender)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/update/<int:user_id>")
def update(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    new_gen = "M" 
    if user.gender == "F":
        new_gen = "M" 
    elif user.gender == "M":
        new_gen = "F"
    user.gender = new_gen
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/delete/<int:user_id>")
def delete(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    # print(user)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True, port=8082)
