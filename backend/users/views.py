from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsAuthorOrReadOnly
from info.models import Invite, Band, UserBandInstrument

from .serializers import UserListSerializer, InviteSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_permissions(self):
            if self.request.method == 'POST':
                return (AllowAny(),)

            return (IsAuthenticated(),)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def invite_user(self, request, pk):
        if request.method == 'POST':
            data = {'author': request.user.id, 'user': pk}
            context = {'request': request}
            serializer = InviteSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        author = request.user
        user = get_object_or_404(User, id=pk)
        Invite.objects.get(author=author, user=user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class InviteViewSet(viewsets.ModelViewSet):
    serializer_class = InviteSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_queryset(self):
        return Invite.objects.filter(user=self.request.user)
    
    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def accept(self, request, pk):
        """Accepting your invites."""

        if UserBandInstrument.objects.filter(user=request.user).exists():
            raise ValidationError("ARE YOU FKING MAD? YOU ALREADY HAVE A BAND")

        try:
            invite = Invite.objects.get(id=pk)
        except Invite.DoesNotExist:
            raise ValidationError('THERE IS NO SUCH INVITE')

        if invite.user != request.user:
            raise ValidationError('hey, its not yours')

        band = Band.objects.get(author=invite.author)
        band.participants.add(request.user)
        UserBandInstrument.objects.create(
            user=request.user,
            instrument=invite.instrument,
            band=band
        )
        invite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
