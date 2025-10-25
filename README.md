# Cap 1 — Etapas de uma Máquina Agrícola (Fase 3 — PBL IA FIAP)

**Aluno:** Murilo Salla (RM568041) • **Grupo:** 44

## 🎯 Objetivo
Importar para o **Oracle** (via SQL Developer) os dados coletados na **Fase 2**, documentar o processo (com prints),
executar `SELECT` e publicar tudo num repositório GitHub organizado. (vide enunciado)

## 🗂 Estrutura
- `.github/` automações
- `assets/` imagens/prints
- `config/` configs
- `document/` documentos (relatório)
- `scripts/` utilitários
- `src/` códigos (Python/C++)
- `README.md` guia

## 🔧 Passos resumidos
1) SQL Developer: Host `oracle.fiap.com.br`, Porta `1521`, **SID `ORCL`**, Usuário `RMxxxxx`, Senha `DDMMYY`.  
2) Importar CSV da Fase 2: **Tabelas (Filtrado) → Importar Dados**.  
3) Conferir: `SELECT * FROM NOME_TABELA;` (Ctrl+Enter).

## 📸 Evidências (em `assets/`)
- Conexão criada
- Assistente de importação
- `SELECT *` com dados

## 🗃 Histórico
- 0.1.0 — Estrutura inicial + guia
