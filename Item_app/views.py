from django.shortcuts import render
from rest_framework import viewsets
from Item_app.serializers import ItemSerializer
from Item_app.models import Item
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import logging
from django.core.cache import cache

logger = logging.getLogger('Item_app')

class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        cache_key = 'item_list'
        cached_data = cache.get(cache_key)
        print(cached_data)
        if cached_data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset,many=True)
            cached_data = serializer.data
            cache.set(cache_key,cached_data,timeout=120)
        return Response(cached_data)
    
    def retrieve(self, request, *args, **kwargs):
        cache_key = f'item_{kwargs["pk"]}'
        cached_data = cache.get(cache_key)

        if cached_data is None:
            response = super().retrieve(request, *args, **kwargs)
            if response.status_code == 200:
                cached_data = response.data
                cache.set(cache_key, cached_data, timeout=60)
                return response
      
        return Response( cached_data)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete(f'item_{kwargs["pk"]}')
        cache.delete('item_list')
        return response

    def destroy(self, request, *args, **kwargs): 
        logger.info('API called: DELETE /Item/%s/', kwargs['pk'])
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            cache.delete(f'item_{kwargs["pk"]}')
            cache.delete('item_list')
        except Exception as e:
            return Response({'message': 'No Item matches the given query.' },status= status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

      
