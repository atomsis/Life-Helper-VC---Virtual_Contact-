from django.shortcuts import render

def chat(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })
