from django import forms




class ProjectCreationForm(forms.Form):
    name = forms.CharField(required=True, label='نام پروژه')
    description = forms.CharField(required=False, widget=forms.Textarea, label='توضیح')
    target = forms.CharField(required=True, label='هدف')
    pic = forms.ImageField(required=False, label='تصویر پروژه')
    attachment = forms.FileField(required=False, label='ضمیمه')
    project_type = forms.ChoiceField(choices=[("1", "ترجمه یا تایپ"), ("2", "دیگر")], required=True, label='نوع پروژه')
    subtask_num = forms.IntegerField(required=True, label='تعداد زیرپروژه‌ها')
    subtask_fee = forms.IntegerField(required=True, label='قیمت انجام هر زیرپروژه')
    deadline = forms.DateField(required=True, label='ددلاین')
    # needs_revision = forms.BooleanField(required=True, label='آیا زیرپروژه‌ها به بررسی نیاز دارند؟')
    revision_num = forms.IntegerField(required=False, label='تعداد بررسی‌ها')
    revision_fee = forms.IntegerField(required=False, label='قیمت انجام هر بررسی')

