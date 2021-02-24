# Bookmarque
An online bookstore class project for Software Engineering (CSCI4050) Spring '21.

# Flask installation for your machine:
https://flask.palletsprojects.com/en/1.1.x/installation/#installation

## TLDR
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

## Running
```
$ export FLASK_APP=hello.py
$ flask run
```
Now just open the port Flask prints!

See below for how this project is run as a package instead of a module.

## Flask Quickstart Tutorial (how to run the web server):
https://flask.palletsprojects.com/en/1.1.x/quickstart/

## SCSS Setup
- [Difference between Sass/SCSS](https://www.geeksforgeeks.org/what-is-the-difference-between-scss-and-sass)
- [libsass with Flask](https://sass.github.io/libsass-python/frameworks/flask.html)

```
pip install libsass
export FLASK_APP=bookmarqueapp
```
