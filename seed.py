from app import create_app, db
from app.models.user import User, RoleEnum
from app.models.task import Task
from app.models.checklist import Checklist, TipoEnum
from app.models.professor_trilha import ProfessorTrilha, StatusEnum
from app.models.professor_checklist import ProfessorChecklist
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Remover dados existentes
    db.drop_all()
    db.create_all()

    # 1. Criação de Usuários
    admin = User(
        nome="Admin Teste",
        email="admin@test.com",
        senha=generate_password_hash("123"),
        role=RoleEnum.ADMIN
    )

    professor = User(
        nome="Professor Teste",
        email="prof@test.com",
        senha=generate_password_hash("123"),
        role=RoleEnum.PROFESSOR
    )

    db.session.add(admin)
    db.session.add(professor)
    db.session.commit()

    # 2. Criação de Trilhas (Checklists)
    trilha_pedagogica = Checklist(
        nome="Trilha Pedagógica",
        descricao="Orientações sobre práticas pedagógicas, critérios de avaliação, planejamento de aulas e rotina em sala.",
        tipo=TipoEnum.PEDAGOGICA,
        obrigatoria=True
    )

    trilha_institucional = Checklist(
        nome="Trilha Institucional",
        descricao="Informações sobre normas, calendário, canais internos, documentos e funcionamento geral da instituição.",
        tipo=TipoEnum.INSTITUCIONAL,
        obrigatoria=True
    )

    trilha_tecnologica = Checklist(
        nome="Trilha Tecnológica",
        descricao="Acesso aos sistemas acadêmicos, plataformas digitais, ambiente virtual e ferramentas utilizadas no dia a dia.",
        tipo=TipoEnum.TECNOLOGICA,
        obrigatoria=False
    )

    db.session.add_all([trilha_pedagogica, trilha_institucional, trilha_tecnologica])
    db.session.commit()

    # 3. Criação de Tarefas
    # Tarefas Pedagógicas
    tarefas_pedagogicas = [
        Task(descricao="Conhecer o plano pedagógico da instituição", ordem=1, checklist_id=trilha_pedagogica.id, material_apoio="Plano Pedagógico Institucional (PPI)", documento_apoio="ppi.pdf"),
        Task(descricao="Conhecer os canais de comunicação com a coordenação", ordem=2, checklist_id=trilha_pedagogica.id),
        Task(descricao="Ler os critérios de avaliação", ordem=3, checklist_id=trilha_pedagogica.id, material_apoio="Manual de critérios de avaliação", documento_apoio="manual.pdf"),
        Task(descricao="Entender a rotina de planejamento de aula", ordem=4, checklist_id=trilha_pedagogica.id),
        Task(descricao="Conhecer o processo de lançamento de notas", ordem=5, checklist_id=trilha_pedagogica.id)
    ]

    # Tarefas Institucionais
    tarefas_institucionais = [
        Task(descricao="Conhecer o calendário acadêmico", ordem=1, checklist_id=trilha_institucional.id),
        Task(descricao="Ler as normas institucionais", ordem=2, checklist_id=trilha_institucional.id),
        Task(descricao="Identificar os setores de apoio (RH, TI, etc)", ordem=3, checklist_id=trilha_institucional.id),
        Task(descricao="Entender os processos de ouvidoria", ordem=4, checklist_id=trilha_institucional.id)
    ]

    # Tarefas Tecnológicas
    tarefas_tecnologicas = [
        Task(descricao="Acessar o sistema acadêmico", ordem=1, checklist_id=trilha_tecnologica.id),
        Task(descricao="Configurar o e-mail institucional", ordem=2, checklist_id=trilha_tecnologica.id),
        Task(descricao="Navegar pelo Ambiente Virtual de Aprendizagem", ordem=3, checklist_id=trilha_tecnologica.id)
    ]

    db.session.add_all(tarefas_pedagogicas + tarefas_institucionais + tarefas_tecnologicas)
    db.session.commit()

    # 4. Associar Professor às Trilhas
    inscricoes = [
        ProfessorTrilha(professor_id=professor.id, trilha_id=trilha_pedagogica.id, status=StatusEnum.EM_ANDAMENTO),
        ProfessorTrilha(professor_id=professor.id, trilha_id=trilha_institucional.id, status=StatusEnum.EM_ANDAMENTO),
        ProfessorTrilha(professor_id=professor.id, trilha_id=trilha_tecnologica.id, status=StatusEnum.NAO_INICIADO)
    ]
    db.session.add_all(inscricoes)
    db.session.commit()

    # 5. Concluir algumas tarefas para o professor
    conclusoes = [
        ProfessorChecklist(professor_id=professor.id, task_id=tarefas_pedagogicas[0].id, concluido=True),
        ProfessorChecklist(professor_id=professor.id, task_id=tarefas_pedagogicas[1].id, concluido=True),
        ProfessorChecklist(professor_id=professor.id, task_id=tarefas_institucionais[0].id, concluido=True)
    ]
    db.session.add_all(conclusoes)
    db.session.commit()

    print("Banco de dados populado com sucesso!")