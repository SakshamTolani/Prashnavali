from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    displayed_question = serializers.SerializerMethodField()
    displayed_answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'displayed_question', 
                 'displayed_answer', 'created_at', 'updated_at']
        read_only_fields = ['displayed_question', 'displayed_answer']

    def get_displayed_question(self, obj):
        lang = self.context.get('lang', 'en')
        return obj.get_translated_text('question', lang)

    def get_displayed_answer(self, obj):
        lang = self.context.get('lang', 'en')
        return obj.get_translated_text('answer', lang)