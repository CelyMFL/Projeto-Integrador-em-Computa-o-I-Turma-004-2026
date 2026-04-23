# Projeto Integrador - Backend de Onboarding Docente

Backend Flask para onboarding de professores, com autenticação, trilhas, tarefas e feedback.

Este repositório foi consolidado para manter somente fluxos ativos ou planejados para o produto atual.

## Escopo Atual

Perfis suportados:
- professor
- admin

Fluxos suportados:
- login com sessão
- dashboard do professor
- visualização de trilha e tarefa
- conclusão de tarefa
- envio de feedback do professor
- painel e gestão administrativa (professores, trilhas, tarefas e feedbacks)

## Arquitetura

A aplicação segue camadas:

- routes: endpoints HTTP (contrato consumido pelo front)
- services: regras de negócio
- models: entidades do banco
- database: MySQL

Estrutura principal:

- app/models
- app/services
- app/routes
- app/templates
- app/__init__.py

## Stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLAlchemy
- MySQL
- Docker

## Execução Local

1. Subir banco MySQL:

```bash
docker-compose up -d
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Criar tabelas:

```bash
python create_db.py
```

4. Rodar aplicação:

```bash
python run.py
```

Aplicação em http://localhost:5000.

## Modelo de Dados Ativo

### User
- nome
- email
- senha (hash)
- role: professor | admin

### Checklist (trilha)
- nome
- descricao
- tipo: pedagogica | institucional | tecnologica
- obrigatoria

### Task
- descricao
- ordem
- checklist_id
- material_apoio
- link_apoio
- documento_apoio

### ProfessorTrilha
- professor_id
- trilha_id
- status: nao_iniciado | em_andamento | concluido
- data_inicio
- data_conclusao

### ProfessorChecklist
- professor_id
- task_id
- concluido
- data_conclusao

### Feedback
- professor_id
- trilha_id (opcional)
- comentario
- data_envio

## Rotas e Contratos para Front-end

Todas as rotas abaixo exigem sessão autenticada, exceto login.

### Autenticação

- GET /auth/login
  - Exibe tela de login atual.

- POST /auth/login
  - Form-data: email, senha
  - Redireciona:
    - admin -> /admin/
    - professor -> /professor/dashboard

- GET /auth/logout
  - Encerra sessão.

## Professor - 4 telas

### 1) Dashboard / Minha integração

- GET /professor/dashboard

Retorna:
- user
- trilhas_atribuidas
- progresso_geral
- proximas_tarefas
- trilhas_obrigatorias

### 2) Tela da trilha

- GET /professor/trilhas/<trilha_id>

Retorna:
- dados da trilha
- status da trilha para o professor
- progresso na trilha
- tasks com status individual

### 3) Tela da tarefa

- GET /professor/tarefas/<task_id>

Retorna:
- descricao
- status
- checklist_id
- material_apoio
- link_apoio
- documento_apoio

Marcar concluida/pendente:
- POST /tasks/<task_id>/complete
- POST /tasks/<task_id>/incomplete
- GET /tasks/<task_id>/status

### 4) Feedback

- GET /professor/feedback
  - Contexto para formulário (campos e trilhas disponíveis).

- POST /professor/feedback
  - Body JSON ou form-data:
    - comentario (obrigatorio)
    - trilha_id (opcional)

## Admin - 4 telas

### 1) Painel administrativo

- GET /admin/
  - Renderiza template administrativo mínimo com métricas.

- GET /admin/analytics
  - Retorna métricas em JSON:
    - total_users
    - total_professores
    - total_trilhas
    - total_obrigatorias
    - total_feedbacks
    - trilhas_concluidas
    - trilhas_em_andamento

### 2) Gestão de professores

- GET /admin/professores
  - Lista professores, status, trilhas atribuídas e andamento.

- POST /admin/professores
  - Cria professor.
  - Campos: nome, email, senha.

- PUT/PATCH /admin/professores/<user_id>
  - Edita professor.
  - Campos opcionais: nome, email, senha.

### 3) Gestão de trilhas

- GET /admin/trilhas
  - Lista trilhas (nome, tipo, obrigatória/opcional, descrição, total de tarefas).

CRUD de trilhas e atribuição funcional:
- GET /trilhas/
- POST /trilhas/
- GET /trilhas/<trilha_id>
- PUT/PATCH /trilhas/<trilha_id>
- DELETE /trilhas/<trilha_id>
- POST /trilhas/<trilha_id>/start
- GET /trilhas/<trilha_id>/progress

### 4) Gestão de tarefas / feedbacks

- GET /admin/tarefas-feedbacks
  - Retorna tarefas por trilha e feedbacks enviados.

Gestão de tarefas:
- POST /trilhas/<trilha_id>/tasks
- PUT/PATCH /tasks/<task_id>
- DELETE /tasks/<task_id>
- POST /tasks/trilhas/<trilha_id>/reorder

## Regras de Permissão

- professor:
  - pode acessar rotas /professor
  - pode atualizar status de tarefas em /tasks/<id>/complete|incomplete
  - nao pode acessar rotas /admin

- admin:
  - pode acessar rotas /admin, /trilhas e rotas administrativas de /tasks
  - nao usa rotas de jornada do professor

## Observação de Banco

Se o banco já estava criado antes das últimas mudanças, pode ser necessário atualizar schema para:
- remoção/ajuste de enum antigo de role
- inclusão dos campos de apoio em tasks

O projeto ainda usa create_all (sem migrations automáticas).
