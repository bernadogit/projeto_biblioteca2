from flask import Flask, render_template, request, redirect
import mysql.connector
from config import DB_CONFIG


app = Flask(__name__)


def conectar():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/alunos")
def listar_alunos():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("SELECT * FROM aluno")
        alunos = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template("alunos.html", alunos=alunos)


    except Exception as erro:
        return f"Erro ao listar alunos: {erro}"


@app.route("/alunos/novo")
def formulario_aluno():
    return render_template("aluno_form.html")


@app.route("/alunos/cadastrar", methods=["POST"])
def cadastrar_aluno():

    try:
        nome = request.form["nome"]
        serie = request.form["serie"]
        turma = request.form["turma"]
        telefone = request.form["telefone"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            INSERT INTO aluno (nome, serie, turma, telefone)
            VALUES (%s, %s, %s, %s)
        """


        valores = (nome, serie, turma, telefone)


        cursor.execute(sql, valores)
        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/alunos")


    except Exception as erro:
        return f"Erro ao cadastrar aluno: {erro}"

# Rotas para livros
@app.route("/livros")
def listar_livros():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("SELECT * FROM livro")
        livros = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template("livros.html", livros=livros)


    except Exception as erro:
        return f"Erro ao listar livros: {erro}"


@app.route("/livros/novo")
def formulario_livro():
    return render_template("livro_form.html")


@app.route("/livros/cadastrar", methods=["POST"])
def cadastrar_livro():
    try:
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        categoria = request.form["categoria"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            INSERT INTO livro (titulo, autor, categoria, status)
            VALUES (%s, %s, %s, %s)
        """


        valores = (titulo, autor, categoria, "Disponível")


        cursor.execute(sql, valores)
        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/livros")


    except Exception as erro:
        return f"Erro ao cadastrar livro: {erro}"

# Rotas para biliotecario
@app.route("/bibliotecarios")
def listar_bibliotecarios():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("SELECT * FROM bibliotecario")
        bibliotecarios = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template("bibliotecarios.html", bibliotecarios=bibliotecarios)


    except Exception as erro:
        return f"Erro ao listar bibliotecários: {erro}"




@app.route("/bibliotecarios/novo")
def formulario_bibliotecario():
    return render_template("bibliotecario_form.html")




@app.route("/bibliotecarios/cadastrar", methods=["POST"])
def cadastrar_bibliotecario():
    try:
        nome = request.form["nome"]
        email = request.form["email"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            INSERT INTO bibliotecario (nome, email)
            VALUES (%s, %s)
        """


        valores = (nome, email)


        cursor.execute(sql, valores)
        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/bibliotecarios")


    except Exception as erro:
        return f"Erro ao cadastrar bibliotecário: {erro}"
    



if __name__ == "__main__":
    app.run(debug=True)

