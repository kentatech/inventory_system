from flask import Flask,request,render_template,redirect,url_for
from configs.base_config import Development

import psycopg2
conn = psycopg2.connect("dbname=kiosk user=postgres password=1234")
cur = conn.cursor()

app=Flask(__name__)
# @app.route ('/')
# def home():
#     return"tuko ndani ya inventory management system"
@app.route('/')
def home():
    username = "kenta"
    return render_template('index.html',usr=username)

# @app.route ('/index')
# def index():
#     return"tuko ndani ya inventory management system"
@app.route('/dashboard')
def dashboard():
    cur.execute("SELECT COUNT(*) FROM products;")
    invs=cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM sales;")
    sls=cur.fetchone()
    cur.execute("SELECT category,COUNT(*) from products GROUP BY category;")
    pie=cur.fetchall()
    cur.execute("SELECT name, sum(quantity_sold) FROM sales INNER JOIN products on products.id = sales.product_id GROUP BY name;")
    bar=cur.fetchall()
    print(pie)
    print(bar)

    pie_labels=[]
    pie_values=[]

    for x in pie:
        pie_labels.append(x[0])
        pie_values.append(x[1])
    print(pie_labels)

    bar_labels=[]
    bar_values=[]
    
    for y in bar:
        bar_labels.append(x[0])
        bar_values.append(x[1])
    print(pie_labels)
    
    return render_template('dashboard.html',invs=invs,sls=sls,pie_labels=pie_labels,pie_values=pie_values,bar_labels=bar_labels,bar_values=bar_values)

@app.route('/inventories', methods=['POST','GET'])
def inventories():
    if request.method=="GET":
        cur.execute("SELECT * FROM products;")
        x=cur.fetchall()
        print (x)
        return render_template('inventories.html',x=x)
    else:
        n=request.form['name']
        b=request.form['buying_price']
        s=request.form['selling_price']
        q=request.form['quantity']
        c=request.form['category']
        # # to link buying price/name 
        print (n,q,b,s,c)
        cur.execute("INSERT INTO products (name,buying_price,selling_price,stock_quantity,category)VALUES(%s,%s,%s,%s,%s)",(n,b,s,q,c))
        conn.commit()
        return redirect(url_for('inventories'))

@app.route('/edit_sales',methods=['GET','POST'])
def edit_sales():
    if request.method=="POST":
        pid=request.form['product_id']
        n=request.form['name']
        b=request.form['buying_price']
        s=request.form['selling_price']
        q=request.form['quantity']
        c=request.form['category']
    
        print(pid,n,b,s,q)
        
        cur.execute("UPDATE products SET name=%s, buying_price=%s, selling_price=%s, stock_quantity=%s, category=%s WHERE products.id =%s;",(n,b,s,q,c,pid))
        conn.commit()
        return redirect(url_for('inventories'))
    else:
        return render_template('inventories.html')

@app.route('/sales',methods=['GET','POST'])
def sales():
    if  request.method=="GET":
        cur.execute("SELECT * FROM sales;")
        all_sales=cur.fetchall()
        print (all_sales)
        return render_template('sales.html',all_sales=all_sales)
    else:
        pid=request.form['product_id']
        q=request.form['quantity_sold']
        # # to link buying price/name 
        
        cur.execute("UPDATE products SET stock_quantity=%s WHERE id=%s",(q,pid))
        cur.execute("INSERT INTO sales (product_id,quantity_sold,date_sold) VALUES(%s,%s,'2020-05-03')",(pid,q))
        conn.commit()
        return redirect(url_for('sales'))
@app.route('/makesales',methods=['GET','POST'])
def make_sales():
    if  request.method=="GET":
        
        return redirect('sales.html')
    else:
        pid=request.form['product_id']
        q=request.form['quantity_sold']
        # # to link buying price/name 
        print (pid,q)
        cur.execute("UPDATE products SET stock_quantity=%s WHERE id=%s",(q,pid))
        cur.execute("INSERT INTO sales (product_id,quantity_sold,) VALUES(%s,%s)",(pid,q))
        conn.commit()
        return redirect(url_for('sales'))
# //dynamic routing
@app.route('/inventories/<int:inventory_id>')
def single_inventories(inventory_id):
    return f"inventory_id is{iventory_id}"

# //or   return"inventories with ID page" +str(inventory_id)
# //dynamic  2
@app.route('/users')
def users():
    return render_template('users.html')

@app.route('/stock')
def stock():
    return render_template('stock.html')