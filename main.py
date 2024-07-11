from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


# it used pip install flask-sqlalchemy
# and pip install flask-mail
# we use this because it allows us to interact with the db with more high level code
# you can use dbbrowser to see the database
# flash allows the jinja(?) code to be used, which flashes the success message
# Sends he email from drewgardenapps@gmail.com

app = Flask(__name__)
app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  #
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "drewgardenapps@gmail.com"
app.config["MAIL_PASSWORD"] = "wcqo avxp jkvw axab"
db = SQLAlchemy(app)
mail = Mail(app)

# setting up the database model (we named it form)
# db is an instance of the sqlalchemy class (above)
# our class Form inherrits from the Model class
# the database table comes from the class name
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))        #sqlite doesn't have a specific type for emails
    date = db.Column(db.Date)
    titles = db.Column(db.String(80))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        titles = request.form["titles"]

        # print(f"{first_name}, {last_name}, {email}, {date}, {titles}")
        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date_obj,
                    titles=titles)
        db.session.add(form)
        db.session.commit()

        message_body = f"Thank you for your submission, {first_name}."\
                        f"Here is you data\n{first_name}\n{last_name}\nYour Doofus title will awarded on the {date}\n"\
                        f"TAbsolutely brilliant, you'll make a prized Doofus"

        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        mail.send(message)

        flash("Your form was submitted successfully!", "success")


    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()     #this method checks if ones exists with the name and uri specified above
        app.run(debug=True, port=5001)


