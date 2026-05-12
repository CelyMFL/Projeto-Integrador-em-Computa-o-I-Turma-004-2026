from app import create_app, db
from app.models.user import User, RoleEnum
from app.models.task import Task
from app.models.checklist import Checklist, TipoEnum
from app.models.professor_trilha import ProfessorTrilha, StatusEnum
from app.models.professor_checklist import ProfessorChecklist
from app.models.feedback import Feedback
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    # Remover dados existentes
    db.drop_all()
    db.create_all()

    print("Iniciando a criação de dados...")

    # 1. Criação de Usuários
    admin = User(
        nome="Administrador Geral",
        email="admin@test.com",
        senha=generate_password_hash("123"),
        role=RoleEnum.ADMIN
    )
    db.session.add(admin)

    professores = []
    # Professor padrão para testes
    prof_teste = User(
        nome="Professor Teste",
        email="prof@test.com",
        senha=generate_password_hash("123"),
        role=RoleEnum.PROFESSOR
    )
    professores.append(prof_teste)
    db.session.add(prof_teste)

    nomes_prof = ["Ricardo Silva", "Ana Paula", "João Mendes", "Maria Souza", "Carlos Oliveira"]
    for nome in nomes_prof:
        email = f"{nome.lower().replace(' ', '.')}@email.com"
        p = User(
            nome=nome,
            email=email,
            senha=generate_password_hash("123"),
            role=RoleEnum.PROFESSOR
        )
        professores.append(p)
        db.session.add(p)
    
    db.session.commit()

    # 2. Criação de Trilhas (Checklists)
    trilha_pedagogica = Checklist(
        nome="Trilha Pedagógica",
        descricao="Orientações sobre práticas pedagógicas, critérios de avaliação e rotina em sala.",
        tipo=TipoEnum.PEDAGOGICA,
        obrigatoria=True
    )
    trilha_institucional = Checklist(
        nome="Trilha Institucional",
        descricao="Normas, calendário, canais internos e funcionamento geral da instituição.",
        tipo=TipoEnum.INSTITUCIONAL,
        obrigatoria=True
    )
    trilha_tecnologica = Checklist(
        nome="Trilha Tecnológica",
        descricao="Acesso aos sistemas acadêmicos e ferramentas digitais.",
        tipo=TipoEnum.TECNOLOGICA,
        obrigatoria=False
    )
    trilha_softskills = Checklist(
        nome="Comunicação Assertiva",
        descricao="Desenvolvimento de habilidades interpessoais para líderes e docentes.",
        tipo=TipoEnum.PEDAGOGICA,
        obrigatoria=False
    )
    trilha_azure = Checklist(
        nome="Introdução ao Azure",
        descricao="Fundamentos de nuvem e arquitetura para projetos educacionais.",
        tipo=TipoEnum.TECNOLOGICA,
        obrigatoria=False
    )

    trilhas = [trilha_pedagogica, trilha_institucional, trilha_tecnologica, trilha_softskills, trilha_azure]
    db.session.add_all(trilhas)
    db.session.commit()

    # 3. Criação de Tarefas
    all_tasks = []
    
    # Tarefas Pedagógicas
    for i in range(1, 6):
        all_tasks.append(Task(descricao=f"Atividade Pedagógica {i}", ordem=i, checklist_id=trilha_pedagogica.id))
    
    # Tarefas Institucionais
    for i in range(1, 5):
        all_tasks.append(Task(descricao=f"Norma Institucional {i}", ordem=i, checklist_id=trilha_institucional.id))

    # Tarefas Tecnológicas
    for i in range(1, 4):
        all_tasks.append(Task(descricao=f"Ferramenta Digital {i}", ordem=i, checklist_id=trilha_tecnologica.id))

    # Tarefas Azure
    for i in range(1, 4):
        all_tasks.append(Task(descricao=f"Módulo Azure {i}", ordem=i, checklist_id=trilha_azure.id))

    db.session.add_all(all_tasks)
    db.session.commit()

    # 4. Inscrições e Progresso
    # Professor de Teste (prof@test.com): Progresso inicial
    for t in [trilha_pedagogica, trilha_institucional]:
        db.session.add(ProfessorTrilha(professor_id=prof_teste.id, trilha_id=t.id, status=StatusEnum.EM_ANDAMENTO))
    db.session.add(ProfessorTrilha(professor_id=prof_teste.id, trilha_id=trilha_tecnologica.id, status=StatusEnum.NAO_INICIADO))
    
    # Ricardo Silva (professores[1]): Quase terminando tudo
    for t in [trilha_pedagogica, trilha_institucional, trilha_tecnologica]:
        db.session.add(ProfessorTrilha(professor_id=professores[1].id, trilha_id=t.id, status=StatusEnum.EM_ANDAMENTO))
    
    # Ana Paula (professores[2]): Concluiu uma e começou outra
    db.session.add(ProfessorTrilha(professor_id=professores[2].id, trilha_id=trilha_pedagogica.id, status=StatusEnum.CONCLUIDO))
    db.session.add(ProfessorTrilha(professor_id=professores[2].id, trilha_id=trilha_azure.id, status=StatusEnum.EM_ANDAMENTO))

    # João Mendes (professores[3]): Só começou a institucional
    db.session.add(ProfessorTrilha(professor_id=professores[3].id, trilha_id=trilha_institucional.id, status=StatusEnum.EM_ANDAMENTO))

    db.session.commit()

    # 5. Conclusões de Tarefas (ProfessorChecklist)
    ped_tasks = [tk for tk in all_tasks if tk.checklist_id == trilha_pedagogica.id]
    inst_tasks = [tk for tk in all_tasks if tk.checklist_id == trilha_institucional.id]

    # Professor de Teste concluiu algumas
    db.session.add(ProfessorChecklist(professor_id=prof_teste.id, task_id=ped_tasks[0].id, concluido=True))
    db.session.add(ProfessorChecklist(professor_id=prof_teste.id, task_id=ped_tasks[1].id, concluido=True))
    db.session.add(ProfessorChecklist(professor_id=prof_teste.id, task_id=inst_tasks[0].id, concluido=True))

    # Ricardo concluiu quase todas as pedagógicas
    for tk in ped_tasks[:4]:
        db.session.add(ProfessorChecklist(professor_id=professores[1].id, task_id=tk.id, concluido=True))
    
    # Ana Paula concluiu todas as pedagógicas (já que o status da trilha é CONCLUIDO)
    for tk in ped_tasks:
        db.session.add(ProfessorChecklist(professor_id=professores[2].id, task_id=tk.id, concluido=True))

    # 6. Feedbacks
    feedbacks = [
        Feedback(professor_id=professores[1].id, trilha_id=trilha_azure.id, comentario="A trilha de Azure me ajudou muito a entender a migração de servidores."),
        Feedback(professor_id=professores[2].id, trilha_id=trilha_pedagogica.id, comentario="Excelente material de apoio nas atividades pedagógicas."),
        Feedback(professor_id=professores[5].id, trilha_id=None, comentario="Gostaria de sugerir mais trilhas sobre Inteligência Artificial.")
    ]
    db.session.add_all(feedbacks)
    
    db.session.commit()

    print("Banco de dados populado com sucesso!")
