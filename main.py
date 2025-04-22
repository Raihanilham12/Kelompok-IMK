from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#koneksi ke database
app.secret_key = 'hotelindonesia'
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='hotelindonesia'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

#tampil data
@app.route('/admin')
def customertampildata():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer ORDER BY id DESC")
    datatampil = cur.fetchall()
    cur.close()
    return render_template('admin.html', datapemesan = datatampil)

#insert into
@app.route('/', methods=['POST'])
def customerinsert():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jml = request.form['jml']
        ket = request.form.get('ket', '')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO customer (nama, email, phone, tipe, checkin, checkout, jml, ket) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nama, email, phone, tipe, checkin, checkout, jml, ket))
        mysql.connection.commit()
        flash("Data behasil di kirim")
        return redirect(url_for('home'))

#insert into
@app.route('/customerupdate', methods=['POST'])
def customerupdate():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        email = request.form['email']
        phone = request.form['phone']
        tipe = request.form['tipe']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        jml = request.form['jml']
        status = request.form['status']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE customer SET nama=%s, email=%s, phone=%s, tipe=%s, checkin=%s, checkout=%s, jml=%s, status=%s WHERE id=%s", (nama, email, phone, tipe, checkin, checkout, jml, status, id,))
        mysql.connection.commit()
        flash("Data behasil di update")
        return redirect(url_for('customertampildata'))

@app.route('/kamar')
def tipekamar():
    return render_template('kamar.html')

@app.route('/fasilitas')
def fasilitas():
    return render_template('fasilitas.html')

#delete data
@app.route('/customerhapus/<int:id>', methods=["GET"])
def customerhapus(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM customer WHERE id=%s", (id,))
    mysql.connection.commit()
    flash("Data behasil di hapus")
    return redirect(url_for('customertampildata'))

if __name__ == '__main__':
    app.run(debug=True)