# Chatbot MVC com Bot do Discord


Bot LDS é um chatbot para o Discord, projetado para facilitar o acesso a informações sobre uma unidade curricular. O sistema permite que estudantes consultem secções específicas do programa da UC, enquanto administradores podem aceder a estatísticas, relatórios e gráficos de utilização.

## Estrutura do Projeto

O projeto implementado segue o estilo arquitetónico MVC (Model-View-Controller)

```
├── interfaces/
│   ├── icontroller.py
│   ├── ieventlistener.py
│   ├── imodel.py
│   └── iview.py
├── model/
│   ├── dados_model.py
│   └── consulta_model.py
├── controller/
│   ├── bot_controller.py
│   |── user_controller.py
|   |── user_commands.py
├── view/
│   ├── bot_view.py
│   └── discord_view.py
|── utils/ 
|── dados/
|── estatisticas/
|── logs/   
├── bot.py   
|── requirements.txt          
└── README.md/
  
´´´         

Instalar os requirements:

```
pip install -r requirements.txt

```

## Funcionalidades

### Comandos Básicos
- `!uc` - Informações gerais
- `!competencias` - Competências a desenvolver
- `!roteiro` - Conteúdo programático
- `!metodologia` - Metodologia de ensino
- `!recursos` - Recursos disponíveis
- `!calendario` - Datas importantes
- `!avaliacao` - Método de avaliação
- `!exame` - Informações sobre exames
- `!ia` - Uso de IA na UC
- `!estrutura` - Estrutura da equipa
- `!cartao` - Cartão de aprendizagem

### Comandos de Administrador
- `!relatorio` - Gera relatório de uso
- `!estatisticas` - Mostra estatísticas
- `!historico ` - Histórico de um utilizador

### Comandos de Ajuda
- `!help` - Mostra todos os comandos disponíveis
- `!help <comando>` - Mostra ajuda específica para um comando
- `!ajuda` - Alternativa ao comando help

## Sistema de Logs

O sistema de logs foi implementado para facilitar o debug e monitoramento do bot. Os logs são salvos em:
- Diretório: `./logs/`
- Formato: `chatbot_YYYYMMDD.log`
- Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Rotação: 5MB por arquivo, mantém últimos 5 arquivos

## Configuração

1. Crie um arquivo `.env` com seu token do Discord:
```

DISCORD_TOKEN=seu_token_aqui
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o bot:
```bash
python bot.py
```

## Responsabilidades da Equipe

- **Tester (Rúben)**: Lider do Projeto
- **Model (Duarte)**: Implementação da camada de Model, gestão de dados JSON
- **Controller (Sofia)**: Implementação da camada de Controller, processamento de comandos
- **View (Yuran)**: Interface Discord, comandos e apresentação
- **Tester (Carlos)**: Testes funcionais e validação
=======

