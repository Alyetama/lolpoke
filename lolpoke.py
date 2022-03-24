import json
import shlex
import subprocess
import sys
import tempfile

import pypokedex
import requests
from loguru import logger


def get_poke(poke):
    try:
        pokemon = pypokedex.get(name=poke)
    except pypokedex.exceptions.PyPokedexHTTPError as e:
        if '--img' in sys.argv:
            logger.error(e)
        sys.exit(1)
    attrs = [
        x for x in dir(pokemon) if x in [
            'abilities', 'base_experience', 'base_stats', 'height', 'name',
            'types', 'weight'
        ]
    ]
    d = {'number': '#' + str(pokemon.dex).zfill(3)}
    for _attr in attrs:
        obj = getattr(pokemon, _attr)
        d.update({_attr: obj})

    d['abilities'] = [x.name for x in d['abilities']]
    d['base_stats'] = [
        f"{x}: {getattr(d['base_stats'], x)}" for x in dir(d['base_stats'])
        if not x.startswith('_') and x not in ['count', 'index']
    ]

    len_ = int(len(d['base_stats']) / 2)

    d['types'] = ', '.join([x for x in d['types']])
    d['height & weight'] = f'{d["height"]}, {d["weight"]}'
    d.pop('height')
    d.pop('weight')

    d = {k.upper().replace('_', ' '): v for k, v in d.items()}
    d['picture'] = f'https://www.serebii.net/art/th/{pokemon.dex}.png'
    return d


def main(pokemon_data):
    r = requests.get(pokemon_data['picture'])
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(r.content)

        p = subprocess.run(shlex.split(f'{catimg} -H 40 {fp.name}'),
                           shell=False,
                           check=True,
                           capture_output=True,
                           text=True)

        if '--img' in sys.argv:
            print(p.stdout)
            return

        if '--print' in sys.argv or True:
            pokemon_data.pop('picture')
            _info = {k.upper(): v for k, v in pokemon_data.items()}
            info = {'NUMBER': _info['NUMBER'], 'NAME': _info['NAME']}
            info.update(_info)
            print(json.dumps(info, indent=2))


if __name__ == '__main__':
    catimg = sys.argv[1]
    poke = sys.argv[2]
    pokemon_data = get_poke(poke)
    main(pokemon_data)
