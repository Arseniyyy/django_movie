from rest_framework.test import APITestCase
from rest_framework import status

from movies.tests.factories.factories import (create_actor_factory,
                                              create_user_factory)


class ActorTestAPI(APITestCase):
    def setUp(self) -> None:
        self.actor = create_actor_factory()
        self.user = create_user_factory(is_staff=True)

    def test_string_representation(self):
        self.assertEqual(str(self.actor), self.actor.name)

    def test_get_absolute_url(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.actor.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
