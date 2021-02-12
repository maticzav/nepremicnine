"""
Ta datoteka vsebuje pomožne funkcije, ki jih uporablja več skript v projektu.
"""

import csv
import json
import os
import sys
from functools import lru_cache

import requests


@lru_cache(maxsize=None)
def levensthein(a, b):
    """
    Vrne Levenstheinovo razdaljo med dvema nizoma in ne spoštuje
    velikih in malih črk.
    """

    # Če je kateri od nizov prazen smo dolžino drugega narazen.
    if a == "":
        return len(b)
    if b == "":
        return len(a)
    
    # Gledamo neodvisno od velikosti znakov.
    a = a.lower()
    b = b.lower()

    # Če sta prva znaka enaka pogledamo repe.
    if a[0] == b[0]:
        return levensthein(a[1:], b[1:])

    # Drugače pogledamo najmanjšo možnost.
    moznosti = [
        levensthein(a[1:], b),
        levensthein(a, b[1:]),
        levensthein(a[1:], b[1:])
    ]

    return 1 + min(moznosti)

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print(f'Shranjujem {url} ...', end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari JSON datoteko.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)

def vsebina_json_datoteke(ime_datoteke):
    '''Vrne json vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return json.load(datoteka)
