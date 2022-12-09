from django.contrib import admin

from .models import (Band, Bookmark, Review, Instrument, Invite,
                     InstrumentCategory, InstrumentUser, Post, Request,
                     Tag, UserBandInstrument)


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'title', 'quantity', 'description',
        'is_full', 'is_visible'
    )
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    empty_value_display = '-empty-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created')
    list_filter = ('post',)
    search_fields = ('post',)
    empty_value_display = '-empty-'


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category')
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(InstrumentUser)
class InstrumentUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'instrument')
    empty_value_display = '-empty-'


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'band', 'instrument', 'author', 'is_accepted'
    )
    empty_value_display = '-empty-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'text', 'pub_date')
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'band', 'instrument', 'author', 'is_accepted'
    )
    empty_value_display = '-empty-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'color', 'slug')
    list_filter = ('title',)
    search_fields = ('title',)
    empty_value_display = '-empty-'


@admin.register(UserBandInstrument)
class UserBandInstrumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'band', 'instrument')
    empty_value_display = '-empty-'
