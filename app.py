from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Ldqlbsn0@database-1.cv2g6i20c963.us-east-2.rds.amazonaws.com/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize database
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=True, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user/<string:username>/<string:email>')
def add_user(username, email):
    if not username or not email:
        flash('Both username and email are required!', 'error')
        return redirect(url_for('index'))

    new_user = User(username=username, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash(f'User {username} added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding user: {str(e)}', 'error')

    return redirect(url_for('index'))

@app.route('/add_product/<string:product_name>/<float:price>')
def add_product(product_name, price):
    if not product_name or not price:
        return redirect(url_for('index'))
    
    new_product = Product(product_name=product_name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('index'))

# READ
@app.route('/read_user/<int:user_id>')
def read_user(user_id):
    user = User.query.get_or_404(user_id)
    return f"User Details: ID: {user.id}, Username: {user.username}, Email: {user.email}"

# UPDATE
@app.route('/update_user/<int:user_id>/<string:username>/<string:email>')
def update_user(user_id, username, email):
    user = User.query.get_or_404(user_id)
    if not username or not email:
        flash('Both username and email are required!', 'error')
        return redirect(url_for('index'))

    user.username = username
    user.email = email

    try:
        db.session.commit()
        flash(f'User {username} updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user: {str(e)}', 'error')
    return redirect(url_for('index'))

# DELETE
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)