from rest_framework import viewsets
from rest_framework.response import Response
from .models import FAQ
from .serializers import FAQSerializer
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.decorators.cache import cache_page

# Create your views here.
class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    @method_decorator(cache_page(60 * 15))  # 15 minutes
    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')

        if lang not in settings.AVAILABLE_LANGUAGES:
            lang = settings.DEFAULT_LANGUAGE

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'lang': lang})
        return Response(serializer.data)