from django import forms


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=15, required=True)


class CheckLoginForm(forms.Form):
    phone = forms.CharField(max_length=15, required=True)


class GetMessagesForm(forms.Form):
    phone = forms.CharField(max_length=15, required=True)
    uname = forms.CharField(max_length=100, required=True)


class SendMessageForm(forms.Form):
    message_text = forms.CharField(max_length=255, required=True)
    from_phone = forms.CharField(max_length=15, required=True)
    username = forms.CharField(max_length=100, required=True)
