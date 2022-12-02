from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
from django.utils import timezone



User = get_user_model()


class InstrumentCategory(models.Model):
    """Instrument Category Model."""

    title = models.CharField(
        verbose_name='title',
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        blank=False,
        null=False,
        unique=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Instrument Category'
        verbose_name_plural = 'Instrument Categories'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/categories/{self.slug}/'
        # return reverse("model_detail", kwargs={"pk": self.pk})


class Tag(models.Model):
    """Tag Model."""

    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]

    title = models.CharField(
        verbose_name='title',
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    color = ColorField(samples=COLOR_PALETTE)
    slug = models.SlugField(
        verbose_name='slug',
        max_length=50,
        blank=False,
        null=False,
        unique=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/tags/{self.slug}/'


class Instrument(models.Model):
    """Instrument Model"""

    title = models.CharField(
        verbose_name='title',
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    category = models.ForeignKey(
        InstrumentCategory,
        on_delete=models.CASCADE,
        related_name='instruments',
        verbose_name='category'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Instrument'
        verbose_name_plural = 'Instruments'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/categories/{self.category.slug}/instruments/{self.pk}/'


class InstrumentUser(models.Model):
    """User and Instruments that User Play Model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_user_instrument',
        verbose_name='instrument user'
    )
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='is_instrument',
        verbose_name='instrument'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Instrument that user play'
        verbose_name_plural = 'Instruments that users play'

    def __str__(self):
        return f'{self.user.username} plays {self.instrument}'


class Post(models.Model):
    """Post Model."""

    title = models.CharField(
        verbose_name='title',
        max_length=255,
        blank=False,
        null=False
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='posts',
        verbose_name='tags'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='author'
    )
    image = models.ImageField(
        verbose_name='image',
        upload_to='posts/images/',
        null=True,
        default=None
    )
    audio = models.FileField(
        verbose_name='audio',
        upload_to='posts/audios/',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3'])],
        default=None
    )
    text = models.TextField(
        verbose_name='text',
        blank=True,
        null=True
    )
    likes = models.ManyToManyField(
        User,
        related_name='posts_liked',
        blank=True
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.title[:20]
    
    def get_like_number(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return f'/posts/{self.pk}/'


class Comment(models.Model):
    """Comment to Some Post Model."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=1000)
    image = models.ImageField(
        verbose_name='image',
        upload_to='posts/images/',
        null=True,
        default=None
    )
    audio = models.FileField(
        verbose_name='audio',
        upload_to='posts/audios/',
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['wav', 'mp3'])],
        default=None
    )
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[:20]


class Bookmark(models.Model):
    """User and Post that User Bookmarked Model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_user_bookmark',
        verbose_name='user'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='is_post',
        verbose_name='post'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Bookmarked user\'s post'
        verbose_name_plural = 'Bookmarked users posts'

    def __str__(self):
        return f'{self.user.username} has {self.post.id} in bookmarks'


class Band(models.Model):
    """Band Model."""

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='band_creator',
        verbose_name='creator'
    )
    title = models.CharField(
        verbose_name='title',
        max_length=255,
        blank=False,
        null=False,
        unique=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='band_participant',
        verbose_name='participants'
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    description = models.TextField(
        verbose_name='description',
        blank=False,
        null=False
    )
    is_full = models.BooleanField(verbose_name='is_full', default=False)
    is_visible = models.BooleanField(verbose_name='is_visible', default=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Band'
        verbose_name_plural = 'Bands'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/bands/{self.pk}/'


class UserBandInstrument(models.Model):
    """Band, User and User\'s Instrument that User Play in this Band Model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_user_in_band',
        verbose_name='user'
    )
    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE,
        related_name='band_user',
        verbose_name='band'
    )
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='instrument_user',
        verbose_name='instrument'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'User, band and instrument'
        verbose_name_plural = 'Users, bands and instruments'

    def __str__(self):
        return f'{self.band} - {self.user.username} - {self.instrument}'


class Request(models.Model):
    """Request to Join some Band Model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_request',
        verbose_name='user'
    )
    band = models.ForeignKey(
        Band,
        on_delete=models.CASCADE,
        related_name='requested_user',
        verbose_name='band'
    )
    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='instrument_request',
        verbose_name='instrument'
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator_request',
        verbose_name='creator'
    )
    is_approved = models.BooleanField(
        verbose_name='is_approved',
        default=False
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'

    def __str__(self):
        return f'{self.pk}'


