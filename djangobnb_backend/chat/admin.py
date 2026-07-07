from django.contrib import admin

# Register your models here.

from .models import ConversationMessage,Conversation

admin.site.register(Conversation)
admin.site.register(ConversationMessage)