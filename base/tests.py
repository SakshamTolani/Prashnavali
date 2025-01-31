import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import FAQ
from django.core.cache import cache

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_faq():
    return FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework.",
        question_hi="जांगो क्या है?",
        answer_hi="जांगो एक उच्च-स्तरीय पाइथन वेब फ्रेमवर्क है।",
        question_bn="জ্যাঙ্গো কি?",
        answer_bn="জ্যাঙ্গো একটি উচ্চ-স্তরের পাইথন ওয়েব ফ্রেমওয়ার্ক।"
    )

@pytest.mark.django_db
class TestFAQAPI:
    def test_create_faq(self, api_client):
        data = {
            "question": "What is REST?",
            "answer": "REST is an architectural style for APIs"
        }
        response = api_client.post(reverse('faq-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.count() == 1

    def test_get_faq_list(self, api_client, sample_faq):
        response = api_client.get(reverse('faq-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_faq_translated(self, api_client, sample_faq):
        # Test Hindi translation
        response = api_client.get(f"{reverse('faq-list')}?lang=hi")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['question'] == sample_faq.question_hi

        # Test Bengali translation
        response = api_client.get(f"{reverse('faq-list')}?lang=bn")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['question'] == sample_faq.question_bn

    def test_cache_mechanism(self, api_client, sample_faq):
        cache.clear()
        
        # First request should cache the result
        response1 = api_client.get(reverse('faq-list'))
        assert response1.status_code == status.HTTP_200_OK
        
        # Modify the FAQ directly in database
        FAQ.objects.filter(id=sample_faq.id).update(question="Modified Question")
        
        # Second request should return cached result
        response2 = api_client.get(reverse('faq-list'))
        assert response2.data == response1.data

    def teardown_method(self):
        cache.clear()