# 🤖 Chatbot MVC para Discord - Bot LDS

## Descrição
**Bot LDS** é um chatbot para Discord que facilita o acesso a informações sobre uma unidade curricular, permitindo:

- 👨‍🎓 Estudantes consultarem secções do programa da UC  
- 👨‍💻 Administradores acederem a estatísticas, relatórios e gráficos de utilização  

## 🏗️ Estilo arquitetónico: MVC
chatbot/
├── interfaces/
│ ├── icontroller.py
│ ├── ieventlistener.py
│ ├── imodel.py
│ └── iview.py
├── model/
│ ├── dados_model.py
│ └── consulta_model.py
├── controller/
│ ├── bot_controller.py
│ ├── user_controller.py
│ └── user_commands.py
├── view/
│ ├── bot_view.py
│ └── discord_view.py
├── utils/
├── dados/
├── estatisticas/
├── logs/
├── bot.py
├── requirements.txt
└── README.md



## 🚀 Instalação

1. Crie um arquivo `.env` com seu token do Discord:

DISCORD_TOKEN=seu_token_aqui


2. Instale as dependências:

`pip install -r requirements.txt `

3. Execute o bot:

`python bot.py `


🎯 Comandos
👨‍🎓 Estudantes
!uc - Informações gerais

!competencias - Competências

!roteiro - Programa da UC

!metodologia - Métodos de ensino

!recursos - Materiais disponíveis

!calendario - Datas importantes

!avaliacao - Critérios de avaliação

!exame - Informação de exames

!ia - Uso de IA na UC

!estrutura - Equipa docente

!cartao - Cartão de aprendizagem

👨‍💻 Administradores
!relatorio - Gera relatório

!estatisticas - Mostra analytics

!historico - Consulta utilizador

❓ Ajuda
!help - Lista comandos

!help [comando] - Ajuda específica

!ajuda - Alternativa a help

⭐ Responsabilidades da Equipa ⭐
⭐ Rúben - Líder

⭐ Duarte - Model

⭐ Sofia - Controller

⭐ Yuran - View

⭐ Carlos - Tester
