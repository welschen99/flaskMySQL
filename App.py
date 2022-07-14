from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# CONNECTION SQL
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "gasf4273"
app.config["MYSQL_DB"] = "contactdb"
mysql = MySQL(app)

# SETTINGS
app.secret_key = 'mysecretkey'  # para inicializar una sesion, datos que guarda para despues usarlo, en este caso lo guardamos en la app esos datos, protegida por el secret_key


@app.route('/')
def index():
    db = mysql.connection.cursor()
    db.execute('SELECT * FROM contacts')
    data = db.fetchall()  # para obtener todos los datos
    print(data)
    return render_template('index.html', contacts=data)  # le paso los datos al index


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        db = mysql.connection.cursor()  # obtuseness la connexion
        db.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',
                   (fullname, phone, email))  # prescribes la consult SQL
        mysql.connection.commit()  # ejectors la consult
        flash('Contact Addred succesfully')
        return redirect(url_for('index'))  # para redirection con la url de index


@app.route('/delete/<string:id>')
def delete_contact(id):
    db = mysql.connection.cursor()
    db.execute('DELETE FROM contacts WHERE id = %s',
               [str(id)])  # borra de la tabla de contacts el id formateado como un string
    mysql.connection.commit()
    flash('Contact Removed Succesfully')  # message
    return redirect(url_for('index'))


@app.route('/edit/<id>')
def edit_contact(id):
    db = mysql.connection.cursor()
    db.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = db.fetchall()
    return render_template('edit.html', contact=data[0])  # para que me retorne solo el id y no todos los datos


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        db = mysql.connection.cursor()
        db.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        flash('Contact Updated Successfully')  # message
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
