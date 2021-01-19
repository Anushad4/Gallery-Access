from flask import Flask, render_template, request, redirect, url_for, send_from_directory, current_app
from flask_mail import *
import mysql.connector
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = './static'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anujesus@1994",
    database="Project"
)

name = ""
uid = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global name, uid
    if request.method == "POST":
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user")
        result = mycursor.fetchall()
        user = request.form['user_name']
        pwd = request.form['pwd']
        for x in result:
            if user == x[1]:
                if pwd == x[2]:
                    name = user
                    uid = x[0]
                    return redirect(url_for('dash'))
                else:
                    return(render_template("login.html", error="Password authentication failed"))
        return(render_template("login.html", error="User not found"))
    else:
        return(render_template("login.html"))

@app.route('/dashboard', methods=["GET", "POST"])
def dash():
    if request.method == "POST":
        if request.form["btn"] == "Upload Photo":
            img = request.files["img"]
            path = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            img.save(path)

            img_ = open(path, 'rb')
            img__ = img_.read()

            # Insert into database
            cur = mydb.cursor()
            query = "INSERT INTO images(iduser, image) VALUES (%s, %s)"
            result = cur.execute(query, (uid, img__))
            mydb.commit()

            return(render_template("dashboard.html", user=name, output=path, message="Image uploaded successfully!"))
        elif request.form["btn"] == "Open Gallery":
            # Get images
            cur = mydb.cursor()
            data = (uid,)
            query = "SELECT * FROM images WHERE iduser= %s "
            cur.execute(query, data)
            imgs = cur.fetchall()
            img_list = []
            for x in range(len(imgs)):
                filename = "tmp" + str(x) + ".jpg"
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                tmp = open(path, 'wb')
                tmp.write(imgs[x][2])
                img_list.append(path)
                tmp.close()
            
            return(render_template("gallery.html", imgs=img_list))
    else:
        return(render_template("dashboard.html", user=name))
if __name__ == '__main__':
   app.run(debug = True)
