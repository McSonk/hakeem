from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


#create the app
app = Flask(__name__)


# ############## DB STUFF #################
# Instance ORM
db = SQLAlchemy()

# ORM config
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_DB = 'postgres'
DB_PWD = '1234'
DB_USER = 'eromn_admin'

DB_URL = f'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_DB}'

# Letting sqlAlchemy know the database's connection URL
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

# Print the SQL queries from SQLAlchemy
app.config['SQLALCHEMY_ECHO'] = True

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# ------- Models ------------

# Basic page, basic model. So, just 1 table and 1 model
class Exam(db.Model):
    __tablename__ = 'exam'
    __table_args__ = {'schema': 'eromn' }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    n_of_questions = db.Column(db.Integer())



# ########### HTML STUFF ####################
# Configure the default view
# We're serving 2 HTTP methods with this python function
# GET = Get the data: query info from the DB
# POST = Add a data record to the database
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        # POST detected! Thus, we need to add a record
        name = request.form['name']
        number = request.form['number']
        exam = Exam()
        exam.name = name
        exam.n_of_questions = number

        db.session.add(exam)
        db.session.commit()
    # Queries all the rows on the table
    exams = db.session.execute(
        db.select(Exam)
    ).scalars()
    # Send the query's result to the template
    return render_template("assignment.html", rows=exams)

# Initialize everything
if __name__ == "__main__":
    # print the default URL connection
    print(f'Using DB connection: "{DB_URL}"')
    # debug=True for printing useful information and reloading when file changes
    app.run(debug=True)
