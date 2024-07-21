from django.db import models
import requests
from django.core.files.base import ContentFile

PART_OF_SPEECH = [
    ("adjectival", 'adjectival'),
    ('noun', 'noun'),
    ('verb', 'verb'),
    ('alliance', 'alliance'),
    ('adverb', 'adverb'),
    ('pronoun', 'pronoun'),
    ('other', 'other'),
    ('pretext', 'pretext'),
    ('interjection', 'interjection'),
    ('article', 'article'),
    ('irregular verb', 'irregular verb'),
]

def sound_path(instance, filename):
    return f'sounds/{instance.word}/{instance.region}/{filename}'


class Word(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_description = models.CharField(max_length=955, unique=True, blank=True, null=True)
    rank = models.CharField(default='22000', max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['name', 'rank']

    def __str__(self):
        return self.name
    

class Example(models.Model):
    example = models.CharField(max_length=500, unique=True)
    translate = models.CharField(max_length=500)
    words = models.ManyToManyField(Word, related_name='examples', blank=True)

    def __str__(self):
        return self.example
    

class Description(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='descriptions')
    part_of_speech = models.CharField(choices=PART_OF_SPEECH, max_length=200)
    general_meaning = models.CharField(max_length=255, blank=True, null=True)
    deep_meaning = models.CharField(max_length=255, blank=True, null=True)
    translate = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.general_meaning
    

class Sound(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='sounds')
    region = models.CharField(choices=[
        ('UK', 'United Kingdom'),
        ('US', 'United States'),
    ], verbose_name='region', max_length=200)
    transcription = models.CharField(max_length=255, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    sound = models.FileField(upload_to=sound_path, blank=True, null=True)

    def __str__(self):
        return self.region
    
    def save(self, *args, **kwargs):
        if self.link and not self.sound:
            try:
                r = requests.get(self.link, varify=False)
                self.sound.save(self.link.split('/')[-1], ContentFile(r.content), save=False)
            except Exception as e:
                print('Ошибка', e)
        super().save(*args, **kwargs)

class Phrase(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='phrases')
    phrase = models.CharField(max_length=255, blank=True)
    translate = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.phrase
    

class Form(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='forms')
    part_of_speech = models.CharField(choices=PART_OF_SPEECH, max_length=200)
    condition = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=255, blank=True)
