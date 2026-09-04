
from flask import Flask
import mysql.connector
from config import DB_CONFIG


app = Flask(__name__)


def conectar():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def index():
    return """
    <h1>Sistema Biblioteca Escolar</h1>
    <p>Projeto iniciado com Python, Flask e MySQL.</p>
    <a href="/livros">Ver livros cadastrados</a>
    """


@app.route("/livros")
def listar_livros():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("SELECT * FROM livro")
        livros = cursor.fetchall()


        cursor.close()
        conexao.close()


        html = """
        <h1>Livros Cadastrados</h1>
        <a href="/">Voltar</a>
        <br><br>


        <table border="1" cellpadding="8">
            <tr>
                <th>Titulo</th>
                <th>Autor</th>
                <th>Categoria</th>
                <th>ID</th>
                <th>status</th>
            </tr>
        """


        for livro in livros:
            html += f"""
            <tr>
                <td>{livro['nome']}</td>
                <td>{livro['serie']}</td>
                <td>{livro['turma']}</td>
                <td>{livro['telefone']}</td>
            </tr>
            """


        html += "</table>"


        return html


    except Exception as erro:
        return f"Erro ao listar livros: {erro}"


if __name__ == "__main__":
    app.run(debug=True)
