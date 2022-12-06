from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from info.models import (Band, Bookmark, Comment, Instrument,
                         InstrumentCategory, InstrumentUser, Invite, Post, 
                         Request, Tag, UserBandInstrument)

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (BandSerializer, PostSerializer, TagSerializer,
                          InstrumentSerailizer, RequestSerializer)


User = get_user_model()


class BandViewSet(viewsets.ModelViewSet):
    serializer_class = BandSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return (
            Band.objects.filter(is_visible=True) | 
            Band.objects.filter(is_visible=False, author=self.request.user)
        )
    
    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def send_request(self, request, pk):
        if request.method == 'POST':
            data = {'author': request.user.id, 'band': pk}
            context = {'request': request}
            serializer = RequestSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        author = request.user
        user = get_object_or_404(User, id=pk)
        Invite.objects.get(author=author, user=user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerailizer
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
