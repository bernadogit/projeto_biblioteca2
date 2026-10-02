USE biblioteca_1ano;


INSERT INTO aluno (nome, serie, turma, telefone)
VALUES
('Ana Clara Lima', '1º Ano', 'B', '4499999-1111'),
('João Pedro Santos', '1º Ano', 'B', '4499999-2222'),
('Maria Eduarda Ribeiro', '1º Ano', 'B', '4499999-3333'),
('Pedro Henrique Silva', '1º Ano', 'B', '4499999-4444'),
('Letícia Oliveira', '1º Ano', 'B', '4499999-5555');


INSERT INTO livro (titulo, autor, categoria, status)
VALUES
('O Pequeno Príncipe', 'Antoine de Saint-Exupéry', 'Literatura', 'Disponível'),
('Dom Casmurro', 'Machado de Assis', 'Romance', 'Disponível'),
('Harry Potter e a Pedra Filosofal', 'J. K. Rowling', 'Fantasia', 'Disponível'),
('A Menina que Roubava Livros', 'Markus Zusak', 'Drama', 'Disponível'),
('O Cortiço', 'Aluísio Azevedo', 'Literatura Brasileira', 'Disponível');


INSERT INTO bibliotecario (nome, email)
VALUES
('Bibliotecária Responsável', 'biblioteca@escola.com'),
('Auxiliar da Biblioteca', 'auxiliar.biblioteca@escola.com');
