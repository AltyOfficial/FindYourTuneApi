from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

from info.models import Instrument, UserBandInstrument, Invite, Band


User = get_user_model()


class UserInstrumentSerializer(serializers.ModelSerializer):
    """User Serializer."""
    instrument = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'instrument')
    
    def get_instrument(self, obj):
        return UserBandInstrument.objects.get(user=obj).instrument.title


class InstrumentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ('id', 'title')


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for User."""
    instruments = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password', 'instruments'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class InviteSerializer(serializers.ModelSerializer):
    """Invite Serializer."""
    band = serializers.StringRelatedField()
    instrument = serializers.StringRelatedField()

    class Meta:
        model = Invite
        fields = ('id', 'user', 'band', 'instrument', 'author')

    def validate(self, attrs):
        author = attrs['author']
        user = attrs['user']
        attrs['is_accepted'] = False

        try:
            ins_title = self.context['request'].data['instrument']
            attrs['instrument'] = Instrument.objects.get(title=ins_title)
        except Exception:
            raise serializers.ValidationError(
                'Fill instrument field correctly'
            )

        try:
            band = Band.objects.get(author=author)
            attrs['band'] = band
        except Band.DoesNotExist:
            raise serializers.ValidationError(
                'You dont own your band'
            )

        if Invite.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'You have already invited this user into your band'
            )
        if UserBandInstrument.objects.filter(user=user, band=band).exists():
            raise serializers.ValidationError(
                'This user is already in your band'
            )

        return attrs

    # def get_band(self, obj):
    #     return obj.band.title
    
    # def get_instrument(self, obj):
    #     return obj.instrument.title
