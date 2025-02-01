import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from .models import FAQ
from django.core.cache import cache


@pytest.fixture
def api_client():
    """Fixture for APIClient instance."""
    return APIClient()


@pytest.fixture
def sample_faq(db):
    """Fixture for creating a sample FAQ with translations."""
    FAQ.objects.all().delete()  # Clear previous FAQs to prevent ID conflicts
    return FAQ.objects.create(
        id=1,  # Explicitly set ID to prevent conflicts
        question="What is Django?",
        answer="Django is a high-level Python web framework.",
        question_hi="जांगो क्या है?",
        answer_hi="जांगो एक उच्च-स्तरीय पाइथन वेब फ्रेमवर्क है।",
        question_bn="জ্যাঙ্গো কি?",
        answer_bn="জ্যাঙ্গো একটি উচ্চ-স্তরের পাইথন ওয়েব ফ্রেমওয়ার্ক।",
        question_gu="જાંગો શું છે?",
        answer_gu="જાંગો એક ઉચ્ચ-સ્તરીય પાયથન વેબ ફ્રેમવર્ક છે.",
        question_pa="ਜਾਂਗੋ ਕੀ ਹੈ?",
        answer_pa="ਜਾਂਗੋ ਇੱਕ ਉੱਚ-ਪੱਧਰੀ ਪਾਈਥਨ ਵੈੱਬ ਫਰੇਮਵਰਕ ਹੈ।"
    )


@pytest.mark.django_db
class TestFAQAPI:
    """Test suite for FAQ API endpoints."""

    def setup_method(self):
        """Set up test client and clear cache before each test."""
        self.client = APIClient()
        cache.clear()

    def test_create_faq(self, db):
        """Test creating a new FAQ entry."""
        data = {
            "question": "What is REST?",
            "answer": "REST is an architectural style for APIs"
        }
        response = self.client.post(reverse('faq-list'), data)
        assert response.status_code == status.HTTP_201_CREATED
        assert FAQ.objects.count() == 1
        created_faq = FAQ.objects.first()
        print(created_faq)
        assert created_faq.question == data['question']
        assert created_faq.answer == data['answer']

    def test_get_faq_list(self, db, sample_faq):
        """Test retrieving the list of FAQs."""
        response = self.client.get(reverse('faq-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['question'] == sample_faq.question

    @pytest.mark.parametrize("lang,field_suffix", [
        ('hi', 'hi'),
        ('bn', 'bn'),
        ('gu', 'gu'),
        ('pa', 'pa'),
    ])
    def test_get_faq_translations(self, db, sample_faq, lang, field_suffix):
        """Test FAQ translations for all supported languages."""
        response = self.client.get(f"{reverse('faq-list')}?lang={lang}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['question'] == getattr(
            sample_faq, f'question_{field_suffix}'
        )

    def test_cache_mechanism(self, db, sample_faq):
        """Test caching behavior of FAQ responses."""
        # First request - should cache the result
        response1 = self.client.get(reverse('faq-list'))
        assert response1.status_code == status.HTTP_200_OK

        # Modify the FAQ directly in database
        FAQ.objects.filter(id=sample_faq.id).update(
            question="Modified Question"
        )

        # Second request - should return cached result
        response2 = self.client.get(reverse('faq-list'))
        assert response2.data == response1.data

    def test_unsupported_language_fallback(self, db, sample_faq):
        """Test fallback to English for unsupported languages."""
        # Test with unsupported language code
        response = self.client.get(f"{reverse('faq-list')}?lang=fr")
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['question'] == sample_faq.question

    def test_faq_model_methods(self, db, sample_faq):
        """Test FAQ model methods and properties."""
        # Test string representation
        assert str(sample_faq) == sample_faq.question[:50]

        # Test translation retrieval for all supported languages
        supported_langs = ['hi', 'bn', 'gu', 'pa']
        for lang in supported_langs:
            translated_text = sample_faq.get_translated_text('question', lang)
            assert translated_text == getattr(sample_faq, f'question_{lang}')

    def test_missing_translation_handling(self, db):
        """Test handling of missing translations."""
        # Mock the translator to simulate translation service being unavailable
        with patch('googletrans.Translator.translate', side_effect=Exception('Translation failed')):
            faq = FAQ.objects.create(
                question="Is there a limitation to McDelivery orders?",
                answer="There is no limit..."
            )
            
            response = self.client.get(f"{reverse('faq-list')}?lang=hi")
            assert response.status_code == status.HTTP_200_OK
            assert response.data[0]['question'] == faq.question

    def teardown_method(self):
        """Clean up after each test."""
        FAQ.objects.all().delete()  # Remove all FAQ entries
        cache.clear()
