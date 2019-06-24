# Parser for the wizard/sorcerer spell list from d20pfsrdcompanion.com

import requests
import re
from bs4 import BeautifulSoup

url = 'http://www.pfcompanion.com/spells/wizard-spells.html'

def clean_name(target):
    r = re.compile('\n+.*')
    return r.sub('', target)


def parse(debug=False):
    """ Parse the spell list from the url

    Parameters:
    debug (boolean) -- whether to print the maps to the standard output or not (default False)

    Returns:
    spell_list (list) -- parsed spell list
    """
    spell_list = []
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    #print(soup.table.tr.get_text())
    spells = soup.find_all('tr')
    for spell in spells[1:]:
        name, level, school, mf, description, source = (it.get_text() for it in spell.find_all('td'))
        link = spell.find('a', href=True)
        spell_map = {
            'name': clean_name(name),
            'level': level,
            'school': school,
            'mf': mf,
            'description': description,
            'source': source,
            'link': link['href']
        }

        spell_list.append(spell_map)
        if(debug):
            print(spell_map)

    return spell_list

if __name__ == '__main__':
    parse(debug=True)
