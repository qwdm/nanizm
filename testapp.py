# python3.6 test app
from nanizm import App


app = App()

DATA = {
    'USERS': [
        {
            'username': 'Amigo',
            'age': 12,
        },
        {
            'username': 'Foofinho',
            'age': 34,
        }
    ],
}

@app.route('/users')
def users():
    return DATA['USERS']

@app.route('/users/names')
def users_names():
    return [user['username'] for user in DATA['USERS']]

@app.route('/users/<id>')
def user(id):
    id = int(id)
    return DATA['USERS'][id]
