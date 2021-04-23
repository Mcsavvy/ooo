from flask import Flask, render_template, request
from flask import current_app
from helper import pets as pet


app = Flask(__name__)


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    current = current_app.name
    return render_template('index.html', agent=user_agent, app=current)


@app.route('/animals/<pet_type>')
def animals(pet_type):
    try:
        pet_names = [
            i['name'] for i in pet[pet_type]
        ]
        links = [f'/animals/{pet_type}/{x}' for x in pet_names]
        lenght = [x for x in range(len(pet_names))]
    except KeyError:
        pet_names = []

    if pet_names:
        return render_template(
            'animals.html',
            pet_type=pet_type,
            pet_names=pet_names,
            Pet_Type=pet_type.title(),
            links=links,
            length=lenght,

        )

    else:
        return f'''
        <h1>
            We Don't have any {pet_type.title()} at the moment
        </h1>
        '''


@app.route('/animals/<pet_type>/<pet_name>')
def details(pet_type, pet_name):
    pet_details = [
        x.items()
        for x in pet[pet_type]
        if x['name'] == pet_name][0]
    detail_name = [x for x, y in pet_details]
    detail_value = [y for x, y in pet_details]
    pet_details = dict(zip(detail_name, detail_value))
    name = pet_details['name']
    age = pet_details['age']
    image = pet_details['url']
    breed = pet_details['breed']
    desc = pet_details['description']
    return render_template(
        'details.html',
        name=name,
        age=age,
        image=image,
        breed=breed,
        desc=desc,
        pet_type_stripped=pet_type.strip('s'),
        Name=name.title(),
    )

