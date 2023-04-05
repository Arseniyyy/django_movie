from rest_framework.test import APITestCase

from movies.tests.factories.factories import create_actor_factory


class ActorTestAPI(APITestCase):
    def test_string_representation(self):
        actor = create_actor_factory()
        self.assertEqual(str(actor), actor.name)
