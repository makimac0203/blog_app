from django import forms

from django.core.mail import EmailMessage

from .models import Blog

class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    ruby = forms.CharField(label='フリガナ', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-11'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力して下さい。'
        self.fields['ruby'].widget.attrs['class'] = 'form-control col-11'
        self.fields['ruby'].widget.attrs['placeholder'] = 'フリガナをここに入力して下さい。'
        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力して下さい。'
        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力して下さい。'
        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力して下さい。'

    def send_email(self):
        name = self.cleaned_data['name']
        ruby = self.cleaned_data['ruby']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ{}'.format(title)
        message = '送信者: {0}\nフリガナ: {1}\nメールアドレス: {2}\nタイトル: {3}\nメッセージ:\n{4}'.format(name, ruby, email, title, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'