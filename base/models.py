# base/models.py
from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def get_translated_text(self, field, lang):
        cache_key = f"faq_{self.id}_{field}_{lang}"
        cached_value = cache.get(cache_key)
        
        if cached_value:
            return cached_value

        if lang == 'en':
            value = getattr(self, field)
        else:
            value = getattr(self, f"{field}_{lang}")
            
            if not value:
                translator = Translator()
                original_text = getattr(self, field)
                translation = translator.translate(original_text, dest=lang)
                value = translation.text
                setattr(self, f"{field}_{lang}", value)
                self.save()

        cache.set(cache_key, value, timeout=86400) #24 hours
        return value

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        
        if is_new:
            super().save(*args, **kwargs)
            translator = Translator()
            
            for lang in ['hi', 'bn']:
                if not getattr(self, f'question_{lang}'):
                    translation = translator.translate(self.question, dest=lang)
                    setattr(self, f'question_{lang}', translation.text)
                
                if not getattr(self, f'answer_{lang}'):
                    translation = translator.translate(self.answer, dest=lang)
                    setattr(self, f'answer_{lang}', translation.text)
        
        super().save(*args, **kwargs)