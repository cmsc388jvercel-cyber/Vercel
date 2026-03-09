from flask import Flask, render_template, redirect, url_for
# from waitress import serve
app = Flask(__name__)
app.jinja_env.globals.update(zip=zip)

@app.route('/')
def index():
    return redirect(url_for("homepage"))

@app.route('/388j')
def homepage():
    return render_template('home.html')

@app.route('/388j/projects')
def projects():
    return render_template('projects.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)  # local dev only