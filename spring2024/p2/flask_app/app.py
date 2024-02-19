from flask import Flask, render_template
from .model import PokeClient
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
poke_client = PokeClient()

@app.route('/')
def index():
    names_ids = zip(poke_client.get_pokemon_list(), poke_client.get_pokemon_ids())
    return render_template('index.html', info=names_ids)

@app.route('/pokemon/<pokemon_name>')
def pokemon_info(pokemon_name):
    info = poke_client.get_pokemon_info(pokemon=pokemon_name)
    return render_template('info.html', info=info)

@app.route('/ability/<ability_name>')
def pokemon_with_ability(ability_name):
    info = poke_client.get_pokemon_with_ability(ability=ability_name)
    return render_template('ability.html', info=info)
