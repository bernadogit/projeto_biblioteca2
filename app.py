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
    
# Rotas para empréstimos
@app.route("/emprestimos")
def listar_emprestimos():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        sql = """
            SELECT
                e.id_emprestimo,
                a.nome AS aluno,
                l.titulo AS livro,
                b.nome AS bibliotecario,
                e.data_emprestimo,
                e.data_prevista_devolucao,
                e.data_devolucao,
                e.status
            FROM emprestimo e
            INNER JOIN aluno a ON e.id_aluno = a.id_aluno
            INNER JOIN livro l ON e.id_livro = l.id_livro
            INNER JOIN bibliotecario b ON e.id_bibliotecario = b.id_bibliotecario
            ORDER BY e.id_emprestimo DESC
        """


        cursor.execute(sql)
        emprestimos = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template("emprestimos.html", emprestimos=emprestimos)


    except Exception as erro:
        return f"Erro ao listar empréstimos: {erro}"




@app.route("/emprestimos/novo")
def formulario_emprestimo():
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("SELECT * FROM aluno ORDER BY nome")
        alunos = cursor.fetchall()


        cursor.execute("SELECT * FROM livro WHERE status = 'Disponível' ORDER BY titulo")
        livros = cursor.fetchall()


        cursor.execute("SELECT * FROM bibliotecario ORDER BY nome")
        bibliotecarios = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template(
            "emprestimo_form.html",
            alunos=alunos,
            livros=livros,
            bibliotecarios=bibliotecarios
        )


    except Exception as erro:
        return f"Erro ao carregar formulário de empréstimo: {erro}"




@app.route("/emprestimos/cadastrar", methods=["POST"])
def cadastrar_emprestimo():
    try:
        id_aluno = request.form["id_aluno"]
        id_livro = request.form["id_livro"]
        id_bibliotecario = request.form["id_bibliotecario"]
        data_emprestimo = request.form["data_emprestimo"]
        data_prevista_devolucao = request.form["data_prevista_devolucao"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            INSERT INTO emprestimo (
                id_aluno,
                id_livro,
                id_bibliotecario,
                data_emprestimo,
                data_prevista_devolucao,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """


        valores = (
            id_aluno,
            id_livro,
            id_bibliotecario,
            data_emprestimo,
            data_prevista_devolucao,
            "Emprestado"
        )


        cursor.execute(sql, valores)


        cursor.execute(
            "UPDATE livro SET status = 'Emprestado' WHERE id_livro = %s",
            (id_livro,)
        )


        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/emprestimos")


    except Exception as erro:
        return f"Erro ao cadastrar empréstimo: {erro}"


# Rota para devolução de livro
@app.route("/emprestimos/devolver/<int:id_emprestimo>")
def devolver_livro(id_emprestimo):


    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("""
            SELECT id_livro
            FROM emprestimo
            WHERE id_emprestimo = %s
        """, (id_emprestimo,))


        emprestimo = cursor.fetchone()


        if emprestimo:


            id_livro = emprestimo["id_livro"]


            cursor.execute("""
                UPDATE emprestimo
                SET
                    data_devolucao = CURDATE(),
                    status = 'Devolvido'
                WHERE id_emprestimo = %s
            """, (id_emprestimo,))


            cursor.execute("""
                UPDATE livro
                SET status = 'Disponível'
                WHERE id_livro = %s
            """, (id_livro,))


            conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/emprestimos")


    except Exception as erro:
        return f"Erro ao devolver livro: {erro}"

## Rota CRUD aluno
@app.route("/alunos/editar/<int:id_aluno>")
def editar_aluno(id_aluno):
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute(
            "SELECT * FROM aluno WHERE id_aluno = %s",
            (id_aluno,)
        )


        aluno = cursor.fetchone()


        cursor.close()
        conexao.close()


        return render_template("aluno_editar.html", aluno=aluno)


    except Exception as erro:
        return f"Erro ao carregar aluno: {erro}"




@app.route("/alunos/atualizar/<int:id_aluno>", methods=["POST"])
def atualizar_aluno(id_aluno):
    try:
        nome = request.form["nome"]
        serie = request.form["serie"]
        turma = request.form["turma"]
        telefone = request.form["telefone"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            UPDATE aluno
            SET nome = %s,
                serie = %s,
                turma = %s,
                telefone = %s
            WHERE id_aluno = %s
        """


        valores = (nome, serie, turma, telefone, id_aluno)


        cursor.execute(sql, valores)
        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/alunos")


    except Exception as erro:
        return f"Erro ao atualizar aluno: {erro}"




@app.route("/alunos/excluir/<int:id_aluno>")
def excluir_aluno(id_aluno):
    try:
        conexao = conectar()
        cursor = conexao.cursor()


        cursor.execute(
            "DELETE FROM aluno WHERE id_aluno = %s",
            (id_aluno,)
        )


        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/alunos")


    except Exception as erro:
        return f"Erro ao excluir aluno: {erro}"

@app.route("/livros/editar/<int:id_livro>")
def editar_livro(id_livro):
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute(
            "SELECT * FROM livro WHERE id_livro = %s",
            (id_livro,)
        )


        livro = cursor.fetchone()


        cursor.close()
        conexao.close()


        return render_template("livro_editar.html", livro=livro)


    except Exception as erro:
        return f"Erro ao carregar livro: {erro}"




@app.route("/livros/atualizar/<int:id_livro>", methods=["POST"])
def atualizar_livro(id_livro):
    try:
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        categoria = request.form["categoria"]
        status = request.form["status"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            UPDATE livro
            SET titulo = %s,
                autor = %s,
                categoria = %s,
                status = %s
            WHERE id_livro = %s
        """


        valores = (titulo, autor, categoria, status, id_livro)


        cursor.execute(sql, valores)
        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/livros")


    except Exception as erro:
        return f"Erro ao atualizar livro: {erro}"




@app.route("/livros/excluir/<int:id_livro>")
def excluir_livro(id_livro):
    try:
        conexao = conectar()
        cursor = conexao.cursor()


        cursor.execute(
            "DELETE FROM livro WHERE id_livro = %s",
            (id_livro,)
        )


        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/livros")


    except Exception as erro:
        return f"Erro ao excluir livro: {erro}"

@app.route("/bibliotecarios/editar/<int:id_bibliotecario>")
def editar_bibliotecario(id_bibliotecario):
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute(
            "SELECT * FROM bibliotecario WHERE id_bibliotecario = %s",
            (id_bibliotecario,)
        )


        bibliotecario = cursor.fetchone()


        cursor.close()
        conexao.close()


        return render_template(
            "bibliotecario_editar.html",
            bibliotecario=bibliotecario
        )


    except Exception as erro:
        return f"Erro ao carregar bibliotecário: {erro}"




@app.route("/bibliotecarios/atualizar/<int:id_bibliotecario>", methods=["POST"])
def atualizar_bibliotecario(id_bibliotecario):
    try:
        nome = request.form["nome"]
        email = request.form["email"]


        conexao = conectar()
        cursor = conexao.cursor()


        sql = """
            UPDATE bibliotecario
            SET nome = %s,
                email = %s
            WHERE id_bibliotecario = %s
        """


        valores = (nome, email, id_bibliotecario)


        cursor.execute(sql, valores)
        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/bibliotecarios")


    except Exception as erro:
        return f"Erro ao atualizar bibliotecário: {erro}"




@app.route("/bibliotecarios/excluir/<int:id_bibliotecario>")
def excluir_bibliotecario(id_bibliotecario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()


        cursor.execute(
            "DELETE FROM bibliotecario WHERE id_bibliotecario = %s",
            (id_bibliotecario,)
        )


        conexao.commit()


        cursor.close()
        conexao.close()


        return redirect("/bibliotecarios")


    except Exception as erro:
        return f"Erro ao excluir bibliotecário: {erro}"


if __name__ == "__main__":
    app.run(debug=True)

