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


if __name__ == "__main__":
    app.run(debug=True)
