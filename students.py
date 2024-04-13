from flask import Flask, render_template, request, flash, redirect, url_for
from form import LoginForm, StudentForm
from flask_mysqldb import MySQL
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(funcName)s : %(lineno)d : %(message)s',
    handlers=[
        logging.handlers.TimedRotatingFileHandler(
            filename=r"Runtime_log.log",
            when="D",
            interval=1,
            backupCount=0,
        )
    ]
)

# Create a SQL Instance
mysql = MySQL()

# Create a Flask Instance
app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = "this is my secret key"

# Configurations for the MySQL Connection
app.config['MYSQL_HOST'] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Priyathars@14"
app.config["MYSQL_DB"] = "Students_DB"

# Initialize MySQL
mysql.init_app(app)


# Login to the system
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        app.logger.info("Login Process Starting")
        form = LoginForm()
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' and request.form['password'] != 'admin':
                error = 'Invalid Credentials. Please try again.'
            else:
                return redirect(url_for('view_student'))
            app.logger.info("Login Process Done")
        return render_template("login.html", error=error, form=form)

    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        print(e, "An ERROR occurred in Login Method")


# Students Registration Page
@app.route('/registration', methods=['GET', 'POST'])
def register_student():
    form = StudentForm()
    form.validate()
    return render_template("registration.html", form=form)


# Function to Insert Student Records
@app.route('/add', methods=['POST'])
def add_student():
    try:
        app.logger.info('Student Insert Process Starting')
        if request.method == 'POST':
            student_name = request.form['student_name']
            dob = request.form['dob']
            email = request.form['email']
            mobile_no = request.form['mobile_no']
            gender = request.form['gender']
            course = request.form['course']

            con = mysql.connect
            cur = con.cursor()

            cur.callproc("create_student", (student_name, dob, email, mobile_no, gender, course))
            app.logger.info('Student Insert request received Successfully')

            con.commit()
            con.close()

            app.logger.info('Student Records Inserted Successfully')
            flash('Student registration done successfully')
            return redirect(url_for('view_student'))

        return render_template('students.html')

    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        print(e, "An ERROR occurred in Add Student Method")


# Function to get all the Students Records
@app.route('/students', methods=['GET', 'POST'])
def view_student():
    try:
        app.logger.info("Get All Student Records Process Starting")

        con = mysql.connect
        cur = con.cursor()

        cur.callproc("view_student")
        results = cur.fetchall()
        app.logger.info('Get All request received Successfully')

        return render_template('students.html', results=results)
        con.commit()
        con.close()

    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        print(e, "An ERROR occurred in View Student Method")


# Function to Update the Particular Student Records
@app.route('/update', methods=['POST', 'GET'])
def update():
    try:
        app.logger.info('Update Process Starting')
        if request.method == 'POST':
            id = request.form.get('id')
            s_name = request.form.get('student_name')
            email = request.form.get('email')
            m_no = request.form.get('mobile_no')
            course = request.form.get('course')

            con = mysql.connect
            cur = con.cursor()
            cur.callproc("update_student", (id, s_name, email, m_no, course))
            app.logger.info('Student Update Request Received Successfully')
            con.commit()

            flash('Student Record has updated successfully')
            app.logger.info('Update Process Successfully Done')
            con.close()

            return redirect(url_for('view_student'))
        return render_template('students.html')

    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        print(e, "An ERROR occurred in Update Student Method")


# Function to Delete the Particular Student Record
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        app.logger.info('Delete Method Starting')
        con = mysql.connect
        cur = con.cursor()
        cur.callproc("delete_student", (id,))
        con.commit()

        flash('Student Record has deleted successfully')
        app.logger.info('Student Delete Process Successfully Done')
        con.close()
        return redirect(url_for('view_student'))

    except Exception as e:
        app.logger.error('An error occurred: %s', str(e))
        print(e, "An ERROR occurred Delete Method")


if __name__ == '__main__':
    app.run(debug=True)
