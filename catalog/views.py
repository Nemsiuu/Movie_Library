from django.shortcuts import render
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

@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_movies = Movie.objects.all().count()
    num_instances = MovieInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = MovieInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
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

    # Render the HTML template index.html with the data in the context variable
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

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewMovieForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            movie_instance.due_back = form.cleaned_data['renewal_date']
            movie_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
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
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')



class MovieCreate(CreateView):
    model = Movie
    fields = '__all__'
    

class MovieUpdate(UpdateView):
    model = Movie
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class MovieDelete(DeleteView):
    model = Movie
    success_url = reverse_lazy('movies')