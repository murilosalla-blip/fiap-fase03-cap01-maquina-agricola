# FIAP - Faculdade de Informática e Administração Paulista
## AI Project Document - Módulo 1 - FIAP

---

### Grupo
Murilo Salla (RM568041)

---

## Sumário
1. Introdução  
2. Visão Geral do Projeto  
3. Desenvolvimento do Projeto  
4. Resultados e Avaliações  
5. Conclusões e Trabalhos Futuros  
6. Referências  
7. Anexos  

---

## 1. Introdução

### 1.1 Escopo do Projeto
Este projeto faz parte da **Fase 3 - Colheita de Dados e Insights** do curso de Inteligência Artificial. O foco é aplicar conceitos de **banco de dados relacionais** para organizar e explorar informações coletadas por sensores simulados na Fase 2 (Wokwi/ESP32).  
O setor escolhido é o **agronegócio**, com ênfase no monitoramento de variáveis como umidade, temperatura e condições de irrigação.

### 1.1.1 Contexto da Inteligência Artificial
A Inteligência Artificial aplicada ao **agronegócio** tem impacto direto na produtividade, redução de custos e sustentabilidade. O uso de sensores inteligentes, integrados a sistemas de banco de dados, permite capturar dados em tempo real e gerar insights para decisões mais assertivas, como previsões de irrigação ou otimização de insumos.

### 1.1.2 Descrição da Solução Desenvolvida
A solução consiste em **importar os dados dos sensores simulados (Fase 2)** para um banco de dados **Oracle SQL Developer**, estruturando-os em tabelas e realizando consultas SQL.  
Essa base de dados será o ponto de partida para análises mais avançadas e aplicações de IA em fases futuras.

---

## 2. Visão Geral do Projeto

### 2.1 Objetivos do Projeto
- Estruturar os dados da Fase 2 em um banco Oracle.  
- Validar a integridade da carga de dados.  
- Demonstrar consultas básicas em SQL.  
- Criar um repositório GitHub organizado conforme o template FIAP.  
- Produzir documentação e vídeo de demonstração.  

### 2.2 Público-Alvo
- Professores e tutores da graduação FIAP.  
- Profissionais de IA interessados em aplicações no agronegócio.  
- Grupos acadêmicos que desejam replicar ou expandir a solução.  

### 2.3 Metodologia
- Extração do log gerado pelo Wokwi (fase anterior).  
- Conversão para CSV via script Python.  
- Importação do CSV no Oracle SQL Developer.  
- Criação de tabela relacional e execução de consultas.  
- Registro de prints e documentação no GitHub.  

---

## 3. Desenvolvimento do Projeto

### 3.1 Tecnologias Utilizadas
- **C++ (Arduino/Wokwi)** – simulação do hardware ESP32.  
- **Python** – script `make_csv_from_wokwi_log.py` para conversão do log em CSV.  
- **Oracle SQL Developer** – ferramenta de banco de dados relacional.  
- **GitHub** – versionamento e entrega.  

### 3.2 Modelagem e Algoritmos
Não há modelagem preditiva nesta fase. A modelagem é **estrutural**, ou seja, transformação dos dados brutos em uma tabela SQL relacional.

### 3.3 Treinamento e Teste
- Importação de ~57 registros dos sensores simulados.  
- Testes de consistência com `SELECT *` e contagem de registros.  
- Ajuste de nomes de tabela/colunas para atender restrições do Oracle.  

---

## 4. Resultados e Avaliações

### 4.1 Análise dos Resultados
- Dados carregados corretamente na tabela `SENSORES_FASE2`.  
- Consultas SQL executadas com sucesso.  
- Prints documentam cada etapa (importação, criação de tabela e consultas).  

### 4.2 Feedback dos Usuários
Como se trata de entrega individual (Grupo 44, 1 participante), não há coleta de feedback externo. O resultado foi avaliado pelo próprio autor como **satisfatório e conforme requisitos**.

---

## 5. Conclusões e Trabalhos Futuros
- Objetivos da entrega foram alcançados: dados estruturados em Oracle, documentação organizada e execução validada.  
- Trabalhos futuros:  
  - Conectar o banco a dashboards em Python (Streamlit).  
  - Explorar aprendizado de máquina com a base de produtos agrícolas (fase posterior).  
  - Expandir o escopo para dados reais de sensores em campo.  

---

## 6. Referências
- Documentação oficial FIAP – Fase 3, Capítulo 1.  
- Oracle SQL Developer (https://www.oracle.com/database/sqldeveloper/).  
- PwC – Global AI Jobs Barometer (2025).  

---

## 7. Anexos
- Prints do processo de importação e consultas.  
- Código Python de conversão (`src/make_csv_from_wokwi_log.py`).  
- Código C++ do Wokwi (`src/fase2_reference/Wokwi.ino`).  
