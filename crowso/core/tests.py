import random
from django.test import SimpleTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import datetime
from core.forms import ProjectCreationForm


class TestFormProject(SimpleTestCase):
    def test_creation_project_form_valid(self):
        upload_file = open('static/assets/image/logo.png', 'rb')
        img = SimpleUploadedFile(upload_file.name, upload_file.read())
        form = ProjectCreationForm(files={'attachment': img, 'picture': img}, data={
            'name': 'a', 'description': 'b', 'value': 20, 'type': 3, 'deadline': datetime.date.today()})
        self.assertTrue(form.is_valid())
        form = ProjectCreationForm(files={'attachment': img, 'picture': img}, data={
            'name': 'a', 'description': 'b', 'value': random.randint(1, 1000), 'type': random.randint(1, 3),
            'deadline': datetime.date.today() - datetime.timedelta(days=random.randint(1, 50))})
        self.assertTrue(form.is_valid())

    def test_creation_project_from_form_invalid(self):
        form = ProjectCreationForm(data={}, files={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)