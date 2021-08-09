from flask import Flask, request, jsonify
import pyodbc
# init
app = Flask(__name__)
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:pyt21-sqlserver.database.windows.net,1433;Database=sqldb;Uid=sqlAdmin;Pwd=Asd123!4;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
#conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:pyt22-sqlserver.database.windows.net,1433;Database=sqldb;Uid=sqlAdmin;Pwd=Ahmadbarho1993;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')

cursor = conn.cursor()
# routes
@app.route('/api/products', methods=['GET'])
def get_all():
    products = []

    for row in cursor.execute('SELECT Products.Id,Products.Name,Products.Description,Categories.Name as Category FROM Products JOIN Categories ON Products.CategoryId = Categories.Id'):
       
        products.append( { 'id': row.Id, 'name': row.Name, 'description': row.Description, 'category': row.Category })
    return jsonify(products)
    
@app.route('/api/products', methods=['POST'])
def post():
    name = request.json['name']
    description = request.json['description']
    category_id = request.json['categoryId']
    cursor.execute('INSERT INTO Products (Name,Description,CategoryId) VALUES(?,?,?)', [name, description, category_id])
    result = cursor.execute('SELECT Products.Id,Products.Name,Products.Description,Categories.Name as Category FROM Products JOIN Categories ON Products.CategoryId = Categories.Id WHERE Products.Id = @@IDENTITY').fetchone()
    cursor.commit()
    product = {
        'id': result.Id,
        'name': result.Name,
        'description': result.Description,
        'category': result.Category
    }
    return jsonify(product)
@app.route('/api/products/<id>', methods=['GET'])
def get_one(id):
    result = cursor.execute('SELECT Products.Id,Products.Name,Products.Description,Categories.Name as Category FROM Products JOIN Categories ON Products.CategoryId = Categories.Id WHERE Products.Id = ?', [id]).fetchone()
     
    product = {
        'id': result.Id,
        'name': result.Name,
        'description': result.Description,
        'category': result.Category
    }
    return jsonify(product)
    
#run server
if __name__ == '__main__':
    app.run()
