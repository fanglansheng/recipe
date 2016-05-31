from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from recipe.models import *

# Create your tests here.
class WorkTestCase(TestCase):
    def test_work_operation(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        client = Client()
        client.login(username='test',password='test')

        # add a new work
        self.assertTrue(Work.objects.all().count() == 0)
        file = open('recipe/static/recipe/res/test.jpg','rb');
        image = SimpleUploadedFile(file.name, file.read(), content_type="image/jpeg")
        response = client.post('/post_work', {'user': user, 'bio': 'test', 'img': image})
        self.assertTrue(Work.objects.all().count() == 1)

        # delete a new work
        work_id = Work.objects.all()[0].id
        response = client.post('/delete_work/'+str(work_id))
        print(Work.objects.all())
        self.assertTrue(Work.objects.all().count() == 0)

