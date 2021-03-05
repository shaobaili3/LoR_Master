from decoder import Deck


def getChampion(deckCode):
    cards = Deck.decode(deckCode).cards
    heros = ''
    for card in cards:
        if card.isChampion:
            heros += card.name + ' '
            heros += '(' + str(card.count) + ') '     
    if heros == '':
        heros = 'No champion '
    print(heros)
    return heros


# getChampion('CIBQCAYGCEBQEBQ2EYVQQAYJEMUDGXWWAHMADWIB3MAQCAQDBEUSUAA')
# getChampion('CICACAIFGAAQIBZPAIBAKBAGAICAKAYFAMBAIBINCABQIBYJFV4QIAIFBMUSWMIDAEAQKGIBAMCQIAQEA5GGC')
# getChampion('CICACBAFAMBAEBIEAYBAIBYCKIBQCBJLGAYQIAIBAUPACAYFBAAQIBZPAMCAKAIFCABQCBAHMEAQIBICAIAQKAJA')
# getChampion('CIAAABQBAMBQ2AQDAYDAQBQBAQEBWJZLGQ3AMAQDAEBQIBIHBAGAEBQEAUEA2FQ4EATCQLJ2HQGQCAYCAQEQYDYUEMSSMKBOGM3Q')
