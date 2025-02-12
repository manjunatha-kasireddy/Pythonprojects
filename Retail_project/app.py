from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Database Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Home Page - List Products
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Add Product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])

        new_product = Product(name=name, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')

# Update Product
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = int(request.form['quantity'])
        product.price = float(request.form['price'])

        db.session.commit()
        flash('Product updated successfully!', 'info')
        return redirect(url_for('index'))

    return render_template('update_product.html', product=product)

# Delete Product
@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!', 'danger')
    return redirect(url_for('index'))

# Run the App
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates database tables if they don't exist
    app.run(debug=True)
