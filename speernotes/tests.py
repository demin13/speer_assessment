import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Note

User = get_user_model()

class NotesAPITestCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('create_user')
        self.login_url = reverse('sign_in')
        self.notes_url = reverse('create_notes')
        self.search_url = reverse('search_notes')

        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
        }
        self.client.post(self.signup_url, data=self.user_data)

        login_data = {
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
        }
        response = self.client.post(self.login_url, data=login_data)
        self.access_token = response.json().get('access_token')
        self.user_id = response.json().get('id')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_note(self):
        data = {'title': 'Test Note', 'content': 'This is a test note.'}
        response = self.client.post(self.notes_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.first().title, 'Test Note')

    def test_create_note_invalid_data(self):
        response = self.client.post(self.notes_url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_get_notes_list(self):
    #     data = {'title': 'Test Note', 'content': 'This is a test note.'}
    #     res = self.client.post(self.notes_url, data=data)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     response = self.client.get(self.notes_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.json()), 1)

    def test_get_single_note(self):
        data = {'title':'Test Note', 'content':'This is a test note.'}
        response_note = self.client.post(self.notes_url, data=data)
        self.assertEqual(response_note.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('get_single_note', kwargs={'id': response_note.json().get('id')}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['title'], 'Test Note')

    # def test_update_note(self):
    #     data = {'title': 'Test Note', 'content': 'This is a test note.'}
    #     res = self.client.post(self.notes_url, data=data)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     data1 = {'title': 'Updated Note'}
    #     response = self.client.put(reverse('update_note', kwargs={'id': res.json().get('id')}), data=data1)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Note.objects.first().title, 'Updated Note')

    def test_delete_note(self):
        data = {'title': 'Test Note', 'content': 'This is a test note.'}
        res = self.client.post(self.notes_url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(reverse('delete_note', kwargs={'id': res.json().get('id')}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_search_notes(self):
        data1 = {'title': 'Test Note', 'content': 'This is a test note.'}
        res1 = self.client.post(self.notes_url, data=data1)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        data2 = {'title': 'Test Note', 'content': 'This is a test note.'}
        res2 = self.client.post(self.notes_url, data=data2)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)