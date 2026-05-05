from app.models import Feedback, User, Checklist
from app import db
from datetime import datetime


class FeedbackService:
    """Service for feedback submissions and management."""

    @staticmethod
    def submit_feedback(professor_id, comentario, trilha_id=None):
        """
        Submit feedback from a professor.
        
        Args:
            professor_id: Professor user ID
            comentario: Feedback text
            trilha_id: Optional trilha ID (if feedback is about specific trilha)
            
        Returns:
            Feedback object or raises ValueError
        """
        # Validation
        professor = User.query.get(professor_id)
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        
        if not comentario or not comentario.strip():
            raise ValueError("Comentario cannot be empty")
        
        # Trim comentario
        comentario = comentario.strip()
        
        # Check trilha exists if provided
        if trilha_id is not None:
            trilha = Checklist.query.get(trilha_id)
            if not trilha:
                raise ValueError(f"Trilha with ID {trilha_id} not found")
        
        try:
            feedback = Feedback(
                professor_id=professor_id,
                trilha_id=trilha_id,
                comentario=comentario,
                data_envio=datetime.utcnow()
            )
            db.session.add(feedback)
            db.session.commit()
            return feedback
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error submitting feedback: {str(e)}")

    @staticmethod
    def get_feedback(feedback_id):
        """Get feedback by ID."""
        return Feedback.query.get(feedback_id)

    @staticmethod
    def get_professor_feedback(professor_id):
        """Get all feedback submitted by a professor."""
        professor = User.query.get(professor_id)
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        
        return Feedback.query.filter_by(professor_id=professor_id).order_by(
            Feedback.data_envio.desc()
        ).all()

    @staticmethod
    def get_trilha_feedback(trilha_id):
        """Get all feedback for a specific trilha."""
        trilha = Checklist.query.get(trilha_id)
        if not trilha:
            raise ValueError(f"Trilha with ID {trilha_id} not found")
        
        return Feedback.query.filter_by(trilha_id=trilha_id).order_by(
            Feedback.data_envio.desc()
        ).all()

    @staticmethod
    def get_all_feedback():
        """Get all feedback (admin view)."""
        return Feedback.query.order_by(Feedback.data_envio.desc()).all()

    @staticmethod
    def get_general_feedback():
        """Get feedback without specific trilha (general feedback)."""
        return Feedback.query.filter(Feedback.trilha_id == None).order_by(
            Feedback.data_envio.desc()
        ).all()

    @staticmethod
    def get_feedback_by_date_range(start_date, end_date):
        """Get feedback submitted within a date range."""
        return Feedback.query.filter(
            Feedback.data_envio >= start_date,
            Feedback.data_envio <= end_date
        ).order_by(Feedback.data_envio.desc()).all()

    @staticmethod
    def update_feedback(feedback_id, comentario=None):
        """
        Update feedback comment.
        
        Args:
            feedback_id: Feedback ID
            comentario: New comment text
            
        Returns:
            Updated Feedback or raises ValueError
        """
        feedback = FeedbackService.get_feedback(feedback_id)
        if not feedback:
            raise ValueError(f"Feedback with ID {feedback_id} not found")
        
        if comentario is not None:
            if not comentario or not comentario.strip():
                raise ValueError("Comentario cannot be empty")
            feedback.comentario = comentario.strip()
        
        try:
            db.session.commit()
            return feedback
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating feedback: {str(e)}")

    @staticmethod
    def delete_feedback(feedback_id):
        """Delete feedback."""
        feedback = FeedbackService.get_feedback(feedback_id)
        if not feedback:
            raise ValueError(f"Feedback with ID {feedback_id} not found")
        
        try:
            db.session.delete(feedback)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error deleting feedback: {str(e)}")

    @staticmethod
    def get_trilha_feedback_count(trilha_id):
        """Get count of feedbacks for a trilha."""
        trilha = Checklist.query.get(trilha_id)
        if not trilha:
            raise ValueError(f"Trilha with ID {trilha_id} not found")
        
        return Feedback.query.filter_by(trilha_id=trilha_id).count()

    @staticmethod
    def get_professor_feedback_count(professor_id):
        """Get count of feedbacks submitted by professor."""
        professor = User.query.get(professor_id)
        if not professor:
            raise ValueError(f"Professor with ID {professor_id} not found")
        
        return Feedback.query.filter_by(professor_id=professor_id).count()
