import factory
import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api_app.models import Author, Book, Quote, Tag
from config.settings import REST_FRAMEWORK



class RandomAuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    date_of_birth = factory.Faker('date_of_birth')
    nationality = 'Latvian'
    


class TestAuthorsResource(APITestCase):
    fixtures = [
        'authors.json',
        ]
    
    def test_get_request_can_fetch_authors(self):
        response = self.client.get(reverse('list-of-authors'))
        payload = response.json()
        author_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(author_count, 3)

    def test_get_request_can_search_authors_by_full_name_contains(self):
        inputs = ['liam', 'Mill', 'Vyd', ]   # Use substrings from first, middle, and last names
        
        for input_ in inputs:
            url = reverse('list-of-authors')
            query = {'contains': input_}
            response = self.client.get(url, query)
            payload = response.json()
            author_count = len(payload['results'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(author_count, 1)

    def test_get_request_can_fetch_author_by_id(self):
        resource_id = 2
        response = self.client.get(f"{reverse('list-of-authors')}{resource_id}/")
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['id'], resource_id)



class TestBooksResource(APITestCase):
    fixtures = [
        'authors.json',
        'books.json',
        ]

    def test_get_request_can_fetch_books(self):
        response = self.client.get(reverse('list-of-books'))
        payload = response.json()
        book_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_count, 5)

    def test_get_request_can_search_books_by_full_title_contains(self):
        inputs = ['Old Man', 'II', ]   # Use substrings from title and subtitle

        for input_ in inputs:
            url = reverse('list-of-books')
            query = {'contains': input_}
            response = self.client.get(url, query)
            payload = response.json()
            book_count = len(payload['results'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(book_count, 1)

    def test_get_request_can_search_books_by_exact_year(self):
        url = reverse('list-of-books')
        query = {'year': 1940}
        response = self.client.get(url, query)
        payload = response.json()
        book_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_count, 1)

    def test_get_request_can_search_books_by_exact_isbn(self):
        url = reverse('list-of-books')
        query = {'isbn': '0684801221'}
        response = self.client.get(url, query)
        payload = response.json()
        book_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_count, 1)

    def test_get_request_can_search_books_by_author_id(self):
        url = reverse('list-of-books')
        query = {'author': 2}
        response = self.client.get(url, query)
        payload = response.json()
        book_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_count, 3)

    def test_get_request_can_search_books_by_combination_of_params(self):
        url = reverse('list-of-books')
        query = {'author': 2, 'year': 1952}
        response = self.client.get(url, query)
        payload = response.json()
        book_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_count, 1)

    def test_get_request_can_fetch_book_by_id(self):
        resource_id = 5
        response = self.client.get(f"{reverse('list-of-books')}{resource_id}/")
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['id'], resource_id)



class TestQuotesResource(APITestCase):
    fixtures = [
        'authors.json',
        'books.json',
        'quotes.json',
        'tags.json',
        'quote_tags.json',
        ]

    def test_get_request_can_fetch_quotes(self):
        response = self.client.get(reverse('list-of-quotes'))
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 4)

    def test_get_request_can_search_quotes_by_text_contains(self):
        url = reverse('list-of-quotes')
        query = {'contains': 'cat'}
        response = self.client.get(url, query)
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 1)

    @unittest.skip('Test fixtures have no quotes that would contain dates')
    def test_get_request_can_search_quotes_by_exact_year(self):
        raise NotImplementedError

    def test_get_request_can_search_quotes_by_author_id(self):
        url = reverse('list-of-quotes')
        query = {'author': 2}
        response = self.client.get(url, query)
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 2)

    def test_get_request_can_search_quotes_by_book_id(self):
        url = reverse('list-of-quotes')
        query = {'book': 3}
        response = self.client.get(url, query)
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 1)

    def test_get_request_can_search_quotes_by_tag_ids(self):
        url = reverse('list-of-quotes')
        query = {'tags': '3,5'}
        response = self.client.get(url, query)
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 1)

    def test_get_request_can_search_quotes_by_combination_of_params(self):
        url = reverse('list-of-quotes')
        query = {'tags': '3', 'author': 1}
        response = self.client.get(url, query)
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 1)

    def test_get_request_can_fetch_quote_by_id(self):
        resource_id = 2
        response = self.client.get(f"{reverse('list-of-quotes')}{resource_id}/")
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['id'], resource_id)



class TestTagsResource(APITestCase):
    fixtures = ['tags.json', ]

    def test_get_request_can_fetch_tags(self):
        response = self.client.get(reverse('list-of-tags'))
        payload = response.json()
        quote_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(quote_count, 5)

    def test_get_request_can_search_tags_by_name_starts_with(self):
        url = reverse('list-of-tags')
        query = {'starts_with': 'wis'}
        response = self.client.get(url, query)
        payload = response.json()
        tag_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_count, 1)

    def test_get_request_can_search_tags_by_name_contains(self):
        url = reverse('list-of-tags')
        query = {'contains': 'dom'}
        response = self.client.get(url, query)
        payload = response.json()
        tag_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_count, 1)

    def test_get_request_can_search_tags_by_similar_name_of_similarity_lte_2(self):
        url = reverse('list-of-tags')
        query = {'similar_to': 'wise'}
        response = self.client.get(url, query)
        payload = response.json()
        tag_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_count, 1)

    def test_get_request_can_search_tags_by_similar_name_and_skip_tags_of_similarity_gt_3(self):
        url = reverse('list-of-tags')
        query = {'similar_to': 'Danish'}
        response = self.client.get(url, query)
        payload = response.json()
        tag_count = len(payload['results'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(tag_count, 0)

    def test_get_request_can_fetch_tag_by_id(self):
        resource_id = 5
        response = self.client.get(f"{reverse('list-of-tags')}{resource_id}/")
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(payload, dict)
        self.assertEqual(payload['id'], resource_id)



class TestRandomQuotesResource(APITestCase):
    fixtures = [
        'authors.json',
        'books.json',
        'quotes.json',
        'tags.json',
        'quote_tags.json',
        ]

    def test_get_request_can_fetch_random_quote(self):
        response = self.client.get(reverse('random-quote-details'))
        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(payload, dict)
        self.assertIsInstance(payload['id'], int)



class TestPagination(APITestCase):
    ''' Test whether the pagination is enabled. Do not bother to test if
        pagination is working properly as this is a feature of DRF and it should
        have been tested by DRF project.

        Test it with only one resource as the pagination configuration is
        applied globally for all resources. '''
    
    over_page_size = REST_FRAMEWORK['PAGE_SIZE'] + 1   # Set the amount that would result in more that one page of data
    
    def setUp(self):
        for _ in range(self.over_page_size):
            author = RandomAuthorFactory()

    def test_pagination_is_enabled(self):
        page_1 = self.client.get(reverse('list-of-authors')).json()
        page_2 = self.client.get(page_1['next']).json()
        author_count = len(page_1['results']) + len(page_2['results'])
        self.assertEqual(author_count, self.over_page_size)



class TestResourceNotFoundResponse(APITestCase):
    ''' Test whether selected resources respond with custom "404 Not Found"
        message when non-existent resource id is used '''

    fixtures = [
        'authors.json',
        'books.json',
        'quotes.json',
        'tags.json',
        'quote_tags.json',
        ]

    def test_get_request_to_fetch_nonexisting_resource_triggers_404_response(self):
        models = [Author, Book, Quote, Tag]

        for model in models:
            model_class_name = model.__name__.lower()
            url_name = reverse(f'list-of-{model_class_name}s')
            model_ids = model.objects.all().values_list('id', flat=True)
            non_existent_id = sum(model_ids) + 1
            response = self.client.get(f"{url_name}{non_existent_id}/")
            response_payload = response.json()
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertIsInstance(response_payload, dict)
            self.assertIsInstance(response_payload['message'], str)
