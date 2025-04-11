from django.urls import path
from .views import GetOrCreateConversationView, MessageListCreateView, ConversationListView


urlpatterns = [
    path('conversations/get_or_create/', GetOrCreateConversationView.as_view(), name='get-or-create-conversation'),
    path('conversations/<int:conversation_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
]
