from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError




class Conversation(models.Model):
    """
        Representa uma conversa privada entre um orientador e um estudante.
        Garante que exista somente uma conversa entre um par específico.
    """
    advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "advisor_conversations",
        limit_choices_to = {'user_type': 'advisor'}
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "student_conversations",
        limit_choices_to = {'user_type': 'student'}
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Garante que não existam duas conversas com o mesmo par.
        unique_together = (('advisor', 'student'),)
        ordering = ['-updated_at']



    def __str__(self):
        return f"Conversa: {self.advisor.username} ↔ {self.student.username}"
    
    def clean(self):
        # Validação extra para garantir que os papéis estejam corretos.
        if getattr(self.advisor, 'user_type', None) != 'advisor':
            raise ValidationError("O usuário designado como 'advisor' deve ser um orientador.")
        if getattr(self.student, 'user_type', None) != 'student':
            raise ValidationError("O usuário designado como 'student' deve ser um estudante.")
        
    def save(self, *args, **kwargs):
        self.full_clean() # Executa a validação antes de salvar.
        super().save(*args, **kwargs)
        
    


class Message(models.Model):
    """
        Representa uma mensagem enviada dentro de uma conversa.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete = models.CASCADE,
        related_name = "messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=True)

    class Meta:
        ordering = ['timestamp'] # Mensagem ordenada da mais antiga para para a mais recente
        indexes = [
            # Índice composto para otimizar buscas por conversa  e timestamp
            models.Index(fields=['conversation', 'timestamp'])
        ]



    def __str__(self):
        return f"Mensagem de {self.sender.username} em {self.timestamp}"
    

    def save(self, *args, **kwargs):
        """
        Ao salvar uma nova mensagem, atualiza a data de modificação da conversa associada,
        permitindo identificar a conversa mais recentemente ativa.
        """
        super().save(*args, **kwargs)
        # Atualiza a data da conversa para refletir a atividade mais recente.
        conversation = self.conversation
        conversation.save()
    
    


    
