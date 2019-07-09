from django import template

register = template.Library()


@register.filter
def html_placeholder(field, args=None):
    name = field.__str__()
    ph = ''

    if 'email' in name:
        ph = 'ایمیل'
    elif 'username' in name:
        ph = 'نام کاربری'
    elif '"name"' in name:
        ph = 'نام و نام خانوادگی'
    elif '"phone_number"' in name:
        ph = 'تلفن همراه، مانند: 09123456789'
    elif '"address"' in name:
        ph = 'نشانی'
    elif 'password1' in name:
        ph = "گذرواژه"
    elif 'password2' in name:
        ph = "تکرار گذرواژه"


    field.field.widget.attrs.update({"placeholder": ph})
    return field
