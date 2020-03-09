import sys # PARA SAIR DO SISTEMA
import psycopg2 # PARA USAR O BANCO DE DADOS
import datetime # PARA CONVERTER HORÁRIO E DATA
from tabulate import tabulate # PARA LISTAR LINDAMENTE
from time import sleep # PARA DAR EFEITO DRAMÁTICO NOS TEXTOS DE LOGIN E DE LOGOUT

## TEXTO É UMA FUNÇÃO INPUT QUE SEMPRE TESTA O QUE O USUÁRIO QUER FAZER
def texto(txt=None, vazio=False, isVariable=False):
    global cur
    
    print('-'*20)
    ## SE NÃO FOR CHAMADO COM UM TEXTO, E NÃO PODE SER RETORNADO VAZIO 
    if txt == None and vazio == False:
        i = input('O que deseja fazer a seguir? ').lower()
        print('')

    ## SE NÃO FOR CHAMADO COM UM TEXTO, MAS PODE SER RETORNADO VAZIO
    elif txt == None and vazio == True:
        return i

    ## SE FOR CHAMADO COM UM TEXTO, ADICIONA UM ESPAÇO NO PRINT E RETORNA O OBJETO
    else:
        i = input(txt + " ").lower()
        print('')
        return i

    ## SE NÃO A FUNÇÃO NÃO TIVER SIDO CHAMADA PARA DEFINIR VARIÁVEIS, CHAMA OUTRAS FUNÇÕES
    if isVariable == False:
        while True:
            if i == 'ajuda':
                ajuda()

            elif i == 'sair':
                print('Mas já? Certeza?')
                sleep(1)
                print('Bem, nesse caso, boa sorte e volte logo! Vamos sentir sua falta! ;)')
                sleep(3)
                print('')
                print('')
                cur.close()
                con.close()
                sys.exit()
            
            elif 'criar p' in i:
                criar_projeto()

            elif 'editar p' in i:
                editar_projeto()

            elif 'atualizar p' in i:
                atualizar_projetos()

            elif 'listar p' in i:
                listar_projetos()

            elif 'excluir p' in i:
                excluir_projeto()

            elif 'buscar' in i:
                buscar_tarefas()

            elif 'criar t' in i:
                criar_tarefa()

            elif 'editar t' in i:
                editar_tarefa()

            elif 'atualizar t' in i:
                atualizar_tarefas()

            elif 'listar t' in i:
                listar_tarefas()

            elif 'excluir t' in i:
                excluir_tarefa()
            
            else:
                print('Comando não reconhecido. Se precisar de ajuda, digite "ajuda".')
                print('')
                texto()

### INICIA O PROMAN
def iniciar():
        global con
        global cur
        con = None
        cur = None

        print('')
        print('')
        print('Seja bem-vindo(a) ao ProMan - Project Manager, seu Gerenciador de Projetos!')
        print('')
        sleep(1)
        print('Criado por Vinícius de Carvalho')
        print('viniciusgouvcarv@gmail.com')
        print('')
        sleep(3)
                
        try:
            con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
            cur = con.cursor()
            print("Nós sentimos a sua falta! ;)")
            print('')

        except psycopg2.OperationalError as e:
            print('Infelizmente, não foi possível se conectar ao servidor. Por favor, verifique se seu computador está conectado à internet.')
            print('')
        
        except psycopg2.DatabaseError as e:
                    print('Infelizmente, não foi possível logar graças ao erro abaixo:')
                    print('')
                    print(f'Error {e}')
                    print('')
                    sys.exit()
        
        ## CRIA AS TABELAS, SE JÁ NÃO EXISTIREM
        cur.execute("""CREATE TABLE IF NOT EXISTS tbl_projects (
            id_projeto SERIAL PRIMARY KEY,
            titulo_projeto VARCHAR(255) NOT NULL UNIQUE,
            data_previsao DATE NOT NULL,
            horario_entrega TIME,
            obs_projeto VARCHAR(510)
        );""")

        cur.execute("""CREATE TABLE IF NOT EXISTS tbl_tasks (
            id_tarefa SERIAL,
            titulo_tarefa VARCHAR(255) NOT NULL,
            obs_tarefa VARCHAR(510),
            projeto INTEGER,
            FOREIGN KEY (projeto) REFERENCES tbl_projects (id_projeto) ON DELETE CASCADE
        );""")

        print('Caso tenha dúvidas sobre como utilizar o sistema, digite "ajuda" a qualquer instante.')
        print('')
        texto()

## PRINTA OS COMANDOS QUE O PROMAN ACEITA
def ajuda():
    print('Abaixo, estão a lista de comandos que o sistema reconhece:')
    print('')
    print('--ajuda: Abre esse menu de comandos')
    print('--sair: Desloga do sistema de maneira segura')
    print('--criar projeto: Abre o menu para você criar um novo projeto')
    print('--listar projetos: Lista todos os seus projetos atuais de acordo com a data e o horário de entrega (dos mais próximos aos mais distantes)')
    print('--editar projeto: Abre o menu para você selecionar um projeto e editá-lo')
    print('--atualizar projeto: Abre o menu para você selecionar um projeto e atualizá-lo')
    print('--excluir projeto: Abre o menu para você selecionar um projeto e exclui-lo')
    print('--buscar tarefas: Abre o menu para buscar tarefas dentre todos os projetos')
    print('--criar tarefa: Abre o menu para você criar uma nova tarefa')
    print('--listar tarefas: Lista todas as tarefas relacionadas a um projeto')
    print('--editar tarefa: Abre o menu para você selecionar uma tarefa e editá-la')
    print('--atualizar tarefa: Abre o menu para você selecionar uma tarefa e atualizar-la')
    print('--excluir tarefa: Abre o menu para você selecionar uma tarefa e exclui-la')
    print('')
    texto()

## CRIA UM PROJETO
def criar_projeto():
    global cur
    global con

    ## PEGA AS VARIÁVEIS
    with cur:
        titulo = texto('Qual o título do projeto que deseja criar?', isVariable=True)
        dia = texto('Qual o dia do mês em que deve ser entregue?', isVariable=True)
        mes = texto('Qual o mês em que deve ser entregue?', isVariable=True)
        ano = texto('Qual o ano em que deve ser entregue?', isVariable=True)        
        
        ## DEIXA A DATA NUM FORMATO ACEITÁVEL
        try:
            data = datetime.date(int(ano), int(mes), int(dia))
        except:
            print('Formato da data está inválido.')
            print('')
            texto()
        
        ## DEIXA O HORÁRIO NUM FORMATO ACEITÁVEL, SE HOUVER
        horas = texto('Se o projeto tiver um horário para ser entregue, digite-o no formato "21:30", ou só aperte "enter" se não tiver.')
        try:
            horas = horas.split(":")
            horario = datetime.time(hour=int(horas[0]), minute=int(horas[1]), second=0)
        except:
            print('Horário não será incluído no projeto (pode ser alterado mais tarde).')
            print('')
            horario = '00:00:01'

        obs = texto('Digite uma observação caso queira. Se não, só pressione "enter".', vazio=True, isVariable=True)
        
        ## ADICIONA O PROJETO NA TABELA
        try:
            cur.execute("""
            INSERT INTO tbl_projects (titulo_projeto, data_previsao, horario_entrega, obs_projeto)
            VALUES (%s, %s, %s, %s);
                """, (titulo, data, horario, obs))
            print('Projeto ' + titulo + ' criado com sucesso!')
            print('')
        except psycopg2.errors.UniqueViolation as e:
            print('Já existe um projeto com esse título, por favor, escolha outro.')
            print('')

        con.commit()

    con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
    cur = con.cursor()
    texto()
    
## LISTA TODOS OS PROJETOS
def listar_projetos():
    global cur

    ## PEGA TODOS OS PROJETOS E OS ORDENA POR DATA E HORÁRIO (SEM HORÁRIO SEMPRE APARECEM ANTES)
    cur.execute("""
        SELECT * FROM tbl_projects ORDER BY data_previsao, horario_entrega ASC
    """)

    projetos = cur.fetchall()
    print('-'*20)
    
    if len(projetos) == 0:
        print('Não há nenhum projeto que atinja os requisitos desejados.')
        print('')
        texto()
    
    ## EXISTINDO ALGUM PROJETO CRIADO, ELE FORMATA PARA UMA MELHOR VISUALIZAÇÃO E OS LISTA
    else:
        ids = []
        titulos = []
        datas = []
        horarios = []
        observacoes = []    
        for projeto in projetos:
            ids.append(projeto[0])
            titulos.append(projeto[1].capitalize())
            datas.append(format(projeto[2], "%d/%m/%Y"))
            if projeto[3] == datetime.time(0,0,second=1):
                horarios.append('Sem horário')
            else:
                horarios.append(projeto[3])
            if projeto[4] == '':
                observacoes.append('Nenhuma')
            else:
                observacoes.append(projeto[4].capitalize())
        
        if len(ids) > 1:
            lista = {'ID': ids, 'Título': titulos, 'Data': datas, 'Horário': horarios, 'Observação': observacoes}
        else:
            lista = {'ID': ids, 'Título': titulos, 'Data': datas, 'Horário': horarios, 'Observação': observacoes}

    print('LISTA DE PROJETOS')
    print(tabulate(lista, showindex=False, headers='keys', tablefmt="grid"))
    texto()

## EDITA UM PROJETO
def editar_projeto():
    global cur
    global con

    with cur:
        ## DEFINE A COLUNA QUE VAI SER EDITADA
        coluna = texto('Qual dado você quer editar? Título, data de previsão, horário de entrega ou observação?', isVariable=True)
        if ('tit' in coluna) or ('tít' in coluna):
            coluna = 'titulo_projeto'
        elif 'dat' in coluna:
            coluna = 'data_previsao'
        elif 'hor' in coluna:
            coluna = 'horario_entrega'
        elif 'obs' in coluna:
            coluna = 'obs_projeto'
        else:
            print('Comando não entendido.')
            print('')
            texto()

        ## DE ACORDO COM A COLUNA A SER EDITADA, DÁ UMA ALTERNATIVA DE EDIÇÃO DIFERENTE
        if coluna == 'titulo_projeto':
            alteracao = texto('Agora, digite o novo título.', isVariable=True)

        elif coluna == 'obs_projeto':
            alteracao = texto('Agora, digite a nova observação, ou só aperte enter para apagar a anterior.', isVariable=True)

        elif coluna == 'horario_entrega':
            alteracao = texto('Agora, digite o novo horário separado por ":". (ex: 21:45)', isVariable=True)
            try:
                ## SE A COLUNA FOR O HORÁRIO, O PÕE NUM FORMATO ACEITÁVEL
                novo_horario = []
                hora = alteracao.split(":")
                for valor in hora:
                    novo_horario.append(int(valor))
                alteracao = datetime.time(novo_horario[0], novo_horario[1], 0)

            except:
                print('Horário atual será apagado.')
                print('')
                alteracao = datetime.time(0,0,1)
        
        elif coluna == 'data_previsao':
            alteracao = texto('Agora, digite os novos dia, mês e ano do projeto separados por espaço. (ex: 21 12 2012)', isVariable=True)
            try:
                ## SE A COLUNA FOR A DATA, A PÕE NUM FORMATO ACEITÁVEL
                nova_data = []
                data = alteracao.split(" ")
                for valor in data:
                    nova_data.append(int(valor))
                alteracao = datetime.date(nova_data[2], nova_data[1], nova_data[0])

            except:
                print('Data inválida.')
                print('')
                editar_projeto()

        ## DEFINE O PROJETO QUE VAI SER ALTERADO
        dado = texto('Por favor, digite o título ou ID do projeto que você quer editar. (ex: "titulo Limpar a casa" ou "id 3")', isVariable=True)
        try:
            comando = dado.split(" ")
            if comando[0] == 'titulo':
                coluna_condicao = 'titulo_projeto'
                valor_condicao = dado[7:]

            elif comando[0] == 'id':
                coluna_condicao = 'id_projeto'
                valor_condicao = dado[3:]
            
            else:
                print('Comando não entendido.')
                print('')
                texto()
        except:
            print('Comando não entendido.')
            print('')
            texto()

        ## ALTERA O PROJETO
        sql_edicao = "UPDATE tbl_projects SET " + coluna + " = '" + str(alteracao) + "' WHERE " + coluna_condicao + " = '" + valor_condicao + "';"
        cur.execute(sql_edicao)
        con.commit()

        print('Projeto alterado com sucesso!')

    con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
    cur = con.cursor()
    texto()

## ATUALIZA PROJETOS
def atualizar_projetos():
    global cur
    texto('Atualizar projetos!')
    texto()

## EXCLUI UM PROJETO
def excluir_projeto():
    global cur
    global con

    with cur:
        ## DEFINE O PROJETO QUE VAI SER EXCLUÍDO
        dado = texto('Por favor, digite o título ou ID do projeto que você quer excluir. (ex: "titulo Limpar a casa" ou "id 3")', isVariable=True)
        try:
            comando = dado.split(" ")
            if comando[0] == 'titulo':
                coluna_condicao = 'titulo_projeto'
                valor_condicao = dado[7:]

            elif comando[0] == 'id':
                coluna_condicao = 'id_projeto'
                valor_condicao = dado[3:]
            
            else:
                print('Comando não entendido.')
                print('')
                texto()
        except:
            print('Comando não entendido.')
            print('')
            texto()

        ## EXCLUI O PROJETO
        sql_edicao = "DELETE FROM tbl_projects WHERE " + coluna_condicao + " = '" + valor_condicao + "';"
        cur.execute(sql_edicao)
        print('Projeto excluído com sucesso!')
        print('')
        con.commit()
    
    con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
    cur = con.cursor()
    texto()

## CRIA UMA TAREFA
def criar_tarefa():
    global cur
    global con

    with cur:
        ## DEFINE A QUAL PROJETO A TAREFA SERÁ ATRIBUÍDA
        id_projeto = texto('Qual a ID do projeto à qual a nova tarefa será atribuída? (digite só o número)', isVariable=True)
        try:
            cur.execute("""
                SELECT * FROM tbl_projects WHERE id_projeto = %s
            """, (id_projeto))
            projetos = cur.fetchall()
        except:
            print('ID do projeto não foi encontrada.')
            print('')
            texto()

        ## DEFINE O TÍTULO DA TAREFA E CHECA SE JÁ NÃO EXISTE UM NO MESMO PROJETO
        titulo = texto('Qual o título da tarefa que deseja criar?', isVariable=True)
        cur.execute("""
                    SELECT titulo_tarefa FROM tbl_tasks WHERE projeto = %s
                ;""", (id_projeto))
        tarefas = cur.fetchall()
        for tarefa in tarefas:
            if titulo == tarefa[0]:
                print('Não é permitido atribuir o mesmo título a duas tarefas diferentes dentro de um único projeto.')
                print('')
                criar_tarefa()

        ## DEFINE A OBSERVAÇÃO
        obs = texto('Digite uma observação caso queira. Se não, só pressione "enter".', vazio=True, isVariable=True)

        ## CRIA A TAREFA
        try:
            cur.execute("""
                INSERT INTO tbl_tasks (titulo_tarefa, obs_tarefa, projeto)
                VALUES (%s, %s, %s);
            """, (titulo, obs, id_projeto))
            print('Tarefa ' + titulo + ' criada com sucesso!')
            print('')
        except:
            print('ID da tarefa não encontrada!')
            print('')
        con.commit()

    con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
    cur = con.cursor()
    texto()

## LISTA TODAS AS TAREFAS
def listar_tarefas():
    global cur

    ## DEFINE O PROJETO QUE CONTÉM AS TAREFAS QUE SERÃO LISTADAS
    valor_condicao = texto('Por favor, digite a ID do projeto cujas tarefas você quer listar. (Só o número mesmo)', isVariable=True)
    try:
        teste = int(valor_condicao)
    except:
        while True:
            valor_condicao = texto('Por favor, digite só o número do ID do projeto. (ex: "5" ou "21")')
            try:
                teste = int(valor_condicao)
                break
            except:
                pass

    ## LISTA AS TAREFAS
    cur.execute("""
        SELECT * FROM tbl_tasks WHERE projeto = %s;
    """, (valor_condicao,))
    tarefas = cur.fetchall()

    print('-'*20)
    if len(tarefas) == 0:
        print('Não há nenhuma tarefa que atinja os requisitos desejados.')
        print('')
        texto()

    else:    
        ids = []
        titulos = []
        observacoes = []
        ids1 = []
        titulos_projetos = []
        for tarefa in tarefas:
            ids.append(tarefa[0])
            titulos.append(tarefa[1].capitalize())
            ids1.append(tarefa[3])
            if tarefa[2] == '':
                observacoes.append('Nenhuma')
            else:
                observacoes.append(tarefa[2].capitalize())
            cur.execute("SELECT titulo_projeto FROM tbl_projects WHERE id_projeto = %s", (str(tarefa[3])))
            titulos_projetos.append(cur.fetchone()[0].capitalize())

        if len(ids) > 1:
            lista = {'ID da Tarefa': ids, 'Título da Tarefa': titulos, 'Observação': observacoes, 'ID do Projeto': ids1, 'Titulo do Projeto': titulos_projetos}
        else:
            lista = {'ID da Tarefa': ids, 'Título': titulos, 'Observação': observacoes, 'ID do Projeto': ids1, 'Titulo do Projeto': titulos_projetos}

    print('LISTA DE TAREFAS')
    print(tabulate(lista, showindex=False, headers='keys', tablefmt="grid"))
    texto()

## EDITA UMA TAREFA
def editar_tarefa():
    global cur
    global con

    with cur:
        ## DEFINE A COLUNA QUE VAI SER EDITADA
        coluna = texto('Qual dado você quer editar? Título ou observação?', isVariable=True)
        if ('tit' in coluna) or ('tít' in coluna):
            coluna = 'titulo_tarefa'
        elif 'obs' in coluna:
            coluna = 'obs_tarefa'
        else:
            print('Comando não entendido.')
            print('')
            texto()

        ## PARA CADA COLUNA, DÁ UMA ALTERNATIVA DIFERENTE DE EDIÇÃO        
        if coluna == 'obs_tarefa':
            alteracao = texto('Agora, digite a nova observação, ou só aperte enter para apagar a anterior.', isVariable=True)

        else:
            alteracao = texto('Agora, digite o novo título.', isVariable=True)


        ## DEFINE A TAREFA QUE VAI SER EDITADA
        dado = texto('Por favor, digite a ID da tarefa que você quer editar. (ex: "3")', isVariable=True)
        
        try:
            dado = int(dado)
            valor_condicao = str(dado)
        except:
            print('Comando não entendido.')
            print('')
            texto()

        ## EDITA A TAREFA
        sql_edicao = "UPDATE tbl_tasks SET " + coluna + " = '" + alteracao + "' WHERE id_tarefa = '" + valor_condicao + "';"
        cur.execute(sql_edicao)
        con.commit()

    con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
    cur = con.cursor()
    texto()

def atualizar_tarefas():
    global cur
    texto('Atualizar tarefas!')
    texto()

## EXCLUI UMA TAREFA
def excluir_tarefa():
    global cur
    global con

    with cur:
        ## DEFINE A TAREFA QUE VAI SER EXCLUÍDA
        dado = texto('Por favor, digite ID da tarefa que você quer excluir. (Só o número mesmo)', isVariable=True)

        ## EXCLUI A TAREFA
        cur.execute("""
            DELETE FROM tbl_tasks WHERE id_tarefa = %s
        ;""", (dado,))
        print('Tarefa excluída com sucesso!')
        print('')
        con.commit()

    con = psycopg2.connect(database='d77fge1uko3ish', user='nompkqfhfxxlhj', host='ec2-3-231-46-238.compute-1.amazonaws.com', password='b986629a71a7d3b487bfc5ee0a82496b5fbd29362c1bdec27d915f66bf6b3bab', port = 5432)
    cur = con.cursor()
    texto()

## LISTA TODAS AS TAREFAS QUE CONTÊM OS REQUISITOS EXIGIDOS, INDEPENDENTE DE PROJETOS
def buscar_tarefas():
    global cur

    ## DEFINE OS REQUISITOS
    titulo = texto('A pesquisa deve ter, ao menos, 3 caracteres:', isVariable=True)
    if len(titulo) < 3:
        print('Por favor, digite mais do que 2 caracteres.')
        print('')
        buscar_tarefas()

    ## LISTA AS TAREFAS
    sql_query = "select * from tbl_tasks where titulo_tarefa like '%%" + titulo + "%%'"
    cur.execute(sql_query)
    tarefas = cur.fetchall()

    print('-'*20)
    if len(tarefas) == 0:
        print('Não há nenhuma tarefa que atinja os requisitos desejados.')
        print('')
        texto()
    else:    
        ids = []
        titulos = []
        observacoes = []
        ids1 = []
        titulos_projetos = []

        for tarefa in tarefas:
            ids.append(tarefa[0])
            titulos.append(tarefa[1].capitalize())
            ids1.append(tarefa[3])
            if tarefa[2] == '':
                observacoes.append('Nenhuma')
            else:
                observacoes.append(tarefa[2].capitalize())
            cur.execute("SELECT titulo_projeto FROM tbl_projects WHERE id_projeto = %s", (str(tarefa[3])))
            titulos_projetos.append(cur.fetchone()[0].capitalize())

        if len(ids) > 1:
            lista = {'ID da Tarefa': ids, 'Título da Tarefa': titulos, 'Observação': observacoes, 'ID do Projeto': ids1, 'Titulo do Projeto': titulos_projetos}
        else:
            lista = {'ID da Tarefa': ids, 'Título': titulos, 'Observação': observacoes, 'ID do Projeto': ids1, 'Titulo do Projeto': titulos_projetos}

    print('LISTA DE TAREFAS')
    print(tabulate(lista, showindex=False, headers='keys', tablefmt="grid"))
    texto()

iniciar()