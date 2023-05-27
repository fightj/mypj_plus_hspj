from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, reverse, redirect
from .models import Room, Message
from django.shortcuts import get_object_or_404
from board.models import Board
@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'chat/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    if request.method == 'POST':
        room_pw = request.POST.get('pw')

        room = get_object_or_404(Room, slug=slug)
        if room_pw == room.pw:
            messages = Message.objects.filter(room=room).order_by('-id')[:50][::-1]
            return render(request, 'chat/room.html', {'room': room, 'messages': messages})
        else:
            board = get_object_or_404(Board, chat_room=room)
            return render(request, 'board/board_detail.html', {'board': board, 'room_error': '비밀번호가 올바르지 않습니다.'})
    else:
        room = get_object_or_404(Room, slug=slug)
        messages = Message.objects.filter(room=room).order_by('-id')[:50][::-1]
        return render(request, 'chat/room.html', {'room': room, 'messages': messages})




@login_required
def room_create(request):
    if request.method == "POST":
        room_name = request.POST["room_name"]
        room_slug = request.POST["room_slug"]

        # 중복 체크
        if Room.objects.filter(slug=room_slug).exists():
            return render(request, 'chat/create.html', {'error': 'Slug already exists'})

        room = Room.objects.create(name=room_name, slug=room_slug)
        return redirect(reverse('room', kwargs={'slug': room.slug}))
    else:
        return render(request, 'chat/create.html')



