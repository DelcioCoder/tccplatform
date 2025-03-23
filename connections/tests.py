from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from connections.models import ConnectionRequest

class ConnectionRequestPermissionTest(APITestCase):
    def setUp(self):
        # Criação de usuários
        self.student = CustomUser.objects.create_user(
            username='student1',
            password='testpass123',
            user_type='student'
        )
        self.advisor = CustomUser.objects.create_user(
            username='advisor1',
            password='testpass123',
            user_type='advisor'
        )
        self.client = APIClient()

    def test_permission_validation(self):
        # Passo 1: Autenticar como orientador e tentar criar uma solicitação (deve falhar)
        self.client.force_authenticate(user=self.advisor)
        create_url = reverse('connection-create')
        data = {
            'advisor': self.advisor.id,
            'message': 'Tentativa inválida'
        }
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Permissão negada

        # Passo 2: Autenticar como estudante e criar uma solicitação
        self.client.force_authenticate(user=self.student)
        data = {
            'advisor': self.advisor.id,
            'message': 'Solicitação válida'
        }
        response = self.client.post(create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        request_id = response.data['id']

        # Passo 3: Autenticar como estudante e tentar responder à solicitação (deve falhar)
        response_url = reverse('connection-response', kwargs={'pk': request_id})
        response_data = {
            'status': 'Accepted',
            'response_message': 'Tentativa inválida'
        }
        response = self.client.patch(response_url, response_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Permissão negada

        # Passo 4: Autenticar como orientador e responder à solicitação
        self.client.force_authenticate(user=self.advisor)
        response = self.client.patch(response_url, response_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar se a solicitação foi atualizada corretamente
        updated_request = ConnectionRequest.objects.get(id=request_id)
        self.assertEqual(updated_request.status, 'Accepted')
        self.assertEqual(updated_request.response_message, 'Tentativa inválida')