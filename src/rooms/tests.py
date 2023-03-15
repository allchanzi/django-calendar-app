from contrib.models import Company
from contrib.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rooms.models import Room


class RoomTestCase(TestCase):
    def setUp(self) -> None:
        Company.objects.create()
        self.user = User.objects.create_user(
            'test_user_1', email='test1@email.dom', password='test1', company=Company.objects.first(),
        )
        self.client = APIClient()

        self.assertEqual(0, Room.objects.count())

        Room.objects.create(
            manager=self.user,
            name='test_room_1',
            address='Test Street, 1, TestCity, TestState',
        )

        self.assertEqual(1, Room.objects.count())
        self.room = Room.objects.first()
        self.assertIsNotNone(self.room)

    def test_list_rooms(self) -> None:
        response = self.client.get('/api/rooms/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [
                {
                    'id': self.room.pk,
                    'manager': {'email': 'test1@email.dom'},
                    'name': 'test_room_1',
                    'address': 'Test Street, 1, TestCity, TestState',
                },
            ], response.json(),
        )

    def test_retrieve_room(self) -> None:
        response = self.client.get(f'/api/room/?pk={self.room.pk}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'id': self.room.pk, 'manager': {'email': 'test1@email.dom'}, 'name': 'test_room_1',
                'address': 'Test Street, 1, TestCity, TestState',
            }, response.json(),
        )

    def test_create_rooms(self) -> None:
        response = self.client.post(
            '/api/create-room/', data={
                'manager': self.user.pk, 'name': 'test_room_2',
                'address': 'Test Street, 2, TestCity, TestState',
            }, format='json',
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, Room.objects.count())
        self.assertIsNotNone(Room.objects.get(name='test_room_2'))
