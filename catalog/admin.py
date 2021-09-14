from django.contrib import admin

# Register your models here.
from .models import Author,Actor, Genre, Movie, MovieInstance
class MoviesInstanceInline(admin.TabularInline):
    model = MovieInstance
    extra = 0
class MoviesInline(admin.TabularInline):
    model = Movie
    extra =0
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [MoviesInline]

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','release', 'author','display_actors', 'display_genre')
    inlines = [MoviesInstanceInline]

@admin.register(MovieInstance)
class MovieInstanceAdmin(admin.ModelAdmin):
     list_display = ('id','movie', 'type','status','borrower', 'due_back')
     list_filter = ('status', 'due_back')
     fieldsets = (
        (None, {
            'fields': ('movie', 'type', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )




    
#admin.site.register(Movie)
#admin.site.register(Author)
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)
#admin.site.register(MovieInstance)
admin.site.register(Actor)