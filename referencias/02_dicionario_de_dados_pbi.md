# Dicionário de Dados para Power BI
## Modelo Estrela Puro (Views SQL)

Este documento descreve as *views* criadas no SQL Server para uso no Power BI, mantendo a estrutura de modelo estrela.
Cada dimensão e fato é exposta de forma independente, preservando a granularidade e facilitando a criação de relacionamentos no Power BI.

---

## 1. Dimensões

### vw_Dim_Alunos
```sql
CREATE VIEW vw_Alunos AS
SELECT
    a.id_aluno,
    a.nome AS nome_aluno,
    a.idade,
    a.genero,
    a.origem_educacional,
    a.id_turma
FROM Dim_Alunos a;
```
- Contém dados cadastrais do aluno e a referência para a turma.

### vw_Dim_Turmas
```sql
CREATE VIEW vw_Turmas AS
SELECT
    t.id_turma,
    t.nome AS nome_turma,
    t.vestibular
FROM Dim_Turmas t;
```
- Contém informações da turma.

### vw_Dim_Professores
```sql
CREATE VIEW vw_Professores AS
SELECT
    p.id_professor,
    p.nome AS nome_professor
FROM Dim_Professores p;
```
- Contém dados dos professores.

### vw_Dim_Disciplinas
```sql
CREATE VIEW vw_Disciplinas AS
SELECT
    d.id_disciplina,
    d.nome AS nome_disciplina
FROM Dim_Disciplinas d;
```
- Lista as disciplinas.

### vw_Dim_Temas
```sql
CREATE VIEW vw_Temas AS
SELECT
    te.id_tema,
    te.nome AS nome_tema,
    te.grau_dificuldade,
    te.id_disciplina
FROM Dim_Temas te;
```
- Lista os temas de cada disciplina.

### vw_Dim_Questoes
```sql
CREATE VIEW vw_Questoes AS
SELECT
    q.id_questao,
    q.numero_questao,
    q.id_tema,
    q.id_simulado
FROM Dim_Questoes q;
```
- Lista as questões e a que tema/simulado pertencem.

### vw_Dim_Simulados
```sql
CREATE VIEW vw_Simulados AS
SELECT
    s.id_simulado,
    s.nome AS nome_simulado,
    s.semana,
    s.data_aplicacao,
    s.id_tipo,
    ts.descricao AS tipo_simulado,
    s.id_turma
FROM Dim_Simulados s
JOIN Dim_Tipo_Simulado ts ON s.id_tipo = ts.id_tipo;
```
- Lista os simulados aplicados.

---

## 2. Fatos

### vw_Fato_Respostas
```sql
CREATE VIEW vw_Fato_Respostas AS
SELECT
    fr.id_resposta,
    fr.id_aluno,
    fr.id_questao,
    d.id_disciplina,
    fr.acertou
FROM Fato_Respostas fr
JOIN Dim_Questoes q   ON fr.id_questao = q.id_questao
JOIN Dim_Temas te     ON q.id_tema = te.id_tema
JOIN Dim_Disciplinas d ON te.id_disciplina = d.id_disciplina;
```
- Contém cada resposta dada, ligando o aluno à questão e indicando se acertou.

### vw_Fato_Turma_Professor
```sql
CREATE VIEW vw_Rel_Turma_Professor AS
SELECT
    rtp.id_turma,
    rtp.id_professor,
    rtp.id_disciplina,
    rtp.data_inicio,
    rtp.data_fim
FROM Fato_Rel_Turma_Professor rtp;
```
- Relaciona turmas, professores e disciplinas.

---

## Observações
- **Dimensões**: apenas atributos fixos, com join apenas com a tabela simulados e tipo simulados.
- **Fatos**: apenas eventos/relacionamentos, sem atributos descritivos.
- **Relacionamentos**: devem ser criados no Power BI, garantindo granularidade correta e flexibilidade analítica.
