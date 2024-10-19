from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import mongo

car = Blueprint('car', __name__)

@car.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        price = request.form.get('price')
        mongo.db.cars.insert_one({
            'make': make,
            'model': model,
            'year': year,
            'price': price
        })
        flash('Car added successfully!')
        return redirect(url_for('car.add_car'))

    return render_template('car/add_car.html')
