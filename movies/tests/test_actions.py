from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.urls import reverse

from movies.models import Movie
from movies.admin import MovieAdmin
from users.models import CustomUser


class MovieAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        email = 'test@test.com'
        password = '12345'
        admin = MovieAdmin(model=Movie, admin_site=AdminSite())
        super_user = CustomUser.objects.create_superuser(
            email=email, password=password)
        self.client.login(email=super_user.email, password=password)
        self.movie = Movie.objects.create(title='Slumberland',
                                          url='new-url-1',
                                          poster='none',
                                          is_draft=False)
        admin.save_model(obj=self.movie, request=None, form=None, change=None)

    def test_make_draft(self):
        url = reverse('admin:movies_movie_changelist')
        data = {'action': 'make_draft', '_selected_action': [self.movie.pk]}
        self.client.post(url, data, follow=True)
        instance = Movie.objects.get(pk=self.movie.pk)
        self.assertTrue(instance.is_draft)
