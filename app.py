from openpyxl import load_workbook, Workbook
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# Read the Excel file

id1 = 53
id2 = 52
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user@localhost:5432/carcmp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




class datas(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer,primary_key = True)
    brand = db.Column(db.String)
    model = db.Column(db.String)
    year = db.Column(db.String)
    price = db.Column(db.String)
    colours = db.Column(db.String)
    fuel = db.Column(db.String)
    mileage = db.Column(db.String)
    boot_space = db.Column(db.String)
    seat_capacity = db.Column(db.String)
    tyre_size = db.Column(db.String)
    air_bags = db.Column(db.String)
    cruise_ctrl = db.Column(db.String)
    engine = db.Column(db.String)
    cylinders = db.Column(db.String)
    transmission = db.Column(db.String)
    gear_box = db.Column(db.String)
    drive_type = db.Column(db.String)
    description = db.Column(db.String)

        


    
def create_excel_file_if_not_exists():
    try:
        wb = load_workbook('form_responses.xlsx')
    except FileNotFoundError:
        wb = Workbook()
        ws = wb.active
        ws.append(['First Name', 'Last Name', 'Email', 'Message'])
        wb.save('form_responses.xlsx')

class kart(db.Model):
    __tablename__ = 'Kart'
    brand = db.Column(db.String)
    carsid = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)    
    model =db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.String)

class cars(db.Model):
    __tablename__ = 'carcmp'
    id = db.Column(db.Integer ,primary_key = True)

create_excel_file_if_not_exists()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/importing')
def excel_file_import():
    excel_file = 'Book.xlsx'
    df = pd.read_excel(excel_file)
    for index, row in df.iterrows():
        mileage = str(row['milege']).split()[0]
        price = str(row['price']).replace(' ','')
        boot_spac=str(row['bootspace']).split()[0]
        seat_capacity = str(row['seat_capacity']).split()[0]
        # Create a new datas object
        data = datas(
            brand=row['brand'],
            model=row['model'],
            year=row['year'],
            price=price,
            colours=row['colours'],
            fuel=row['fuel'],
            mileage=mileage,
            boot_space=boot_spac,
            seat_capacity=seat_capacity,
            tyre_size=row['tyre_size'],
            air_bags=str(row['air_bags']),
            cruise_ctrl=str(row['cruise_ctrl']),
            engine=str(row['engine']).split()[0],
            cylinders=str(row['cylinders']).split()[0],
            transmission=str(row['transmission']).split()[0],
            gear_box=str(row['gear_box']).split()[0],
            drive_type=str(row['drive_type ']).split()[0],
            description=row['description']
        )
        
        db.session.add(data)
    db.session.commit()
    return "Commit completed"


@app.route('/contact')
def contactpage():
    return render_template('contactus.html')

@app.route('/preview/<id>')
def preview(id):
    row = datas.query.get(id)
    return render_template('preview.html',row=row)

@app.route('/addtocart/<id>')
def addcart(id):
    row = datas.query.get(id)
    data = kart( carsid = id,model = row.model ,brand = row.brand, description = row.description,price = row.price)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/addcompare/<id>')
def addcompare(id):
    global id2,id1
    id2= id1
    id1 = id
    print(id1,id2)
    return redirect(url_for('compare'))

@app.route('/compare')
def compare():
    global id2,id1
    row1 = datas.query.get(id1)
    row2 = datas.query.get(id2)
    return render_template('comparison.html',row1 = row1 ,row2 = row2)

@app.route('/contactus', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        message = request.form.get('message')
        wb = load_workbook('form_responses.xlsx')
        ws = wb.active
        ws.append([fname, lname, email, message])
        wb.save('form_responses.xlsx')

        return "Form responses saved successfully!"

    return "Method Not Allowed"


@app.route('/audicars')
def audi():
    row = datas.query.filter(datas.brand == 'audi').all()
    return render_template('allcarpreview.html',rows= row,fun = 'all')


@app.route('/volvocars')
def volvo():
    row = datas.query.filter(datas.brand == 'volvo').all()
    return render_template('allcarpreview.html',rows= row,fun = 'all')


@app.route('/cartview')
def cart():
    row = kart.query.all()
    return render_template('allcarpreview.html',rows= row,func = 'cart')

@app.route('/allcars')
def all():
    row = datas.query.all()
    return render_template('allcarpreview.html',rows= row,fun = 'all')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False) 

