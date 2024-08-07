from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .services import _get_description, _get_dict_words_with_short_description, _get_form
from .models import Word, Example
from .serializers import WordSerializer, ExampleSerializer

import json


def word_detail(request):
    word_name = request.GET.get('word')
    try:
        word = get_object_or_404(Word, name=word_name.lower().strip())
        if request.method == 'GET':
            serializer = WordSerializer(word)
            word = serializer.data
            descriptions = _get_description(word)
            forms = _get_form(word)
            return render(request, 'detail.html', {'word': word,
                                                   'descriptions': descriptions,
                                                   'forms': forms})
    except Http404:
        return render(request, 'mistake.html')
    
def word_list(request):
    if request.method == 'GET':
        text = request.GET.get('text', '').strip().lower()
        if text == '':
            return JsonResponse({'error': 'Nothing transferred', 'words': ''})
        
        words = Word.objects.filter(name__startswith=text)[:10]
        directory = _get_dict_words_with_short_description(words)
        try:
            return JsonResponse({'success': True, 'words': directory})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
    return JsonResponse({'error': 'method not allowed'}, status=405)


class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    

class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAdminUser()]