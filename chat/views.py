from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def chat(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })
