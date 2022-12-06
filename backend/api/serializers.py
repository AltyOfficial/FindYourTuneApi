from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import Base64AudioField, Base64ImageField
from info.models import (Band, Bookmark, Comment, Instrument,
                         InstrumentCategory, InstrumentUser, Invite, Post, 
                         Request, Tag, UserBandInstrument)
from users.serializers import UserInstrumentSerializer


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Tag Serializer."""

    class Meta:
        model = Tag
        fields = ('id', 'title', 'color', 'slug')


class PostSerializer(serializers.ModelSerializer):
    """Post Serializer."""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    audio = Base64AudioField()

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'tags', 'author', 'image',
            'audio', 'text', 'likes', 'pub_date'
        )
        read_only_fields = ('author', 'likes', 'pub_date')

    def add_tags(self, post, tags):
        for tag in tags:
            post.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        post = Post.objects.create(author=author, **validated_data)
        self.add_tags(post, tags)
        return post


class InstrumentSerailizer(serializers.ModelSerializer):
    """Instrument Serializer."""

    category = serializers.ReadOnlyField(source='category.title')

    class Meta:
        model = Instrument
        fields = ('id', 'title', 'category')


class BandSerializer(serializers.ModelSerializer):
    """Band Serializer."""

    author = UserInstrumentSerializer(read_only=True)
    participants = UserInstrumentSerializer(read_only=True, many=True)
    poster = Base64ImageField()

    class Meta:
        model = Band
        fields = (
            'id', 'author', 'title', 'description', 'participants',
            'quantity', 'pub_date', 'is_visible', 'poster'
        )
        read_only_fields = ('author', 'participants', 'pub_date')
        extra_kwargs = {
            'is_visible': {'write_only': True}
        }

    def create_or_refuse_user_in_band(self, user, band, instrument):
        if UserBandInstrument.objects.filter(user=user).exists():
            band.delete()
            raise serializers.ValidationError(
                'You are forbidden to join more than one band'
            )
        else:
            UserBandInstrument.objects.create(
                user=user,
                band=band,
                instrument=instrument
            )
            return True

    def create(self, validated_data):
        request = self.context['request']
        author = request.user

        try:
            author_instrument = request.data['your_instrument']
            instrument = Instrument.objects.get(title=author_instrument)
        except Exception:
            raise serializers.ValidationError(
                'Fill your instument field correctly'
            )

        band = Band.objects.create(author=author, **validated_data)
        self.create_or_refuse_user_in_band(author, band, instrument)
        band.participants.add(author)

        return band
    
    def update(self, instance, validated_data):
        if 'quantity' in validated_data:
            quantity = validated_data.pop('quantity')
            if instance.participants.count() == quantity:
                instance.is_full = True
            elif instance.participants.count() < quantity:
                instance.is_full = False
            else:
                raise serializers.ValidationError(
                    'Number of Participants must be bigger than quantity'
                )
            instance.quantity = quantity
        print(validated_data)
        instance.save()
        return super().update(instance, validated_data)


class RequestSerializer(serializers.ModelSerializer):
    """Invite Serializer."""
    user = serializers.StringRelatedField()
    instrument = serializers.StringRelatedField()

    class Meta:
        model = Request
        fields = ('id', 'user', 'band', 'instrument', 'author')

    def validate(self, attrs):
        author = attrs['author']
        band = attrs['band']
        attrs['is_accepted'] = False

        try:
            ins_title = self.context['request'].data['instrument']
            attrs['instrument'] = Instrument.objects.get(title=ins_title)
        except Exception:
            raise serializers.ValidationError(
                'Fill instrument field correctly'
            )

        try:
            user = User.objects.get(id=band.author.id)
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'You dont own your band'
            )

        if Request.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'You have already send request into this band'
            )
        if UserBandInstrument.objects.filter(user=author, band=band).exists():
            raise serializers.ValidationError(
                'You are already in this band'
            )

        return attrs
