# Front-end API Reference

Guia de integração das telas com exemplos reais de payload.

Base URL local: http://localhost:5000

Observações gerais:
- As rotas protegidas exigem sessão autenticada (cookie de login Flask).
- Respostas de erro de permissão usam HTTP 403 com {"error": "Acesso negado"}.
- Respostas de validação geralmente usam HTTP 400 com {"error": "..."}.

## 1) Login

### GET /auth/login
Retorna HTML da tela de login.

### POST /auth/login
Content-Type: application/x-www-form-urlencoded

Campos:
- email
- senha

Comportamento:
- admin redireciona para /admin/
- professor redireciona para /professor/dashboard

## 2) Professor - Dashboard / Minha integração

### GET /professor/dashboard

Exemplo de resposta:

```json
{
  "user": {
    "id": 3,
    "nome": "Professor Teste",
    "email": "prof@test.com",
    "role": "professor"
  },
  "trilhas_atribuidas": [
    {
      "id": 1,
      "nome": "Onboarding Pedagogico",
      "tipo": "pedagogica",
      "descricao": "Primeiros passos pedagógicos",
      "obrigatoria": true,
      "status": "em_andamento",
      "progresso": {
        "total_tarefas": 4,
        "tarefas_concluidas": 2,
        "percentual": 50.0
      },
      "tasks": [
        {
          "id": 10,
          "descricao": "Ler plano de ensino",
          "ordem": 1,
          "status": "concluido",
          "material_apoio": "Guia do professor",
          "link_apoio": "https://escola.local/guias/professor",
          "documento_apoio": "plano-ensino.pdf"
        }
      ]
    }
  ],
  "progresso_geral": {
    "total_tarefas": 8,
    "tarefas_concluidas": 3,
    "percentual": 37.5
  },
  "proximas_tarefas": [
    {
      "task_id": 12,
      "descricao": "Configurar ambiente virtual",
      "trilha_id": 1
    }
  ],
  "trilhas_obrigatorias": [
    {
      "id": 1,
      "nome": "Onboarding Pedagogico",
      "status": "em_andamento"
    }
  ]
}
```

## 3) Professor - Tela da trilha

### GET /professor/trilhas/<trilha_id>

Exemplo:
- GET /professor/trilhas/1

Resposta:

```json
{
  "id": 1,
  "nome": "Onboarding Pedagogico",
  "tipo": "pedagogica",
  "descricao": "Primeiros passos pedagógicos",
  "obrigatoria": true,
  "status": "em_andamento",
  "progresso": {
    "total_tarefas": 4,
    "tarefas_concluidas": 2,
    "percentual": 50.0
  },
  "tasks": [
    {
      "id": 10,
      "descricao": "Ler plano de ensino",
      "ordem": 1,
      "status": "concluido",
      "material_apoio": "Guia do professor",
      "link_apoio": "https://escola.local/guias/professor",
      "documento_apoio": "plano-ensino.pdf"
    }
  ]
}
```

## 4) Professor - Tela da tarefa

### GET /professor/tarefas/<task_id>

Exemplo:
- GET /professor/tarefas/10

Resposta:

```json
{
  "id": 10,
  "descricao": "Ler plano de ensino",
  "status": "concluido",
  "checklist_id": 1,
  "material_apoio": "Guia do professor",
  "link_apoio": "https://escola.local/guias/professor",
  "documento_apoio": "plano-ensino.pdf"
}
```

### Ações de conclusão de tarefa

#### POST /tasks/<task_id>/complete
Resposta:

```json
{
  "message": "Tarefa concluída com sucesso",
  "task_id": 10,
  "concluido": true
}
```

#### POST /tasks/<task_id>/incomplete
Resposta:

```json
{
  "message": "Tarefa marcada como pendente",
  "task_id": 10,
  "concluido": false
}
```

#### GET /tasks/<task_id>/status
Resposta:

```json
{
  "task_id": 10,
  "concluido": true,
  "data_conclusao": "2026-04-23T18:03:47.123456"
}
```

## 5) Professor - Feedback

### GET /professor/feedback

Resposta:

```json
{
  "message": "Formulário de feedback disponível",
  "campos": ["comentario", "trilha_id (opcional)"],
  "trilhas_disponiveis": [
    { "id": 1, "nome": "Onboarding Pedagogico" }
  ]
}
```

### POST /professor/feedback

Body JSON:

```json
{
  "comentario": "A trilha foi clara e bem estruturada.",
  "trilha_id": 1
}
```

Resposta 201:

```json
{
  "id": 7,
  "comentario": "A trilha foi clara e bem estruturada.",
  "trilha_id": 1,
  "data_envio": "2026-04-23T18:10:11.778899"
}
```

## 6) Admin - Painel

### GET /admin/
Retorna HTML do painel administrativo.

### GET /admin/analytics

Resposta:

```json
{
  "total_users": 12,
  "total_professores": 10,
  "total_trilhas": 6,
  "total_obrigatorias": 3,
  "total_feedbacks": 15,
  "trilhas_concluidas": 9,
  "trilhas_em_andamento": 4
}
```

## 7) Admin - Gestão de professores

### GET /admin/professores

Resposta:

```json
[
  {
    "id": 3,
    "nome": "Professor Teste",
    "email": "prof@test.com",
    "status": "em_andamento",
    "trilhas_atribuidas": [
      { "id": 1, "nome": "Onboarding Pedagogico" }
    ],
    "andamento": {
      "total_tarefas": 8,
      "tarefas_concluidas": 3,
      "percentual": 37.5
    }
  }
]
```

### POST /admin/professores

Body JSON:

```json
{
  "nome": "Novo Professor",
  "email": "novo.prof@escola.com",
  "senha": "123456"
}
```

Resposta 201:

```json
{
  "id": 21,
  "nome": "Novo Professor",
  "email": "novo.prof@escola.com",
  "role": "professor"
}
```

### PUT/PATCH /admin/professores/<user_id>

Body JSON (exemplo):

```json
{
  "nome": "Professor Atualizado",
  "email": "atualizado@escola.com"
}
```

## 8) Admin - Gestão de trilhas

### GET /admin/trilhas

Resposta:

```json
[
  {
    "id": 1,
    "nome": "Onboarding Pedagogico",
    "tipo": "pedagogica",
    "obrigatoria": true,
    "descricao": "Primeiros passos pedagógicos",
    "total_tarefas": 4
  }
]
```

### CRUD de trilhas

- GET /trilhas/
- POST /trilhas/
- GET /trilhas/<trilha_id>
- PUT/PATCH /trilhas/<trilha_id>
- DELETE /trilhas/<trilha_id>
- POST /trilhas/<trilha_id>/start
- GET /trilhas/<trilha_id>/progress

## 9) Admin - Gestão de tarefas e feedbacks

### GET /admin/tarefas-feedbacks

Resposta:

```json
{
  "tarefas_por_trilha": [
    {
      "trilha_id": 1,
      "trilha_nome": "Onboarding Pedagogico",
      "tarefas": [
        {
          "id": 10,
          "descricao": "Ler plano de ensino",
          "ordem": 1,
          "material_apoio": "Guia do professor",
          "link_apoio": "https://escola.local/guias/professor",
          "documento_apoio": "plano-ensino.pdf"
        }
      ]
    }
  ],
  "feedbacks": [
    {
      "id": 7,
      "professor_id": 3,
      "trilha_id": 1,
      "comentario": "A trilha foi clara e bem estruturada.",
      "data_envio": "2026-04-23T18:10:11.778899"
    }
  ]
}
```

### Gestão de tarefas

- POST /trilhas/<trilha_id>/tasks
- PUT/PATCH /tasks/<task_id>
- DELETE /tasks/<task_id>
- POST /tasks/trilhas/<trilha_id>/reorder

Exemplo de reorder:

POST /tasks/trilhas/1/reorder

```json
{
  "task_ids": [12, 10, 11]
}
```
