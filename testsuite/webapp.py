from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu-link')
def menu_link():
    return 'Menu Link Clicked'

@app.route('/contact', methods=['POST'])
def submit():
    return '{name} sent {message}'.format(
            name=request.form['name'],
            message=request.form['message'])

if __name__ == '__main__':
    app.run(debug=True)
