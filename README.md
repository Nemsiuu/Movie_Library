# Movie_Library
Movie library website written in django


Simple django application which creates online catalog for movie library, where users can browse movie.
There is also a Librarian role, used to manage content and set movies as borrowed or available.
Movies have copies, with different types( DVD, Blu-Ray)

Main features that have been implemented:

- There are models for movies, copies, genre, release, actors and authors.
- Users can view list and detail information for movies, genre, actors, authors.
- Librarians can create and manage models.
- Librarians can renew reserved movies.

There are few unit tests in project, just for the show.


Quick Start

To check the project, enter https://polar-scrubland-76158.herokuapp.com/

Then create new account if you want, or use:
- Simple account ( Login = Test | Password = testuser)
- Librarian account ( Login = Librarian | Password = testuser)
- Admin account ( Login = Admin | Password = testuser)

To open admin site, open https://polar-scrubland-76158.herokuapp.com/admin/


To get this project up and running locally on your computer:

Set up the Python development environment. 
Assuming you have Python setup, run the following commands:
pip3 install -r requirements.txt

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py collectstatic

python3 manage.py test # Run the standard tests. These should all pass.

python3 manage.py createsuperuser # Create a superuser

python3 manage.py runserver

Open a browser to http://127.0.0.1:8000/admin/ to open the admin site

Create a few test objects of each type.
Open tab to http://127.0.0.1:8000 to see the main site, with your new objects.
