## Hosted URL
https://capstone-project-deployment.onrender.com
## Getting Started Locally

### Installing Dependencies

#### Python 3.9

Follow instructions to install this version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). 

```bash
python3 -m venv env # to make the environment
source env/bin/activate # to activate the environment
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
export FLASK_DEBUG=True;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# API Reference
## Error Handling

### Unauthorized
``` json
    "success": "False", 
    "error": 401, 
    "message": "unauthorised"
```
### Permission not found
``` json
    "success": "False", 
    "error": 403, 
    "message": "permission not found"
```
### Not Found
```json
{
    "success": "False",
    "error": 404, 
    "message": "resource not found"
}
```
### Method not allowed
```json
{
  "success": "False",
  "error": 405, 
  "message": "method not allowed"
}
```
### Unprocessable entity
```json
{
  "success": "False",
  "error": 422,
  "message": "unprocessable entity"
}
```
## Endpoints
`GET '/movies'`

- Returns a dictionary of movies, including titles and release dates
- Request Arguments: None
- Sample: `curl -X GET http://127.0.0.1:5000/movies`

```json
{
  "movies": [{
    "title": "Titanic",
    "release date": "December 17 1998"
  }],
  "number of movies": 1,
  "success": true
}
```

`GET '/actors'`

- Returns a dictionary of actors and their corresponding name, age, and gender.
- Request Arguments: None
- Sample: `curl -X GET http://127.0.0.1:5000/actors`

```json
{
    "actors": [{
        "name": "Gillian Anderson",
        "age": 55,
        "gender": "female"
    },
    {
       "name": "Bella Ramsey",
        "age": 20,
        "gender": "non-binary" 
    }],
    "number of actors": 2, 
    "success": true
}
```
`POST '/actors'`

- Creates a new actor entry using submitted name, age, and gender. Returns a dictionary summary of the new actor, inlcuding the entry id. 
- Request Arguments: Required: `'name'` string, `'age'` integer, `'gender'`. Key `'gender'` accepts the following values `'male', 'female', 'non-binary', 'other', 'prefer not to say'`.
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"name": "Bella Ramsey", "age": 20, "gender": "non-binary"}' http://localhost:5000/actors`

``` json
{
    "new actor": {
        "name": "Bella Ramsey",
        "age": 20,
        "gender": "non-binary"
    },
    "success": true
}
```

`POST '/movies'`

- Creates a new movie entry using submitted title and release date. Returns a dictionary summary of the new movie, inlcuding the entry id. 
- Request Arguments: Required: `'title'` string, `'release_date'` dd/mm/yyyy. 
- Sample: `curl -X POST -H "Content-Type: application/json" -d '{"title": "Titanic", "release_date": "December 17 1998"}' http://localhost:5000/movies`

``` json
{
    "new movie": {
        "title": "Titanic",
        "release date": "December 17 1998"
    },
    "success": true
}
```

`DELETE '/movies/<int:movie_id>'`

- Deletes the movie corresponding to the given ID if it exists. Returns the title of the deleted movie on success.
- Request arguments: Required: `question_id` - integer.
- Sample: `curl -X DELETE http://127.0.0.1:5000/movies/1`

``` json
{
  "deleted": "Movie Titanic deleted!",
  "success": true
}
```

`DELETE '/actors/<int:actor_id>'`

- Deletes the movie corresponding to the given ID if it exists. Returns the name of the deleted actor on success.
- Request arguments: Required: `actor_id` integer.
- Sample: `curl -X DELETE http://127.0.0.1:5000/actors/2`

``` json
{
  "deleted": "Gillian Anderson",
  "success": true
}
```

`PATCH '/movies/<int:movie_id>'`

- Modifies an existing movie entry, selected by its ID. Returns the updated movie item on success.
- Request arguments: At least one of the following: `'title'` string, `'release_date'` dd/mm/yyyy. 
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Accept: application/json" -d '{"release_date": "12/12/2004"}' http://127.0.0.1:5000/movies/1`

``` json
{
  "new movie": {
        "title": "Titanic",
        "release date": "December 12 2004"
    },
    "success": true
}
```

`PATCH '/actors/<int:actor_id>'`
- Modifies an existing actor, selected by its ID. Returns the updated actor item on success.
- Request arguments: At least one of the following: `'name'` string, `'age'` integer, `'gender'`. Key `'gender'` accepts the following values `'male', 'female', 'non-binary', 'other', 'prefer not to say'`.
- Sample: `curl -X PATCH -H "Content-Type: application/json" -H "Accept: application/json" -d '{"age": "21"}' http://127.0.0.1:5000/movies/2`

``` json
{
    "new actor": {
        "name": "Bella Ramsey",
        "age": 21,
        "gender": "non-binary"
    },
    "success": true
}
```