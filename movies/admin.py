from django.contrib import admin

from movies.actions import make_draft
from movies.forms import ActorAdminForm, MovieAdminForm, ReviewAdminForm
from movies.models import Actor, Category, Genre, Movie, Rating, Review


class ReviewInline(admin.TabularInline):
    model = Review
    form = ReviewAdminForm
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
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
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        (None, {
            'fields': (('url',), ('is_draft',))
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'movie')
    readonly_fields = ('name',)
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
