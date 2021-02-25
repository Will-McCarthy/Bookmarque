# Bookmarqué
An online bookstore class project for Software Engineering (CSCI4050) Spring '21.

## Flask installation for your machine:
https://flask.palletsprojects.com/en/1.1.x/installation/#installation

## TLDR

- we need to install Flask to use it
- it is good practice to create a virtual environment when working on a Python project
  - essentially it is an isolated copy of Python so you can work on a specific project without worry of affecting other projects/installing different versions of things/etc.
- run the following commands to create and start the venv and then install Flask

(Mac/Linux)
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install Flask
```

(Windows)
```
$ py -3 -m venv venv
\> venv\Scripts\activate
$ pip install Flask
```

- to exit venv, you can use `deactivate` from CLI
- to gain access to the virtual environment at a later time you will need to run the activate script again

## Starting a Flask Server
```
$ export FLASK_APP=hello.py
$ flask run
```
Now just open the port Flask prints!

See SCSS setup for how this project is run as a package instead of a module.

## Flask Quickstart Tutorial (How to Run the Web Server):
https://flask.palletsprojects.com/en/1.1.x/quickstart/

## SCSS Setup
- [Difference between Sass/SCSS](https://www.geeksforgeeks.org/what-is-the-difference-between-scss-and-sass)
- [libsass with Flask](https://sass.github.io/libsass-python/frameworks/flask.html)

```
pip install libsass
export FLASK_APP=bookmarqueapp
```

- instead of exporting a module you are doing so with the entire package folder
