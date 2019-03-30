from django.shortcuts import render
import json
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from meetingsite.models import CustomUser
from .models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, 'dispatch')
class RoomView(TemplateView):
    template_name = 'chatengine/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receiver = kwargs['room_name']
        query_receiver = CustomUser.objects.get(username=receiver)
        group_messages = Group.objects.filter(group_name__icontains=receiver)
        context = {
            'receiver': query_receiver,
            'group_messages': group_messages
        }
        return context
