import psycopg2

class BancoDeDados:
    def __init__(self, dbname='ucsal_db', user='postgres', password='1234', host='localhost', port='5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                matricula VARCHAR(20) NOT NULL,
                curso VARCHAR(100) NOT NULL,
                semestre INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def inserir_aluno(self, nome, matricula, curso, semestre):
        try:
            self.cursor.execute('''
                INSERT INTO alunos (nome, matricula, curso, semestre)
                VALUES (%s, %s, %s, %s)
            ''', (nome, matricula, curso, semestre))
            self.conn.commit()
            print('Aluno inserido com sucesso.')
        except Exception as e:
            print('Erro ao inserir aluno:', e)

    def listar_alunos(self):
        self.cursor.execute('SELECT * FROM alunos')
        alunos = self.cursor.fetchall()
        if not alunos:
            print('Nenhum aluno encontrado.')
        else:
            for aluno in alunos:
                print(aluno)

    def atualizar_aluno(self, aluno_id, nome, matricula, curso, semestre):
        try:
            self.cursor.execute('''
                UPDATE alunos
                SET nome=%s, matricula=%s, curso=%s, semestre=%s
                WHERE id=%s
            ''', (nome, matricula, curso, semestre, aluno_id))
            self.conn.commit()
            print('Aluno atualizado com sucesso.')
        except Exception as e:
            print('Erro ao atualizar aluno:', e)

    def excluir_aluno(self, aluno_id):
        try:
            self.cursor.execute('DELETE FROM alunos WHERE id=%s', (aluno_id,))
            self.conn.commit()
            print('Aluno excluído com sucesso.')
        except Exception as e:
            print('Erro ao excluir aluno:', e)

    def __del__(self):
        self.conn.close()

# Interface de linha de comando
if __name__ == '__main__':
    banco = BancoDeDados()

    while True:
        print('\n### Menu ###')
        print('1. Inserir Aluno')
        print('2. Listar Alunos')
        print('3. Atualizar Aluno')
        print('4. Excluir Aluno')
        print('5. Sair')
        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            nome = input('Digite o nome do aluno: ')
            matricula = input('Digite a matrícula do aluno: ')
            curso = input('Digite o curso do aluno: ')
            try:
                semestre = int(input('Digite o semestre do aluno: '))
                banco.inserir_aluno(nome, matricula, curso, semestre)
            except ValueError:
                print('Erro: Semestre deve ser um número inteiro.')
        elif escolha == '2':
            print('\nLista de Alunos:')
            banco.listar_alunos()
        elif escolha == '3':
            try:
                aluno_id = int(input('Digite o ID do aluno que deseja atualizar: '))
                nome = input('Digite o novo nome do aluno: ')
                matricula = input('Digite a nova matrícula do aluno: ')
                curso = input('Digite o novo curso do aluno: ')
                semestre = int(input('Digite o novo semestre do aluno: '))
                banco.atualizar_aluno(aluno_id, nome, matricula, curso, semestre)
            except ValueError:
                print('Erro: ID e semestre devem ser números inteiros.')
        elif escolha == '4':
            try:
                aluno_id = int(input('Digite o ID do aluno que deseja excluir: '))
                banco.excluir_aluno(aluno_id)
            except ValueError:
                print('Erro: ID do aluno deve ser um número inteiro.')
        elif escolha == '5':
            print('Saindo do programa. Até mais!')
            break
        else:
            print('Opção inválida. Tente novamente.')