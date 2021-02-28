from flask import Flask
from flask import render_template # for file extends
from sassutils.wsgi import SassMiddleware # for sass/scss compilation


app = Flask(__name__)

# configure directory locations for Sass/SCSS
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'bookmarqueapp': ('static/sass', 'static/css', '/static/css')
})

@app.route('/')
def homepage():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin_view.html')
