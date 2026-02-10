from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
import pymysql
from config import config

app = Flask(__name__)
app.config.from_object(config["development"])

# Initialize Flask-Session for server-side sessions
sess = Session()
sess.init_app(app)


def get_db_connection():
    """Create and return a database connection"""
    connection = pymysql.connect(
        host=app.config["DB_HOST"],
        port=app.config["DB_PORT"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        db=app.config["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    return connection


def init_db():
    """Initialize database tables"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        create_users_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_users_table_sql)
        
        # Create customers table
        create_customers_table_sql = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            phone VARCHAR(50),
            company VARCHAR(255),
            address TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """
        cursor.execute(create_customers_table_sql)
        
        # Create courses table
        create_courses_table_sql = """
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            instructor VARCHAR(255),
            duration VARCHAR(100),
            level VARCHAR(50),
            price DECIMAL(10, 2),
            start_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_courses_table_sql)
        
        print("✓ Database initialized successfully")
    except pymysql.Error as e:
        print(f"❌ Database initialization error: {e}")
    finally:
        connection.close()


def get_user_by_email(email):
    """Fetch a user from the database by email"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()
    except pymysql.Error:
        return None
    finally:
        connection.close()


@app.route("/")
def root():
    user = None
    if session.get("user"):
        user = get_user_by_email(session["user"])
    return render_template("home.html", user=user)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and user["password"] == password:
            session["user"] = email
            return redirect(url_for("index"))
        else:
            msg = "Invalid email or password!"
            return render_template("login.html", msg=msg)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return render_template("login.html", msg=msg)
    finally:
        connection.close()


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["GET", "POST"])
def register_post():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            msg = "Passwords do not match!"
            return render_template("register.html", msg=msg)

        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                msg = "Email already registered!"
                return render_template("register.html", msg=msg)

            # Insert new user into database
            cursor.execute(
                "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)",
                (email, name, password),
            )
            session["user"] = email
            return redirect(url_for("root"))

        except pymysql.Error as e:
            msg = f"Database error: {e}"
            return render_template("register.html", msg=msg)
        finally:
            connection.close()

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("root"))


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/account")
def account():
    if not session.get("user"):
        return redirect(url_for("login"))
    user = get_user_by_email(session["user"])
    return render_template("account.html", user=user)


@app.route("/account", methods=["POST"])
def account_post():
    if not session.get("user"):
        return redirect(url_for("login"))

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    connection = get_db_connection()
    try:
        cursor = connection.cursor()

        # Check if new email is already taken by another user
        cursor.execute("SELECT * FROM users WHERE email = %s AND email != %s", (email, session["user"]))
        existing_user = cursor.fetchone()

        if existing_user:
            msg = "Email already in use by another account!"
            user = get_user_by_email(session["user"])
            return render_template("account.html", user=user, msg=msg)

        # Update user information
        cursor.execute(
            "UPDATE users SET name = %s, email = %s, password = %s WHERE email = %s",
            (name, email, password, session["user"])
        )

        # Update session if email changed
        if email != session["user"]:
            session["user"] = email

        return redirect(url_for("root"))

    except pymysql.Error as e:
        msg = f"Database error: {e}"
        user = get_user_by_email(session["user"])
        return render_template("account.html", user=user, msg=msg)
    finally:
        connection.close()


# Customer Management Routes

@app.route("/customers")
def customers():
    """Display all customers"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY created_at DESC")
        customers = cursor.fetchall()
        return render_template("customers/index.html", customers=customers)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return render_template("customers/index.html", customers=[], msg=msg)
    finally:
        connection.close()


@app.route("/customers/add", methods=["GET", "POST"])
def customers_add():
    """Add a new customer"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        company = request.form.get("company")
        address = request.form.get("address")
        notes = request.form.get("notes")
        
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO customers (name, email, phone, company, address, notes) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, email, phone, company, address, notes)
            )
            return redirect(url_for("customers"))
        except pymysql.Error as e:
            msg = f"Database error: {e}"
            return render_template("customers/add.html", msg=msg)
        finally:
            connection.close()
    
    return render_template("customers/add.html")


@app.route("/customers/<int:customer_id>")
def customers_view(customer_id):
    """View customer details"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            return redirect(url_for("customers"))
        
        return render_template("customers/view.html", customer=customer)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return redirect(url_for("customers"))
    finally:
        connection.close()


@app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
def customers_edit(customer_id):
    """Edit customer details"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            company = request.form.get("company")
            address = request.form.get("address")
            notes = request.form.get("notes")
            
            cursor.execute(
                "UPDATE customers SET name = %s, email = %s, phone = %s, company = %s, address = %s, notes = %s WHERE id = %s",
                (name, email, phone, company, address, notes, customer_id)
            )
            return redirect(url_for("customers"))
        
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            return redirect(url_for("customers"))
        
        return render_template("customers/edit.html", customer=customer)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return redirect(url_for("customers"))
    finally:
        connection.close()


@app.route("/customers/<int:customer_id>/delete")
def customers_delete(customer_id):
    """Delete a customer"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        return redirect(url_for("customers"))
    except pymysql.Error as e:
        return redirect(url_for("customers"))
    finally:
        connection.close()


# Course Management Routes

@app.route("/courses")
def courses():
    """Display all courses"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM courses ORDER BY created_at DESC")
        courses = cursor.fetchall()
        return render_template("courses/index.html", courses=courses)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return render_template("courses/index.html", courses=[], msg=msg)
    finally:
        connection.close()


@app.route("/courses/add", methods=["GET", "POST"])
def courses_add():
    """Add a new course"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        instructor = request.form.get("instructor")
        duration = request.form.get("duration")
        level = request.form.get("level")
        price = request.form.get("price")
        start_date = request.form.get("start_date")
        
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO courses (title, description, instructor, duration, level, price, start_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (title, description, instructor, duration, level, price, start_date)
            )
            return redirect(url_for("courses"))
        except pymysql.Error as e:
            msg = f"Database error: {e}"
            return render_template("courses/add.html", msg=msg)
        finally:
            connection.close()
    
    return render_template("courses/add.html")


@app.route("/courses/<int:course_id>")
def courses_view(course_id):
    """View course details"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        course = cursor.fetchone()
        
        if not course:
            return redirect(url_for("courses"))
        
        return render_template("courses/view.html", course=course)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return redirect(url_for("courses"))
    finally:
        connection.close()


@app.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
def courses_edit(course_id):
    """Edit course details"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            instructor = request.form.get("instructor")
            duration = request.form.get("duration")
            level = request.form.get("level")
            price = request.form.get("price")
            start_date = request.form.get("start_date")
            
            cursor.execute(
                "UPDATE courses SET title = %s, description = %s, instructor = %s, duration = %s, level = %s, price = %s, start_date = %s WHERE id = %s",
                (title, description, instructor, duration, level, price, start_date, course_id)
            )
            return redirect(url_for("courses"))
        
        cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        course = cursor.fetchone()
        
        if not course:
            return redirect(url_for("courses"))
        
        return render_template("courses/edit.html", course=course)
    except pymysql.Error as e:
        msg = f"Database error: {e}"
        return redirect(url_for("courses"))
    finally:
        connection.close()


@app.route("/courses/<int:course_id>/delete")
def courses_delete(course_id):
    """Delete a course"""
    if not session.get("user"):
        return redirect(url_for("login"))
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
        return redirect(url_for("courses"))
    except pymysql.Error as e:
        return redirect(url_for("courses"))
    finally:
        connection.close()


if __name__ == "__main__":
    init_db()  # Initialize database on startup
    app.run(debug=True, port=5001)

