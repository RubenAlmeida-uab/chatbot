# Chatbot MVC com Bot do Discord


Este é um chatbot Discord implementado usando o padrão MVC (Model-View-Controller). Foi desenvolvido para responder às dúvidas/questões dos estudantes face à UC de Laboratório de Desenvolvimento de Software.

**Versões de python e pip configurados onde este bot foi desenvolvido**:
- python v.3.12.3
- pip v.24.0


## Estrutura do Projeto

```
.
├── bot.py              # Arquivo principal do bot
├── requirements.txt    # Requirements necessários ao bom funcionamento do projeto
├── controller/         # Camada de Controller
├── model/              # Camada de Model
├── view/               # Camada de View
├── interfaces/         # Camada de interfaces 
├── utils/              # Utilitários ( Validação conta admin, gestão de logs e exportação de estatisticas )
├── dados/              # Dados do chatbot
│   └── puc/            # Informações da UC
└── logs/               # Logs do sistema ( Apenas criado quando o bot arranca )
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
- `!historico` - Histórico de um utilizador
- `!grafico_comandos` - Gera um gráfico dos comandos mais utilizados
- `!grafico_seccoes` - Gera um gráfico das secções mais consultadas
- `!gerar_relatorio` - Gera um relatório em PDF com estatísticas e gráficos

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

Crie um arquivo `.env` com:
```
DISCORD_TOKEN=seu_token_aqui
DISCORD_GUILD=
ADMIN_IDS= # Definir os IDS dos administradores
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o bot:
```bash
python -m bot 
# ou 
python bot.py
```

## Responsabilidades da Equipe

- **Tester (Rúben)**: Lider do Projeto
- **Model (Duarte)**: Implementação da camada de Model, gestão de dados JSON
- **Controller (Sofia)**: Implementação da camada de Controller, processamento de comandos
- **View (Yuran)**: Interface Discord, comandos e apresentação
- **Tester (Carlos)**: Testes funcionais e validação
