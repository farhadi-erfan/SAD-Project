from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
import random
from accounts.forms import UserSignupForm


# Create your tests here.

class TestFormProject(TestCase):
    def test_signup_form_valid(self):
        upload_file = open('static/assets/image/banner.jpg', 'rb')
        img = SimpleUploadedFile(upload_file.name, upload_file.read())

        form = UserSignupForm(files={'picture': img}, data={
            'name': 'a', 'username': 'ab', 'email': 'ab@u.ic', 'password1': 'aabbaabb', 'password2': 'aabbaabb',
            'phone_number': '09091234567', 'address': 'b'})
        self.assertTrue(form.is_valid())

        pn = '09' + ''.join(str(random.randint(1, 9)) for i in range(9))
        form = UserSignupForm(files={'picture': img}, data={
            'name': 'a', 'username': 'ab', 'email': 'ab@u.ic', 'password1': 'aabbaabb', 'password2': 'aabbaabb',
            'phone_number': pn, 'address': 'b'})
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        form = UserSignupForm(data={}, files={})
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)

        upload_file = open('static/assets/image/banner.jpg', 'rb')
        img = SimpleUploadedFile(upload_file.name, upload_file.read())
        form = UserSignupForm(files={'picture': img}, data={'password1': 'aabbaabb', 'password2': 'aabbaabb',
            'name': 'a', 'username': 'ab', 'email': 'ab', 'is_requester': False, 'phone_number': '09091234567', 'address': 'b'})
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

        form = UserSignupForm(files={'picture': img}, data={'password1': 'abbbaa2', 'password2': 'abbbaa2',
            'name': 'a', 'username': 'ab', 'email': 'ab@c.ir', 'is_requester': True, 'phone_number': '09091234567', 'address': 'b'})
        print(form.errors)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
