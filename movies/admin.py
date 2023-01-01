from django.contrib import admin

from movies.actions import make_draft
from movies.models import (Category,
                           Genre,
                           Movie,
                           Actor,
                           Rating,
                           Star,
                           Review)
from movies.forms import (MovieAdminForm,
                          ReviewAdminForm,
                          ActorAdminForm)


admin.site.register(Star)


class ReviewInline(admin.TabularInline):
    form = ReviewAdminForm
    model = Review
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url',)
    list_display_links = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_draft')
    list_display_links = ('title',)
    search_fields = ('title', 'category__name')
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('is_draft',)
    form = MovieAdminForm
    actions = (make_draft,)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': (('description', 'poster'),)
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'fields': (('actors', 'directors', 'genres', 'category'),),
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        (None, {
            'fields': (('url'), ('is_draft'))
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    readonly_fields = ('name', 'email')
    form = ReviewAdminForm


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    form = ActorAdminForm


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
