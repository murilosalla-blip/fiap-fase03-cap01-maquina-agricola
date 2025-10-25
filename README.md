# FIAP - Faculdade de Informática e Administração Paulista
## Fase 3 - Capítulo 1  
### Etapas de uma Máquina Agrícola

🎥 **Vídeo demonstrativo no YouTube:** [Assista aqui](https://youtu.be/m3aPuPz5YMA)

---

## 👨‍🎓 Integrantes
- Murilo Salla (RM568041)

## 👩‍🏫 Professores
- Tutor(a): Ana Cristina dos Santos  
- Coordenador(a): André Godoi Chiovato  

---

## 📜 Descrição
Este projeto faz parte da **Fase 3 - Colheita de Dados e Insights** do curso de Inteligência Artificial da FIAP.  

O objetivo foi explorar conceitos iniciais de **Banco de Dados Relacional** utilizando o **Oracle SQL Developer**, realizando a importação e manipulação de dados coletados pelos sensores simulados na **Fase 2 (Wokwi/ESP32)**.  

A proposta segue o PBL (Project-Based Learning) em que a startup fictícia **FarmTech Solutions** aplica soluções de Inteligência Artificial no **agronegócio**, uma das áreas mais promissoras do Brasil segundo o *Global AI Jobs Barometer* da PwC (2025).  

**Principais entregas:**  
- Conversão do log da Fase 2 em CSV via Python.  
- Importação dos dados para o Oracle SQL Developer.  
- Criação de tabela relacional e execução de consultas SQL.  
- Documentação estruturada em repositório GitHub conforme template oficial da FIAP.  
- Vídeo demonstrativo do funcionamento (link acima).  

Este trabalho consolida a prática de coleta, organização e análise inicial de dados, preparando terreno para fases futuras de análise avançada e aplicação de Machine Learning.

---

## 📁 Estrutura de pastas
Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- **.github/**: arquivos de configuração específicos do GitHub para relatórios de problemas.  
- **assets/**: arquivos relacionados a elementos não estruturados (imagens/prints do Oracle).  
- **config/**: arquivos de configuração e ajustes do projeto.  
- **document/**: documentação oficial do projeto (inclui o `documentai_project_document_fiap.md`).  
- **document/other/**: documentos complementares e auxiliares.  
- **scripts/**: scripts auxiliares para tarefas específicas (deploy, backups, etc.).  
- **src/**: código-fonte principal do projeto (Python da Fase 3 e referência em C++ da Fase 2).  
- **README.md**: guia geral do projeto (este arquivo).  

---

## 🔧 Como executar o código

### Pré-requisitos
- **Python 3.13+**  
- **Oracle SQL Developer** (configurado com usuário RM e senha padrão FIAP)  
- **Bibliotecas Python**: `pandas`, `os`  

### Passos
1. Baixe o repositório:  
   ```bash
   git clone https://github.com/murilosalla-blip/fiap-fase03-cap01-maquina-agricola
   cd fiap-fase03-cap01-maquina-agricola

2. Converta o log da Fase 2 em CSV (já fornecido em /data):
python src/make_csv_from_wokwi_log.py

3. No Oracle SQL Developer, importe o CSV para uma nova tabela (SENSORES_FASE2).

4. Execute consultas SQL como:
SELECT * FROM SENSORES_FASE2;
SELECT COUNT(*) FROM SENSORES_FASE2;

5. Confira os prints em /assets para acompanhar cada etapa.

🗃 Histórico de lançamentos

1.0.0 - 25/10/2025
Estrutura do template completa, importação no Oracle, README finalizado, vídeo adicionado.