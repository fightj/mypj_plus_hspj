from django.db import models
from django.utils.text import slugify
from accounts.models import User
from board.models import Board
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User)
    room_board = models.OneToOneField(Board, related_name='chat_room', on_delete=models.CASCADE, null=True, blank=True)
    pw = models.CharField(max_length=4)
    # ...


from django.utils.text import slugify

@receiver(post_save, sender=Board)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        slug = slugify(instance.title)
        pw = instance.pw

        print("Creating chat room...")
        print(f"Title: {instance.title}")

        print(f"pw: {instance.pw}")
        # 중복된 slug 값이 있는지 확인
        existing_slugs = Room.objects.filter(slug__startswith=slug)
        if existing_slugs:
            # 중복된 slug 값이 있다면, 가장 큰 숫자를 찾아서 뒤에 붙임
            max_number = max([int(s.slug[len(slug):]) for s in existing_slugs])
            slug = f"{slug}{max_number + 1}"
            print(f"Slug: {slug}")
        room = Room.objects.create(name=f"{instance.title} Room", slug=slug, pw=pw, room_board=instance)
        room.users.add(instance.writer)



class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)