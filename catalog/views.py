from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Author, MovieInstance, Genre, Actor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.models import Author
from catalog.forms import RenewMovieForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from catalog.forms import SignUpForm

@login_required
def index(request):
    """View function for home page of site."""

    
    num_movies = Movie.objects.all().count()
    num_instances = MovieInstance.objects.all().count()

    
    num_instances_available = MovieInstance.objects.filter(status__exact='a').count()

    
    num_genres = Genre.objects.count()   
    num_authors = Author.objects.count()
    num_actors = Actor.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_movies': num_movies,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_actors' : num_actors,
        'num_genres' : num_genres,
        'num_visits': num_visits,
    }

    
    return render(request, 'index.html', context=context)

from django.views import generic

class MovieListView(LoginRequiredMixin,generic.ListView):
    model = Movie
    paginate_by = 10


class MovieDetailView(LoginRequiredMixin,generic.DetailView):
    model = Movie

    
class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    model = Author

    
class ActorListView(LoginRequiredMixin,generic.ListView):
    model = Actor
    paginate_by = 10


class ActorDetailView(LoginRequiredMixin,generic.DetailView):
    model = Actor

class GenreListView(LoginRequiredMixin,generic.ListView):
    model = Genre
    paginate_by = 10


class GenreDetailView(LoginRequiredMixin,generic.DetailView):
    model = Genre

class LoanedMoviesByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = MovieInstance
    template_name ='catalog/movieinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return MovieInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedMoviesByUsers(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = MovieInstance
    template_name ='catalog/movieinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return MovieInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_movie_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    movie_instance = get_object_or_404(MovieInstance, pk=pk)

    
    if request.method == 'POST':

       
        form = RenewMovieForm(request.POST)

       
        if form.is_valid():
            
            movie_instance.due_back = form.cleaned_data['renewal_date']
            movie_instance.save()

           
            return HttpResponseRedirect(reverse('all-borrowed') )

    
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewMovieForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'movie_instance': movie_instance,
    }

    return render(request, 'catalog/movie_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    

class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__' 

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')



class MovieCreate(CreateView):
    model = Movie
    fields = '__all__'
    

class MovieUpdate(UpdateView):
    model = Movie
    fields = '__all__' 

class MovieDelete(DeleteView):
    model = Movie
    success_url = reverse_lazy('movies')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})