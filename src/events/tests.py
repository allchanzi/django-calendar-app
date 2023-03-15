import datetime

import pytz
from contrib.models import Company
from contrib.models import User
from django.test import Client
from django.test import TestCase
from django.utils import timezone
from events.models import Event
from rooms.models import Room


class EventTestCase(TestCase):
    def setUp(self) -> None:
        Company.objects.create()
        self.user = User.objects.create_user(
            'test_user_1', email='test1@email.dom', password='test1', company=Company.objects.first(),
        )

        Room.objects.create(
            manager=self.user,
            name='test_room_1',
            address='Test Street, 1, TestCity, TestState',
        )

        self.room = Room.objects.get(name='test_room_1')
        self.client = Client()

        self.assertEqual(0, Event.objects.count())

        Event.objects.create(
            owner=self.user,
            name='test_event_1',
            start_time=pytz.utc.localize(datetime.datetime(2022, 12, 1, 20)),
            end_time=pytz.utc.localize(datetime.datetime(2022, 12, 2, 23)),
            location=self.room,
        )

        self.user_1 = User.objects.create_user(
            'test2', email='test2@email.dom', password='test2', company=Company.objects.first(), timezone='MST',
        )
        self.user_2 = User.objects.create_user(
            'test3', email='test3@email.dom', password='test3', company=Company.objects.first(),
        )
        Event.objects.create(
            owner=self.user_1,
            name='test_event_2',
            start_time=timezone.now(),
            end_time=timezone.now(),
            location=self.room,
        )

        self.even_1 = Event.objects.create(
            owner=self.user_2,
            name='test_event_3',
            start_time=pytz.utc.localize(datetime.datetime(2022, 12, 5, 8)),
            end_time=pytz.utc.localize(datetime.datetime(2022, 12, 5, 9)),
            location=self.room,
        )
        self.even_1.participants.add(self.user_1)
        self.even_2 = Event.objects.create(
            owner=self.user_2,
            name='test_event_4',
            start_time=timezone.now(),
            end_time=timezone.now(),
            location=self.room,
        )
        self.even_2.participants.add(self.user_2)

        Room.objects.create(
            manager=self.user_2,
            name='test_room_2',
            address='Test Street, 1, TestCity, TestState',
        )

        self.room_1 = Room.objects.get(name='test_room_2')

        Event.objects.create(
            owner=self.user_2,
            name='test_event_5',
            start_time=timezone.now(),
            end_time=timezone.now(),
            location=self.room_1,
        )

        self.assertEqual(5, Event.objects.count())

    def test_event_endpoint_403(self):
        response = self.client.get('/api/events/')
        self.assertEqual(403, response.status_code)

    def test_list_events_as_room_manager(self) -> None:
        # Owner should see all events in room
        self.client.login(username=self.user.email, password='test1')
        response = self.client.get('/api/events/')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(4, len(response_data))
        self.assertEqual(
            ['test_event_1', 'test_event_2', 'test_event_3', 'test_event_4'],  # whole objects could be compared
            [event['name'] for event in response_data],
        )

    def test_list_events_as_non_room_manager(self) -> None:
        # Non owner should see only events that he organizes, and he attends as participant
        self.client.login(username=self.user_1.email, password='test2')
        response = self.client.get('/api/events/')
        response_data: list = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response_data))
        self.assertEqual(
            ['test_event_2', 'test_event_3'],
            [event['name'] for event in response_data],
        )

    def test_list_event_with_param(self) -> None:
        self.client.login(username=self.user.email, password='test1')
        response = self.client.get('/api/events/?name=test_event_1')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('test_event_1', response_data[0]['name'])

    def test_list_event_with_param_search(self) -> None:
        self.client.login(username=self.user.email, password='test1')
        response = self.client.get('/api/events/?search=test_event_1')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('test_event_1', response_data[0]['name'])

    def test_retrieve_event_as_manager_non_participant(self) -> None:
        self.client.login(username=self.user_1.email, password='test2')
        response = self.client.get('/api/event/?name=test_event_3')
        self.assertEqual(200, response.status_code)
        response_data: dict = response.json()
        self.assertEqual(
            {
                'id': self.room.pk,
                'manager': {'email': 'test1@email.dom'},
                'name': 'test_room_1', 'address': 'Test Street, 1, TestCity, TestState',
            }, response_data['location'],
        )

    def test_retrieve_event_as_non_manager_participant(self) -> None:
        self.client.login(username=self.user_1.email, password='test2')
        response = self.client.get('/api/events/')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(2, len(response_data))
        self.assertEqual(
            ['test_event_2', 'test_event_3'],
            [event['name'] for event in response_data],
        )

    def test_retrieve_event_as_non_manager_non_participant(self) -> None:
        self.client.login(username=self.user_1.email, password='test2')
        response = self.client.get('/api/events/')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(2, len(response_data))
        self.assertEqual(
            ['test_event_2', 'test_event_3'],
            [event['name'] for event in response_data],
        )

    def test_retrieve_by_day(self):
        self.client.login(username=self.user.email, password='test1')
        response = self.client.get('/api/events/?day=2022-12-1')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('test_event_1', response_data[0]['name'])

        self.client.login(username=self.user_2.email, password='test3')
        response = self.client.get('/api/events/?day=2022-12-1')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(0, len(response_data))

    def test_retrieve_by_location(self):
        self.client.login(username=self.user_2.email, password='test3')
        response = self.client.get(f'/api/events/?location_id={self.room_1.pk}')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('test_event_5', response_data[0]['name'])

        self.client.login(username=self.user.email, password='test1')
        response = self.client.get(f'/api/events/?location_id={self.room_1.pk}')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(0, len(response_data))

        self.client.login(username=self.user.email, password='test1')
        response = self.client.get(f'/api/events/?location_id={self.room.pk}')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(4, len(response_data))
        self.assertEqual(
            ['test_event_1', 'test_event_2', 'test_event_3', 'test_event_4'],
            [event['name'] for event in response_data],
        )

    def test_default_timezone(self):
        self.client.login(username=self.user_1.email, password='test2')
        response = self.client.get('/api/events/?name=test_event_3')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('2022-12-05T01:00:00-07:00', response_data[0]['start_time'])  # MST

        self.client.login(username=self.user_2.email, password='test3')
        response = self.client.get('/api/events/?name=test_event_3')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('2022-12-05T08:00:00Z', response_data[0]['start_time'])  # UTC

    def test_timezone(self):
        self.client.login(username=self.user_1.email, password='test2')
        response = self.client.get('/api/events/?name=test_event_3', django_timezone='UTC')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('2022-12-05T08:00:00Z', response_data[0]['start_time'])  # UTC instead of default MST

        self.client.login(username=self.user_2.email, password='test3')
        response = self.client.get('/api/events/?name=test_event_3', django_timezone='MST')
        self.assertEqual(200, response.status_code)
        response_data: list = response.json()
        self.assertEqual(1, len(response_data))
        self.assertEqual('2022-12-05T01:00:00-07:00', response_data[0]['start_time'])  # MST instead of default UTC

    def test_create_event_duration_exceeded(self):
        self.client.login(username=self.user.email, password='test1')
        response = self.client.post(
            '/api/create-event/', data={
                'owner': 1,
                'name': 'test_event_6',
                'agenda': 'sprint',
                'start_time': pytz.utc.localize(datetime.datetime(2022, 12, 1, 8)),
                'end_time': pytz.utc.localize(datetime.datetime(2022, 12, 1, 18)),
                'location': self.room.pk,
            }, format='json',
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual({'non_field_errors': ['Maximal allowed duration is 8 hours']}, response.json())
        self.assertEqual(5, Event.objects.count())

    def test_create_event(self):
        self.client.login(username=self.user.email, password='test1')
        response = self.client.post(
            '/api/create-event/', data={
                'owner': self.user.pk,
                'name': 'test_event_6',
                'agenda': 'sprint',
                'start_time': pytz.utc.localize(datetime.datetime(2022, 12, 1, 22)),
                'end_time': pytz.utc.localize(datetime.datetime(2022, 12, 2, 6)),
                'location': self.room.pk,
            }, format='json',
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(6, Event.objects.count())
        self.assertIsNotNone(Event.objects.get(name='test_event_6'))
