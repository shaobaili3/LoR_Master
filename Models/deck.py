from decoder import Deck


def getChampion(deckCode):
    try:
        cards = Deck.decode(deckCode).cards
        heros = ''
        for card in cards:
            if card.isChampion:
                heros += card.name + ' '
                heros += '(' + str(card.count) + ') '
        if heros == '':
            heros = 'No champion '
    except Exception as e:
        print('valid hero from code:', e)
        return 'None champion'
    print(heros)
    return heros


def getDeckCode(cardsInDeck):
    try:
        deckCode = Deck(cards=cardsInDeck).encode().deck_code
    except Exception as e:
        print('invalid cards error:', e)
        return None
    return deckCode


def validDeckCode(deckCode):
    try:
        if Deck.decode(deckCode) is None:
            return False
        else:
            return True
    except Exception as e:
        print('validDeckCode Error: ', e)
        return False
# getChampion('CIBQCAYGCEBQEBQ2EYVQQAYJEMUDGXWWAHMADWIB3MAQCAQDBEUSUAA')
# getChampion('CICACAIFGAAQIBZPAIBAKBAGAICAKAYFAMBAIBINCABQIBYJFV4QIAIFBMUSWMIDAEAQKGIBAMCQIAQEA5GGC')
# getChampion('CICACBAFAMBAEBIEAYBAIBYCKIBQCBJLGAYQIAIBAUPACAYFBAAQIBZPAMCAKAIFCABQCBAHMEAQIBICAIAQKAJA')
# getChampion('CIAAABQBAMBQ2AQDAYDAQBQBAQEBWJZLGQ3AMAQDAEBQIBIHBAGAEBQEAUEA2FQ4EATCQLJ2HQGQCAYCAQEQYDYUEMSSMKBOGM3Q')
# deckList =  {
#             "01PZ039": 1,
#             "04SH014": 1,
#             "04SH028": 3,
#             "04SH039": 1,
#             "04SH059": 1,
#             "04SH070": 1,
#             "04SH076": 2,
#             "04SH079": 1,
#             "04SH081": 1,
#             "04SH089": 1,
#             "04SH110": 1,
#             "04SH130": 2,
#             "04SH130T1": 1,
#             "04SH130T11": 2,
#             "04SH130T12": 1,
#         }

# print(deck.getDeckCode(deckList))
