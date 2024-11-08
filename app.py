from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'port': 3307,
    'database': 'jornada',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# Função para se conectar ao banco de dados
def get_db_connection():
    connection = pymysql.connect(**db_config)
    return connection


# Rota para exibir a lista de registros com paginação
@app.route('/records')
def records():
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de registros por página
    offset = (page - 1) * per_page

    # Conectar ao banco de dados e buscar os registros com base na página e no limite
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Consultar o total de registros
        cursor.execute("SELECT COUNT(*) AS total FROM obf")
        total_records = cursor.fetchone()['total']

        # Consultar registros específicos para a página atual
        cursor.execute("SELECT * FROM obf LIMIT %s OFFSET %s", (per_page, offset))
        records = cursor.fetchall()

    connection.close()

    # Calcular o total de páginas
    total_pages = (total_records + per_page - 1) // per_page

    return render_template('records.html', records=records, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)
