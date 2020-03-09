# ProMan-Project-Manager
ProMan é um gerenciador de projetos onde você pode criar projetos com data de entrega e título (obrigatórios) e observações, horário de entrega e tarefas (opcionais)!

Para utilizar o ProMan, você pode rodar o aplicativo "proman.exe" clicando duas vezes, ou se você tiver Python 3.8.0 ou mais recente instalado em sua máquina (que você pode adquirir aqui https://www.python.org/downloads/release/python-382/), você pode abrir seu prompt de comando na pasta onde se encontra o arquivo "proman.py" e rodar o código com "python proman.py" ou "python3 proman.py".

Caso você opte por abrir via terminal, tenha em mente que você precisará instalar psycopg2 e tabulate, normalmente através dos comandos "pip install psycopg2" e "pip install tabulate".

Independente de quais métodos você utilizar para rodar o ProMan, será aberto um terminal com mensagens de saudações e será esperado que você comece a utilizá-lo. Para saber quais comandos o ProMan recebe, digite "ajuda" e pressione enter. Veja qual o retorno desse comando abaixo:

--ajuda: Abre esse menu de comandos

--sair: Desloga do sistema de maneira segura

--criar projeto: Abre o menu para você criar um novo projeto

--listar projetos: Lista todos os seus projetos atuais de acordo com a data e o horário de entrega (dos mais próximos aos mais distantes)

--editar projeto: Abre o menu para você selecionar um projeto e editá-lo

--excluir projeto: Abre o menu para você selecionar um projeto e exclui-lo

--buscar tarefas: Abre o menu para buscar tarefas dentre todos os projetos

--criar tarefa: Abre o menu para você criar uma nova tarefa

--listar tarefas: Lista todas as tarefas relacionadas a um projeto

--editar tarefa: Abre o menu para você selecionar uma tarefa e editá-la

--excluir tarefa: Abre o menu para você selecionar uma tarefa e exclui-la

Então, por exemplo, para criar um novo projeto, digite "criar projeto", então, preencha corretamente os campos requisitados. Como título e data, e se haverá horário de entrega ou observação.

Após isso, para listar todos os projetos criados, digite "listar projetos".

Para editar um projeto, digite "editar projeto", digite o campo que gostaria de editar. Por exemplo, "data de previsão", digite os novos dia, mês e ano separados por espaço, ex: "21 12 2012" e escolha o projeto a ser editado através da ID, digitando "id 2", por exemplo, ou através do título digitando "titulo relatório de vendas", por exemplo.

Para excluir um projeto, selecione-o através da ID, digitando "id 2", por exemplo, ou através do título digitando "titulo relatório de vendas", por exemplo.

Para atribuir uma tarefa a um projeto, digite "criar tarefa", depois ponha a ID do projeto (só o número, por exemplo "3" ou "25"). Após, selecione o nome que gostaria de dar à tarefa e uma observação, caso queira.

Para listar todas as tarefas atribuídas a um projeto, digite "listar tarefas" e a ID do projeto (só o número, por exemplo "3" ou "25").

Para editar tarefas, escolha o campo que gostaria de editar e o novo valor, então digite a ID da tarefa (só o número, por exemplo "3" ou "25").

Para excluir uma tarefa, digite a ID da tarefa (só o número, por exemplo "3" ou "25")

Para buscar todas as tarefas que tenham determinado termo no título, por exemplo que tenham "relatório" no título, digite "buscar tarefas" e "relatório" quando lhe for pedido. Tenha em mente que o termo pesquisado precisa ter, no mínimo 3 caracteres.

A ideia do ProMan é ser simples e intuitivo! Depois do segundo ou terceiro comando, você já vai ter entendido o sistema completamente! Boa sorte!
