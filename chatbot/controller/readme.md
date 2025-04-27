# ChatBot

Bot para Discord desenvolvido para fornecer informações sobre a unidade curricular LDS e gerar estatísticas de utilização.

## Controllers Implementados

### 1. UserController

Responsável por gerir as interações dos utilizadores comuns(alunos) com o bot.

#### Atributos:
- `dados_model`: Instância de DadosModel para acesso às secções do PUC
- `consulta_model`: Instância de ConsultaModel para registo de consultas
- Listas de listeners para diferentes tipos de eventos

#### Métodos Principais:

##### Gestão de Eventos:
- `adicionar_listener_comando_processado(listener)`: Adiciona listener para eventos de comando processado
- `adicionar_listener_seccao_acedida(listener)`: Adiciona listener para eventos de acesso a secções
- `adicionar_listener_erro(listener)`: Adiciona listener para eventos de erro
- `remover_listener(listener)`: Remove um listener de todas as listas

##### Notificação de Eventos:
- `_notificar_comando_processado(utilizador_id, utilizador_nome, comando, seccao, sucesso)`: Notifica processamento
- `_notificar_seccao_acedida(utilizador_id, seccao, dados)`: Notifica acesso a secção
- `_notificar_erro(utilizador_id, comando, seccao, mensagem_erro)`: Notifica erro

##### Processamento de Comandos:
- `processar_comando(utilizador_id, utilizador_nome, comando, seccao=None)`: Processa comandos do utilizador
- `obter_resposta(utilizador_id, utilizador_nome, comando, seccao=None)`: Obtém resposta para o comando
- `_formatar_resposta(seccao, dados)`: Formata a resposta com base nos dados
- `_obter_ajuda()`: Retorna mensagem de ajuda com comandos disponíveis

#### Comandos:
- `puc`: Visão geral do Plano da Unidade Curricular
- `ajuda`: Exibe mensagem de ajuda com comandos disponíveis
- `listar_seccoes`: Lista todas as seções disponíveis
- `unidade_curricular`: Descrição detalhada da disciplina

### 2. BotController

Responsável por funções administrativas, como estatísticas e relatórios.

### Funcionalidades:
- Processar comandos do utilizador.
- Obter informações específicas de secções do PUC.
- Listar todas as secções disponíveis.
- Fornecer ajuda com os comandos disponíveis.

#### Atributos:
- `consulta_model`: Instância de ConsultaModel para acesso às estatísticas
- Listas de listeners para diferentes tipos de eventos administrativos

##### Gestão de Eventos:
- `adicionar_listener_estatisticas_acedidas(listener)`: Adiciona listener para acesso a estatísticas
- `adicionar_listener_relatorio_gerado(listener)`: Adiciona listener para geração de relatórios
- `adicionar_listener_grafico_gerado(listener)`: Adiciona listener para geração de gráficos
- `adicionar_listener_erro(listener)`: Adiciona listener para eventos de erro
- `remover_listener(listener)`: Remove um listener de todas as listas

##### Notificação de Eventos:
- `_notificar_estatisticas_acedidas(admin_id, estatisticas)`: Notifica acesso a estatísticas
- `_notificar_relatorio_gerado(admin_id, tipo_relatorio, caminho_ficheiro)`: Notifica geração de relatório
- `_notificar_grafico_gerado(admin_id, tipo_grafico, caminho_ficheiro)`: Notifica geração de gráfico
- `_notificar_erro(admin_id, operacao, mensagem_erro)`: Notifica erro administrativo

##### Processamento de Comandos Administrativos:
- `processar_comando_admin(admin_id, admin_nome, comando, *args)`: Processa comandos administrativos
- `obter_estatisticas(admin_id=None)`: Obtém estatísticas de uso do bot
- `gerar_relatorio(admin_id=None)`: Gera relatório de utilização em formato markdown
- `gerar_grafico_comandos(admin_id=None)`: Gera gráfico dos comandos mais utilizados
- `gerar_grafico_seccoes(admin_id=None)`: Gera gráfico das seções mais consultadas
- `obter_utilizador_historico(utilizador_id, admin_id=None)`: Obtém histórico de um utilizador específico

#### Comandos Administrativos:
- `estatisticas`: Mostra estatísticas gerais de utilização
- `relatorio`: Gera relatório completo em markdown
- `grafico_comandos`: Gera gráfico dos comandos mais populares
- `grafico_seccoes`: Gera gráfico das seções mais consultadas
- `historico_utilizador`: Exibe histórico de consultas de um utilizador específico


## Integração com Model

### Os controllers dependem dos seguintes modelos:
- `DadosModel`: Acede aos dados do PUC 
- `ConsultaModel`: Registaa consultas e gera estatísticas

## Integração com View

### Os controllers comunicam-se com as views através de retorno direto de dados:
- `UserController.processar_comando()`: Retorna respostas formatadas para a view
- `BotController.processar_comando_admin()`: Retorna resultados (estatísticas, ficheiros) para apresentação


## Pré-requisitos

- Python 3.8+
- discord.py
- matplotlib
