from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            }
        )
    )


class AddNewsForm(forms.Form):
    name = forms.CharField(
        label='Название',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст',
            }
        )
    )
    content = forms.CharField(
        label='Содержание',
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст',
            }
        )
    )
    is_public = forms.BooleanField(
        label='Публичная новость',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class GetNewsForm(forms.Form):
    name = forms.CharField(
        label='Название',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'введите название или его часть',
                'style': 'min-width: 400px',
            }
        )
    )

class YaCalcForm(forms.Form):
    expression = forms.CharField(
        label='Выражение',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите выражение',
                'style': 'min-width: 400px',
            }
        )
    )