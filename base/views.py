from rest_framework import viewsets
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.decorators.cache import cache_page

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @method_decorator(cache_page(60 * 15))  # 15 minutes
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        
        if not hasattr(settings, 'AVAILABLE_LANGUAGES'):
            settings.AVAILABLE_LANGUAGES = ['en', 'hi', 'bn', 'gu', 'pa']
            settings.DEFAULT_LANGUAGE = 'en'

        if lang not in settings.AVAILABLE_LANGUAGES:
            lang = settings.DEFAULT_LANGUAGE

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'lang': lang})
        response_data = serializer.data
        
        for item in response_data:
            item['question'] = item.pop('displayed_question')
            item['answer'] = item.pop('displayed_answer')
        
        return Response(response_data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        instance = serializer.instance
        response_serializer = self.get_serializer(instance)
        response_data = response_serializer.data
        
        response_data['question'] = response_data.pop('displayed_question')
        response_data['answer'] = response_data.pop('displayed_answer')
        
        return Response(response_data, status=201)