from django.db import models
from django.urls import reverse
import uuid
from datetime import date

from django.contrib.auth.models import User

class Genre(models.Model):
   
    name = models.CharField(max_length=200, help_text='Enter a movie genre (e.g. Science Fiction)')

    def get_absolute_url(self):
     
        return reverse('genre-detail', args=[str(self.id)])

    def __str__(self):
        
        return self.name


class Movie(models.Model):
    
    title = models.CharField(max_length=200)

  
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    actor = models.ManyToManyField('Actor', help_text='Add actor to this movie')
    release = models.IntegerField('Release', help_text='Year of Movie release',null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the movie')
    imdb = models.CharField('IMDb', max_length=13, unique=True,
                             help_text='7 or 8 Character <a href="https://www.imdb.com/">IMDb number</a>')

   
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this movie')

    def __str__(self):
        
        return self.title

    def get_absolute_url(self):
        
        return reverse('movie-detail', args=[str(self.id)])
    
    def display_genre(self):
        
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def display_actors(self):
     
        return ', '.join(actor.first_name +' ' +actor.last_name for actor in self.actor.all()[:3])

    display_actors.short_description = 'Actors'

class MovieInstance(models.Model):
   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular movie across whole library')
    movie = models.ForeignKey('Movie', on_delete=models.RESTRICT, null=True)
    type = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Movie availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set movie as returned"),)
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    def __str__(self):
        
        return f'{self.id} ({self.movie.title})'


class Author(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
     
        return f'{self.first_name} {self.last_name}'


class Actor(models.Model):
 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
      
        return reverse('actor-detail', args=[str(self.id)])

    def __str__(self):
        
        return f'{self.first_name} {self.last_name}'