from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from .models import  Message
from django.contrib.auth.models import User


# @login_required
# def chat(request, username):
#     return render(request, 'chat/chat.html', {
#         'room_name': username
#     })


def chat(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(sender=request.user, recipient=friend) | Message.objects.filter(sender=friend, recipient=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'chat/chat.html', {'friend': friend, 'messages': messages})
