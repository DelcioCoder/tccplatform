import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from django.contrib.auth import get_user_model


User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extrai conversation_id da URL 
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'


        # Usuário autenticado(graças ao AuthMiddlewareStack)
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close()
            return 
        

        # Verifica se o usuário faz parte da conversa
        if not await self.user_in_conversation():
            await self.close()
            return
        
        # Adiciona o canal actual ao grupo (para a conversa)
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        # Remove o canal do grupo da conversa
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recebe mensagem do Websocket
        data = json.loads(text_data)
        message_text = data.get('message')

        if message_text:
            # Salva a mensagem no banco de dados
            saved_message = await self.save_message(message_text)


            # Envia a mensagem para todos os participantes da conversa
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": saved_message.content,
                    "sender_username": self.user.username,
                    "timestamp": saved_message.timestamp.isoformat(),
                }
            )
    

    async def chat_message(self, event):
        # Envia a mensagem para o cliente WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_username": event["sender_username"],
            "timestamp": event["timestamp"],
        }))


    @database_sync_to_async
    def user_in_conversation(self):
        """Verifica se o usuário autenticado faz parte da conversa com o ID self.conversation_id."""
        try:
            conv = Conversation.objects.get(id=self.conversation_id)
            return self.user == conv.advisor or self.user == conv.student
        except Conversation.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        """Salva a mensagem no banco de dados e retorna o objeto salvo."""
        conv = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conv,
            sender=self.user,
            content=content
        )


                



