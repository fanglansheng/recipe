from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from recipe.models import *

# Create your tests here.
class WorkTestCase(TestCase):
    def test_work_operation(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        profile = Profile(owner=user)
        profile.save()

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
        # self.assertTrue(Work.objects.all().count() == 0)

        # add a new work
        file = open('recipe/static/recipe/res/test.jpg','rb');
        image = SimpleUploadedFile(file.name, file.read(), content_type="image/jpeg")
        response = client.post('/post_work', {'user': user, 'bio': 'test', 'img': image})

        # add a comment
        work = Work.objects.all()[0]
        self.assertTrue(WorkComments.objects.all().count() == 0)
        response = client.post('/post_comment/'+str(work.id), {'user': user, 'work': work, 'content': "hahah"})
        self.assertTrue(WorkComments.objects.all().count() == 1)

        #delete a comment
        response = client.post('/delete_work_comment/'+str(work.id))
        self.assertTrue(WorkComments.objects.all().count() == 0)

        #like a work
        self.assertTrue(user.liked_work.all().count() == 0)
        response = client.get('/like_work/'+str(work.id))
        response = client.get('/like_work/'+str(work.id))
        self.assertTrue(user.liked_work.all().count() == 1)
        response = client.get('/unlike_work/'+str(work.id))
        self.assertTrue(user.liked_work.all().count() == 0)


