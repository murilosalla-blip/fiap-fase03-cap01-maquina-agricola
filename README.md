# Cap 1 — Etapas de uma Máquina Agrícola (Fase 3 — PBL IA FIAP)

**Aluno:** Murilo Salla (RM568041)  
**Grupo:** 44

## 🎯 Objetivo da atividade
Importar para o **Oracle** (via SQL Developer) os dados coletados na **Fase 2**, documentar o processo (com prints), executar consultas `SELECT` e publicar tudo em um repositório GitHub organizado. Também será produzido um vídeo de até **5 minutos** demonstrando o funcionamento.  
_Fonte: enunciado oficial da atividade._ :contentReference[oaicite:7]{index=7}

## 🗂 Estrutura do repositório
- `.github/` — automações e relatórios de problemas  
- `assets/` — imagens/prints usados na documentação  
- `config/` — arquivos de configuração  
- `document/` — documentos do projeto (incluir relatório PDF/MD)  
- `scripts/` — scripts auxiliares  
- `src/` — código-fonte (Python ou C/C++)  
- `README.md` — este guia

> A estrutura segue o template FIAP analisado. :contentReference[oaicite:8]{index=8}

## 🔧 Como reproduzir (resumo)
1. Instalar o **Oracle SQL Developer** e criar conexão com:
   - Host: `oracle.fiap.com.br` • Porta: `1521` • SID: `ORCL`
   - Usuário: `RMxxxxx` • Senha: `DDMMYY` (data de nascimento) :contentReference[oaicite:9]{index=9}
2. Importar o arquivo CSV da Fase 2 (menu **Tabelas (Filtrado)** → **Importar Dados**). :contentReference[oaicite:10]{index=10}
3. Verificar com `SELECT * FROM NOME_TABELA;` (Ctrl+Enter). :contentReference[oaicite:11]{index=11}

## 📸 Evidências (subir em `assets/`)
- Print da tela de conexão criada  
- Print do assistente de importação  
- Print do `SELECT *` com dados retornando  
- (opcional) Prints do dashboard/ML, se fizer o “Ir Além” :contentReference[oaicite:12]{index=12}

## 🧪 Scripts/códigos
- Conexão e consulta Oracle via Python (em `src/`)  
- (opcional) Dashboard Streamlit ou Notebook ML conforme “Ir Além” :contentReference[oaicite:13]{index=13}

## 🗃 Histórico de versões
- 0.1.0 — Estrutura inicial + guia
