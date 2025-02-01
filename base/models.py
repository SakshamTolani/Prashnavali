from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    question_hi = models.TextField(blank=True, null=True)
    answer_hi = RichTextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)
    question_gu = models.TextField(blank=True, null=True)
    answer_gu = RichTextField(blank=True, null=True)
    question_pa = models.TextField(blank=True, null=True)
    answer_pa = RichTextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def get_translated_text(self, field, lang):
        if lang == 'en':
            return getattr(self, field)
            
        translated_field = f"{field}_{lang}"
        translated_value = getattr(self, translated_field)
        
        if not translated_value:
            cache_key = f"faq_{self.id}_{field}_{lang}"
            cached_value = cache.get(cache_key)
            
            if cached_value:
                return cached_value
                
            try:
                translator = Translator()
                original_text = getattr(self, field)
                translation = translator.translate(original_text, dest=lang)
                translated_value = translation.text
                setattr(self, translated_field, translated_value)
                self.save(update_fields=[translated_field])
                cache.set(cache_key, translated_value, timeout=86400)  # Cache for 24 hours
            except Exception:
                return getattr(self, field)  # Fallback to original text
                
        return translated_value or getattr(self, field)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        if is_new and not kwargs.get('update_fields'):
            self.translate_all_fields()

    def translate_all_fields(self):
        try:
            translator = Translator()
            languages = ['hi', 'bn', 'gu', 'pa']
            
            for lang in languages:
                for field in ['question', 'answer']:
                    translated_field = f"{field}_{lang}"
                    if not getattr(self, translated_field):
                        original_text = getattr(self, field)
                        translation = translator.translate(original_text, dest=lang)
                        setattr(self, translated_field, translation.text)
            
            self.save(update_fields=[f"{field}_{lang}" for field in ['question', 'answer'] 
                                   for lang in languages])
        except Exception:
            pass 