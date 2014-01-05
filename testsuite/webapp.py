from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu-link')
def menu_link():
    return 'Menu Link'

if __name__ == '__main__':
    app.run(debug=True)
