from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db import models
from .models import Message


@login_required
def chat(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    if friend not in request.user.profile.get_friends():
        return redirect('chat:friend_list')

    messages = Message.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=friend)) |
        (models.Q(sender=friend) & models.Q(recipient=request.user))
    ).order_by('timestamp')

    return render(request, 'chat/chat.html', {'friend': friend, 'messages': messages,'room_name': friend.id})
# def room(request, room_name):
#     return render(request, "chat/chat.html", {"room_name": room_name})