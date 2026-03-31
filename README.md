# Projeto Integrador - Aplicação Flask + MySQL

## 📌 Descrição

Este projeto é uma aplicação backend desenvolvida com Flask, utilizando banco de dados MySQL e executada em ambiente containerizado com Docker.

O objetivo é estruturar uma aplicação seguindo boas práticas de arquitetura, separando responsabilidades entre camadas como rotas, serviços, modelos e templates.

---

## 🏗️ Arquitetura do Projeto

A aplicação segue uma arquitetura em camadas:

```
routes (camada HTTP)
   ↓
services (regras de negócio)
   ↓
models (entidades / banco de dados)
   ↓
database (MySQL)
```

### 📁 Estrutura de pastas

```
app/
 ├── models/        # Definição das entidades do banco
 ├── services/      # Regras de negócio
 ├── routes/        # Endpoints da API
 ├── templates/     # Templates HTML (renderização)
 └── __init__.py    # Inicialização do app
```

---

## ⚙️ Tecnologias utilizadas

- Python
- Flask
- SQLAlchemy
- MySQL
- Docker

---

## 🧠 Conceitos aplicados

### Models

Responsáveis por representar as tabelas do banco de dados utilizando SQLAlchemy.

### Services

Camada responsável pelas regras de negócio da aplicação. Centraliza a lógica e evita acoplamento com as rotas.

### Routes

Responsáveis por expor a API HTTP e receber requisições.

### Templates

Responsáveis pela renderização de páginas HTML utilizando o mecanismo de templates do Flask.

---

## 🚀 Como executar o projeto

### 1. Subir os containers

```
docker-compose up --build
```

### 2. Acessar a aplicação

A aplicação estará disponível em:

```
http://localhost:5000
```

---

## 🗄️ Banco de dados

O banco de dados é gerenciado via SQLAlchemy.

Para criação inicial das tabelas:

```
from app import db

db.create_all()
```

---

## 📌 Funcionalidades atuais

- Estrutura base do projeto
- Integração com banco MySQL
- Criação de models
- Implementação da camada de services
- Suporte a templates HTML

---

## 📈 Próximos passos

- Implementar rotas (CRUD)
- Adicionar migrations
- Criar validações
- Implementar autenticação

---

## 👨‍💻 Autores

Eric Armendani Gonçalves

Guilherme de Oliveira Ortiz

Heitor Fernando Almeida

Joyce Sarmento de Lima

Kerly Yukie Shoji

Marcely Migliorini Fernandes Luna

Pablo Aciole Vieira

Thiago Lupinaci Cavalcante de Almeida
