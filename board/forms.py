from django import forms
from .models import Board

class BoardForm(forms.Form):
    title = forms.CharField(error_messages={
        'required': '제목을 입력하세요.'
    }, max_length=100, label="게시글 제목")
    contents = forms.CharField(error_messages={
        'required': '내용을 입력하세요.'
    }, widget=forms.Textarea, label="게시글 내용")
    image = forms.ImageField(label='이미지 파일', error_messages={
        'required': '이미지를 첨부해주세요.'
    })
    pw = forms.CharField(max_length=4, label='pw', error_messages={
       'required': '4자리 숫자를 입력해주세요.'
    })

