import base64
import os
from io import BytesIO
from email.mime import image
from tkinter import Image
import io
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import uuid

from sqlalchemy.dialects import mysql

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:sa123@localhost/crud_operations'

db = SQLAlchemy(app)


"""fname lname password gender email phone address files"""


class Form(db.Model):
    fname = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(10), nullable=False, primary_key = True)
    address = db.Column(db.String(30), nullable=False)
    modalname = db.Column(db.String(30), nullable=False)
    year = db.Column(db.String(30), nullable=False)
    fuel = db.Column(db.String(30), nullable=False)
    kilometer = db.Column(db.String(30), nullable=False)
    carnumber = db.Column(db.String(30), nullable=False)
    color = db.Column(db.String(30), nullable=False)
    filename = db.Column(db.String(30))
    data = db.Column(db.LargeBinary)
    path = db.Column(db.String(60))
    def __repr__(self):

        return f"<form ( name = '{self.fname},color = '{self.color}',filename = '{self.filename}',modalname = '{self.modalname}',kilometer = '{self.kilometer}',carnumber = '{self.carnumber}',email = '{self.email}',year = '{self.year}',phone = '{self.phone}',address = '{self.address}',fuel = '{self.fuel}', path = '{self.path}')>\n"


@app.route("/", methods=['POST'])
def index():
    if (request.method == 'POST'):
        '''ADD ENTRY TO DATABASE'''
        fname = request.form.get('fname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')

        modalname = request.form.get('modalname')
        year = request.form.get('year')
        fuel = request.form.get('fuel')
        kilometer = request.form.get('kilometer')
        carnumber = request.form.get('carnumber')
        color = request.form.get('color')
        key = uuid.uuid1()
        #eccomimage uploading method
        file = request.files['file']


        #data = base64.b64encode(data)
        file_new_name = f"{key}{file.filename}"
        path = "./static/images/"+str(key)+'.jpg'
        file.save(path)

        # os.rename(f"static/images/{file.filename}",f"static/images/{file_new_name}")
        # '''paths = Image(imgtype='jpeg')
        '''paths.path = 'static/images'''''
        # path = 'f"static/images/{file_new_name}"
        print(path)
        #new_image = Image(path='/static/images/file_new_name.jpg')
        #file = file_new_name
        data = file.read()
        entry = Form(fname=fname, email=email, phone=phone, address=address, modalname=modalname, year=year, fuel=fuel,
                     kilometer=kilometer, carnumber=carnumber, color=color,data = data, filename=file.filename, path = path)

        db.session.add(entry)
        db.session.commit()
        db.session.refresh(entry)
        data = Form.query.all()

        print(data)

    return render_template("index.html")


'''@app.route("/", methods=['GET'])
def show():
    data = Form.query.all()
    print(data)

    return render_template("index.html")'''
@app.route("/", methods=['GET'])
def show():
    if (request.method == "GET"):
        # data = Form.query.all()
        # print(data)
        # print("Show method check")
        return render_template("index.html")

@app.route("/getdata", methods=['GET'])
def getData():
    if (request.method == "GET"):
        print("Get data method check ")
        datas = Form.query.all()
        #image_rec = Form.query.get(Form.data)
        #image_rec = Form.query.with_entities(Form.data).all()
        # image_rec = Form.query.all()
        # data = BytesIO(row[11] for row in image_rec)
        # image_jpg = BytesIO()
        # image.save(image_jpg,format ='JPEG')
        # image_jpg.seek(0)
        #
        print(datas)
        '''image = Form[0][11]
        binary_data = base64.b64decode(image)
        image = Image.open(io.BytesIO(binary_data))'''
        return render_template("file.html" , datas = datas)

if __name__ == "__main__":
    app.run(port=5000 ,debug=True)
