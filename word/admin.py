from django.contrib import admin
from .models import Word, Description, Sound, Form, Example, Phrase


class SoundInline(admin.TabularInline):
    model = Sound
    extra = 2


class DescriptionInline(admin.TabularInline):
    model = Description
    ordering = ['part_of_speech']
 

class FormInline(admin.TabularInline):
    model = Form


class PhraseInline(admin.TabularInline):
    model = Phrase


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'rank')
    inlines = [SoundInline, DescriptionInline, FormInline, PhraseInline]


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('example', 'translate')
    raw_id_fields = ['words']


@admin.register(Description)
class WordDescriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Sound)
class SoundAdmin(admin.ModelAdmin):
    pass


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    pass