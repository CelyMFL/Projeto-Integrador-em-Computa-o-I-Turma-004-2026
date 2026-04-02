from app.models import Task, Checklist
from app import db


class TaskService:
    """Service for task management."""

    @staticmethod
    def create_task(checklist_id, descricao, ordem=None):
        """
        Create a new task in a trilha.
        
        Args:
            checklist_id: Trilha (Checklist) ID
            descricao: Task description
            ordem: Task order (optional, auto-incremented if not provided)
            
        Returns:
            Task object or raises ValueError
        """
        # Validation
        if not descricao or not descricao.strip():
            raise ValueError("Descricao cannot be empty")
        
        trilha = Checklist.query.get(checklist_id)
        if not trilha:
            raise ValueError(f"Trilha with ID {checklist_id} not found")
        
        # Auto-increment ordem if not provided
        if ordem is None:
            max_ordem = db.session.query(db.func.max(Task.ordem)).filter_by(
                checklist_id=checklist_id
            ).scalar() or 0
            ordem = max_ordem + 1
        
        try:
            task = Task(
                descricao=descricao.strip(),
                checklist_id=checklist_id,
                ordem=ordem if ordem else 1
            )
            db.session.add(task)
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating task: {str(e)}")

    @staticmethod
    def get_task(task_id):
        """Get task by ID."""
        return Task.query.get(task_id)

    @staticmethod
    def list_tasks_by_trilha(checklist_id):
        """Get all tasks in a trilha, ordered by ordem."""
        trilha = Checklist.query.get(checklist_id)
        if not trilha:
            raise ValueError(f"Trilha with ID {checklist_id} not found")
        
        return Task.query.filter_by(checklist_id=checklist_id).order_by(Task.ordem).all()

    @staticmethod
    def update_task(task_id, descricao=None, ordem=None):
        """
        Update task information.
        
        Args:
            task_id: Task ID
            descricao: New description (optional)
            ordem: New order (optional)
            
        Returns:
            Updated Task or raises ValueError
        """
        task = TaskService.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        if descricao is not None:
            if not descricao or not descricao.strip():
                raise ValueError("Descricao cannot be empty")
            task.descricao = descricao.strip()
        
        if ordem is not None:
            if not isinstance(ordem, int) or ordem < 1:
                raise ValueError("Ordem must be a positive integer")
            task.ordem = ordem
        
        try:
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating task: {str(e)}")

    @staticmethod
    def delete_task(task_id):
        """Delete a task."""
        task = TaskService.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")
        
        try:
            checklist_id = task.checklist_id
            db.session.delete(task)
            
            # Re-order remaining tasks
            remaining_tasks = Task.query.filter_by(checklist_id=checklist_id).order_by(Task.ordem).all()
            for idx, t in enumerate(remaining_tasks, 1):
                t.ordem = idx
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error deleting task: {str(e)}")

    @staticmethod
    def reorder_tasks(checklist_id, task_ids):
        """
        Reorder tasks in a trilha.
        
        Args:
            checklist_id: Trilha ID
            task_ids: List of task IDs in desired order
            
        Returns:
            True or raises ValueError
        """
        trilha = Checklist.query.get(checklist_id)
        if not trilha:
            raise ValueError(f"Trilha with ID {checklist_id} not found")
        
        # Verify all tasks belong to this trilha
        for idx, task_id in enumerate(task_ids, 1):
            task = TaskService.get_task(task_id)
            if not task:
                raise ValueError(f"Task with ID {task_id} not found")
            if task.checklist_id != checklist_id:
                raise ValueError(f"Task {task_id} does not belong to trilha {checklist_id}")
            
            task.ordem = idx
        
        try:
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error reordering tasks: {str(e)}")
