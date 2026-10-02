from flask import Flask, render_template, request, redirect, flash, session

import mysql.connector
from config import DB_CONFIG
from datetime import datetime




app = Flask(__name__)
app.secret_key = "biblioteca_escolar"




def conectar():
   return mysql.connector.connect(**DB_CONFIG)




@app.route("/")
def index():
    try:
        if "id_usuario" not in session:
            return redirect("/login")

        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        cursor.execute("SELECT COUNT(*) AS total FROM aluno")
        total_alunos = cursor.fetchone()["total"]


        cursor.execute("SELECT COUNT(*) AS total FROM livro")
        total_livros = cursor.fetchone()["total"]


        cursor.execute("SELECT COUNT(*) AS total FROM livro WHERE status = 'Disponível'")
        total_disponiveis = cursor.fetchone()["total"]


        cursor.execute("SELECT COUNT(*) AS total FROM emprestimo WHERE status = 'Emprestado'")
        total_emprestimos = cursor.fetchone()["total"]


        cursor.close()
        conexao.close()


        return render_template(
            "index.html",
            total_alunos=total_alunos,
            total_livros=total_livros,
            total_disponiveis=total_disponiveis,
            total_emprestimos=total_emprestimos
        )


    except Exception as erro:
        flash(f"Erro ao carregar página inicial: {erro}", "erro")
        return render_template(
            "index.html",
            total_alunos=0,
            total_livros=0,
            total_disponiveis=0,
            total_emprestimos=0
        )


@app.route("/alunos")
def listar_alunos():
    try:
        pesquisa = request.args.get("pesquisa", "")


        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        if pesquisa:
            sql = """
                SELECT * FROM aluno
                WHERE nome LIKE %s
                   OR serie LIKE %s
                   OR turma LIKE %s
                ORDER BY nome
            """


            valor = f"%{pesquisa}%"
            cursor.execute(sql, (valor, valor, valor))
        else:
            cursor.execute("SELECT * FROM aluno ORDER BY nome")


        alunos = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template(
            "alunos.html",
            alunos=alunos,
            pesquisa=pesquisa
        )


    except Exception as erro:
        flash(f"Erro ao listar alunos: {erro}", "erro")
        return redirect("/")




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


       # ACRESCENTE A MENSAGEM DE SUCESSO AO CADASTRAR O ALUNO
       flash("Aluno cadastrado com sucesso!", "sucesso")
       return redirect("/alunos")


   except Exception as erro:
       flash(f"Erro ao cadastrar aluno: {erro}", "erro")
       return redirect("/alunos")


# Rotas para livros




@app.route("/livros")
def listar_livros():
    try:
        pesquisa = request.args.get("pesquisa", "")


        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        if pesquisa:
            sql = """
                SELECT * FROM livro
                WHERE titulo LIKE %s
                   OR autor LIKE %s
                   OR categoria LIKE %s
                   OR status LIKE %s
                ORDER BY titulo
            """


            valor = f"%{pesquisa}%"
            cursor.execute(sql, (valor, valor, valor, valor))
        else:
            cursor.execute("SELECT * FROM livro ORDER BY titulo")


        livros = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template(
            "livros.html",
            livros=livros,
            pesquisa=pesquisa
        )


    except Exception as erro:
        flash(f"Erro ao listar livros: {erro}", "erro")
        return redirect("/")





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
       flash("Livro cadastrado com sucesso!", "sucesso")


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


       flash("Bibliotecário cadastrado com sucesso!", "sucesso")


       return redirect("/bibliotecarios")


   except Exception as erro:
       return f"Erro ao cadastrar bibliotecário: {erro}"


# Rotas para empréstimos




@app.route("/emprestimos")
def listar_emprestimos():
    try:
        status = request.args.get("status", "")


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
        """


        if status:
            sql += " WHERE e.status = %s ORDER BY e.id_emprestimo DESC"
            cursor.execute(sql, (status,))
        else:
            sql += " ORDER BY e.id_emprestimo DESC"
            cursor.execute(sql)


        emprestimos = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template(
            "emprestimos.html",
            emprestimos=emprestimos,
            status=status
        )


    except Exception as erro:
        flash(f"Erro ao listar empréstimos: {erro}", "erro")
        return redirect("/")


@app.route("/emprestimos/novo")
def formulario_emprestimo():
   try:
       conexao = conectar()
       cursor = conexao.cursor(dictionary=True)


       cursor.execute("SELECT * FROM aluno ORDER BY nome")
       alunos = cursor.fetchall()


       cursor.execute(
           "SELECT * FROM livro WHERE status = 'Disponível' ORDER BY titulo")
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
       data_emp = datetime.strptime(data_emprestimo, "%Y-%m-%d")
       data_dev = datetime.strptime(data_prevista_devolucao, "%Y-%m-%d")




       if data_dev < data_emp:
           flash("A data prevista de devolução não pode ser menor que a data do empréstimo.", "erro")
           return redirect("/emprestimos/novo")




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


       flash("Empréstimo registrado com sucesso!", "sucesso")


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


       flash("Livro devolvido com sucesso!", "sucesso")
       return redirect("/emprestimos")


   except Exception as erro:
       flash("Erro ao devolver livro.", "erro")
   return redirect("/emprestimos")




# Rota CRUD aluno
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


       flash("Aluno excluído com sucesso!", "sucesso")
       return redirect("/alunos")


   except Exception as erro:
       flash(f"Erro ao atualizar aluno: {erro}", "erro")
   return redirect("/alunos")




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


       flash("Aluno excluído com sucesso!", "sucesso")
       return redirect("/alunos")


   except Exception as erro:
       flash("Não foi possível excluir o aluno. Verifique se ele possui empréstimos cadastrados.", "erro")
       return redirect("/alunos")




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


       flash("Livro atualizado com sucesso!", "sucesso")


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


       flash("Não foi possível excluir o livro. Verifique se ele possui empréstimos cadastrados.", "erro")
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


       flash("Bibliotecário atualizado com sucesso!", "sucesso")


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


       flash("Bibliotecário excluído com sucesso!", "sucesso")


       return redirect("/bibliotecarios")


   except Exception as erro:
       flash("Não foi possível excluir o bibliotecário. Verifique se ele possui empréstimos cadastrados.", "erro")
       return redirect("/bibliotecario")

# Rota Empréstimos atrasados
@app.route("/emprestimos/atrasados")
def listar_emprestimos_atrasados():
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
                DATEDIFF(CURDATE(), e.data_prevista_devolucao) AS dias_atraso,
                e.status
            FROM emprestimo e
            INNER JOIN aluno a ON e.id_aluno = a.id_aluno
            INNER JOIN livro l ON e.id_livro = l.id_livro
            INNER JOIN bibliotecario b ON e.id_bibliotecario = b.id_bibliotecario
            WHERE e.status = 'Emprestado'
              AND e.data_prevista_devolucao < CURDATE()
            ORDER BY e.data_prevista_devolucao
        """


        cursor.execute(sql)
        emprestimos = cursor.fetchall()


        cursor.close()
        conexao.close()


        return render_template(
            "emprestimos_atrasados.html",
            emprestimos=emprestimos
        )


    except Exception as erro:
        flash(f"Erro ao listar empréstimos atrasados: {erro}", "erro")
        return redirect("/emprestimos")

## Rota de Login
@app.route("/login")
def login():
    return render_template("login.html")




@app.route("/login/autenticar", methods=["POST"])
def autenticar():
    email = request.form["email"]
    senha = request.form["senha"]


    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)


        sql = """
            SELECT *
            FROM usuario
            WHERE email = %s
              AND senha = %s
              AND status = 'Ativo'
        """


        cursor.execute(sql, (email, senha))
        usuario = cursor.fetchone()


        cursor.close()
        conexao.close()


        if usuario:
            session["id_usuario"] = usuario["id_usuario"]
            session["nome"] = usuario["nome"]
            session["perfil"] = usuario["perfil"]


            flash("Login realizado com sucesso!", "sucesso")
            return redirect("/")
        else:
            flash("E-mail ou senha inválidos.", "erro")
            return redirect("/login")


    except Exception as erro:
        flash(f"Erro ao realizar login: {erro}", "erro")
        return redirect("/login")




@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect("/login")



if __name__ == "__main__":
   app.run(debug=True)
