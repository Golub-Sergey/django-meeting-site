from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer
from channels.db import database_sync_to_async
from .models import Group
import json
import asyncio

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connection_successfull', event)
        
        await self.send({
            'type': 'websocket.accept'
        })

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        '''
        await asyncio.sleep(5)
        await self.send({
            'type': 'websocket.close'
        })
        await self.send({
            'type': 'websocket.send',
            'text': 'hello world'
        })
        '''

    async def websocket_receive(self, event):
        message = event['text']
        handled_message = json.loads(message)
        username = str(self.scope['user'])

        await self.create_group(group_name=self.room_group_name, 
            username=username, text=handled_message['message'])

        message_send = {
            'message': handled_message,
            'username': username
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': json.dumps(message_send)
            }
        )
    
    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def create_group(self, group_name, username, text):
        Group.objects.create(group_name=group_name, username=username, text=text)
