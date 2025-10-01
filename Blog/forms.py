from django import forms
from Blog.models import Comment, Post, User, Account


class TicketForm(forms.Form):
    SUBJECT_CHOICES = [
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    ]

    name = forms.CharField(max_length=250, required=True, label="", widget=forms.TextInput(attrs={
        'placeholder': "نام و نام خانوادگی",
        'class': 'ticket-form-name  form-field',
    }))
    message = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={
        "placeholder": 'متن پیام',
        'class': 'form-message form-field',
    }))
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={
        'placeholder': 'ایمیل',
        'class': 'ticket-form-email form-field',
    }))
    phone = forms.CharField(required=True, max_length=11, label="", widget=forms.TelInput(attrs={
        'placeholder': 'تلفن همراه',
        'class': 'ticket-form-phone form-field',
    }))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label="موضوع")

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isdigit() and len(phone) != 11 and not phone[0:1] == '09':
                raise forms.ValidationError("شماره تلفن درست نیست!")
            else:
                return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-message form-field',
                'placeholder': 'متن نظر'
            }),
            'name': forms.TextInput(attrs={
                'class': 'comment-form-name form-field',
                'placeholder': 'نام و نام خانوادگی'
            })
        }
        labels = {
            'name': "",
            'body': ''
        }


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول", )
    image2 = forms.ImageField(label="تصویر دوم", )

    class Meta:
        model = Post
        fields = ('title', 'description', 'reading_time', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'عنوان',
                'class': 'form-field post-form--title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'متن پست',
                'class': 'form-field form-message'
            }),
            'reading_time': forms.TextInput(attrs={
                'placeholder': 'زمان مطالعه',
                'class': 'form-field post-form--reading-time'
            }),
            'category': forms.TextInput(attrs={
                'placeholder': 'دسته بندی',
            }),
        }
        labels = {
            'title': '',
            'description': '',
            'reading_time': '',
            'category': '',
        }


class SearchForm(forms.Form):
    query = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={
        'placeholder': 'جستجو',
        'class': ''
    }))


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, required=True, label='', widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(max_length=20, required=True, label='', widget=forms.PasswordInput(attrs={}))

    class Meta:
        model = User
        fields = ('username', "first_name", "last_name", 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("رمز ها مطابقت ندارند")
        else:
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('date_of_birth', 'bio', 'job', 'photo')
