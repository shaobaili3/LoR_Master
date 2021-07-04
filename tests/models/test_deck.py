import pytest
from Models.deck import getChampion


@pytest.mark.parametrize(
    "deck_code, expected", [
        ('CIBQCAYGCEBQEBQ2EYVQQAYJEMUDGXWWAHMADWIB3MAQCAQDBEUSUAA',
         'Twisted Fate (3) Aphelios (3) '),
        ('CICACAIFGAAQIBZPAIBAKBAGAICAKAYFAMBAIBINCABQIBYJFV4QIAIFBMUSWMIDAEAQKGIBAMCQIAQEA5GGC',
         'Nasus (3) Kindred (3) '),
        ('CICACBAFAMBAEBIEAYBAIBYCKIBQCBJLGAYQIAIBAUPACAYFBAAQIBZPAMCAKAIFCABQCBAHMEAQIBICAIAQKAJA',
         'Kalista (2) Nasus (2) Kindred (2) '),
        ('CIAAABQBAMBQ2AQDAYDAQBQBAQEBWJZLGQ3AMAQDAEBQIBIHBAGAEBQEAUEA2FQ4EATCQLJ2HQGQCAYCAQEQYDYUEMSSMKBOGM3Q',
         'Teemo (1) Swain (1) Miss Fortune (1) Gangplank (1) Draven (1) Darius (1) ')
    ]
)
def test_get_champion(deck_code, expected):
    result = getChampion(deck_code)

    assert result == expected
