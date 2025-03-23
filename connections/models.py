from django.db import models
from django.conf import settings


class ConnectionRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pendente'),
        ('Accepted', 'Aceito'),
        ('Rejected', 'Rejeitado'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name = 'sent_requests',
        on_delete = models.CASCADE,
        limit_choices_to = {'user_type': 'student'}
    )

    advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name = 'received_requests',
        on_delete = models.CASCADE,
        limit_choices_to = {'user_type': 'advisor'}
    )
    
    message = models.TextField(help_text='Mensagem enviada pelo estudante')
    response_message = models.TextField(null=True, blank=True, help_text='Resposta do orientador')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Solicitação de {self.student.username} para {self.advisor.username}'