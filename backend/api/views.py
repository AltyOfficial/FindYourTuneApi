from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from info.models import (Band, Bookmark, Review, Instrument,
                         InstrumentCategory, Invite, Post,
                         Request, Tag, UserBandInstrument)
from utils.pagination import ResponseOnlyPagination

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (BandSerializer, BookmarkSeriazlier,
                          InstrumentCategorySerializer, InstrumentSerailizer,
                          PostSerializer, RequestSerializer, ReviewSerializer,
                          TagSerializer)


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


class InstrumentCategoryViewSet(viewsets.ModelViewSet):
    queryset = InstrumentCategory.objects.all()
    serializer_class = InstrumentCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ResponseOnlyPagination
    lookup_field = 'slug'


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerailizer
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def like(self, request, pk):
        """Like the Post."""

        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            raise ValidationError('THERE IS NO SUCH POST')

        if request.method == 'POST':
            post.likes.add(request.user)
            return Response(
                'Your like was submitted',
                status=status.HTTP_200_OK
            )

        post.likes.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
        serializer_class=ReviewSerializer
    )
    def review(self, request, pk):
        if request.method == 'POST':
            data = {"author": request.user.id, "post": pk}
            context = {'request': request}

            for key, value in request.data.items():
                if key not in ('text', 'image', 'audio'):
                    raise ValidationError('Wrong Field')
                data[key] = value

            serializer = ReviewSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        post = get_object_or_404(Post, id=pk)
        review = get_object_or_404(Review, post=post, author=request.user)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def reviews(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        queryset = Review.objects.filter(post=post)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def bookmark(self, request, pk):
        """Adding the Post to Bookmarks."""

        if request.method == 'POST':
            data = {'user': request.user.id, 'post': pk}
            serializer = BookmarkSeriazlier(
                data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        user = request.user
        post = get_object_or_404(Post, id=pk)
        obj = get_object_or_404(Bookmark, post=post, user=user)
        obj.delete()

        return Response('DELETED', status=status.HTTP_204_NO_CONTENT)


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Request.objects.filter(user=self.request.user)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def accept(self, request, pk):
        """Accepting your invites."""

        try:
            request_obj = Request.objects.get(id=pk)
        except Request.DoesNotExist:
            raise ValidationError('THERE IS NO SUCH REQUEST')

        if request_obj.user != request.user:
            raise ValidationError('hey, its not yours')

        band = Band.objects.get(author=request.user)

        if band.quantity <= band.participants.count():
            raise ValidationError('Your band is full')

        band.participants.add(request_obj.author)
        UserBandInstrument.objects.create(
            user=request_obj.author,
            instrument=request_obj.instrument,
            band=band
        )
        request_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
