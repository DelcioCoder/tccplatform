from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Message

User = get_user_model()



class MessageAPITestCase(APITestCase):
    def setUp(self):
        # Criar usuários para teste
        self.user1 = User.objects.create_user(
            username = 'user1',
            email='user1@test.com',
            password='testpass123',
            user_type='student'
        )
        self.user2 = User.objects.create_user(
            username = 'user2',
            email='user2@test.com', 
            password='testpass123',
            user_type='advisor'
        )
        
        # Criar uma mensagem de teste
        self.message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content="Mensagem de teste"
        )

    def test_list_messages(self):
        # Autenticar usuário
        self.client.force_authenticate(user=self.user1)
        
        # Fazer requisição GET para listar mensagens
        response = self.client.get('/api/chat/')
        
        # Verificar se a resposta foi bem sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se retornou a mensagem criada
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], "Mensagem de teste")

    def test_create_message(self):
        # Autenticar usuário
        self.client.force_authenticate(user=self.user1)
        
        # Dados da nova mensagem
        data = {
            'recipient': self.user2.id,
            'content': 'Nova mensagem de teste'
        }
        
        # Fazer requisição POST para criar mensagem
        response = self.client.post('/api/chat/', data)
        
        # Verificar se a mensagem foi criada com sucesso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Nova mensagem de teste')
        
        # Verificar se a mensagem foi salva no banco
        self.assertEqual(Message.objects.count(), 2)

    def test_unauthorized_access(self):
        # Tentar acessar sem autenticação
        response = self.client.get('/api/chat/')
        
        # Verificar se o acesso foi negado
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
