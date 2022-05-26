# Credit to @stelar7, this python implementation is a port of his original javascript implementation

from base64 import b32decode, b32encode
from io import BytesIO
MAX_KNOWN_VERSION = 50


class Base32:
    @staticmethod
    def decode(b32string):
        s = Base32.add_padding(b32string)
        return b32decode(s)

    @staticmethod
    def encode(bytes_list):
        encoded_string = b32encode(bytes(bytes_list))
        encoded_string = str(encoded_string, "utf-8").strip("=")
        return encoded_string

    # python's builtin decoder is strict with padding
    @staticmethod
    def add_padding(b32String):
        length = len(b32String)
        padding = 0

        if (length % 8 > 0):
            padding = 8 - (length % 8)
            b32String += "=" * padding
        return b32String


faction_code_to_id = {
    "DE": 0,
    "FR": 1,
    "IO": 2,
    "NX": 3,
    "PZ": 4,
    "SI": 5,
    "BW": 6,
    "SH": 7,
    "BC": 10,
    "MT": 9,
    "RU": 12
}
id_to_faction_code = {
    0: "DE",
    1: "FR",
    2: "IO",
    3: "NX",
    4: "PZ",
    5: "SI",
    6: "BW",
    7: "SH",
    10: "BC",
    9: "MT",
    12: "RU"
}


class DeckCode:
    @staticmethod
    def encode_deck(deck):

        result = [17]
        cards_3 = []
        cards_2 = []
        cards_1 = []
        cards_other = []
        #remove non-collectable and created deck code 
        deck = DeckCode.remove_invalid_cards(deck)
        if not DeckCode.is_valid_card_codes_and_count(deck):
            raise Exception("Deck contains invalid card codes")
        else:
            for card, count in deck.items():
                if count == 3:
                    cards_3.append(card)
                elif count == 2:
                    cards_2.append(card)
                elif count == 1:
                    cards_1.append(card)
                else:
                    cards_other.append((card, count))

        grouped_cards_3 = DeckCode.group_by_faction(cards_3)
        grouped_cards_2 = DeckCode.group_by_faction(cards_2)
        grouped_cards_1 = DeckCode.group_by_faction(cards_1)

        grouped_cards_3 = DeckCode.sort_card_groups(grouped_cards_3)
        grouped_cards_2 = DeckCode.sort_card_groups(grouped_cards_2)
        grouped_cards_1 = DeckCode.sort_card_groups(grouped_cards_1)
        cards_other = sorted(cards_other)

        # encode
        result = [*result, *VarIntTransformer.encodeGroupOf(grouped_cards_3)]
        result = [*result, *VarIntTransformer.encodeGroupOf(grouped_cards_2)]
        result = [*result, *VarIntTransformer.encodeGroupOf(grouped_cards_1)]

        result = [*result, *VarIntTransformer.encodeNOfs(cards_other)]

        return Base32.encode(result)

    @staticmethod
    def group_by_faction(card_list):
        new_list = []
        while len(card_list) > 0:
            card = card_list.pop(0)
            set_num, faction, _ = DeckCode.parse_card_code(card)

            faction_set = []
            faction_set.append(card)

            temp_list = card_list[:]
            for card in temp_list:
                current_set_num, current_faction, _ = DeckCode.parse_card_code(
                    card)
                if current_set_num == set_num and current_faction == faction:
                    faction_set.append(card)
                    card_list.remove(card)
            faction_set.sort()
            new_list.append(faction_set)

        return new_list

    @staticmethod
    def sort_card_groups(card_groups):
        s = sorted(card_groups, key=lambda x: len(x))
        return s

    @staticmethod
    def parse_card_code(card_code):
        set = card_code[:2]
        faction = card_code[2:4]
        card_id = card_code[4:]
        return set, faction, card_id

    @staticmethod
    def is_valid_card_codes_and_count(deck):
        for card, count in deck.items():
            code = card
            if len(code) != 7:
                print(f"deck code length is {len(code)}")
                return False

            # check set code is numeric
            for char in code[:2]:
                if not char.isdigit():
                    print(f"code is not digit: {char}")
                    return False

            faction = faction_code_to_id.get(code[2:4], -1)
            if faction < 0:
                print(f"faction code not in faction code list: {code[2:4]}")
                return False

            for char in code[4:]:
                if not char.isdigit():
                    print(f"card number contains non digit: {char}")
                    return False

            if count < 1:
                print("less than one card: {count}")
                return False

        return True

    @staticmethod
    def remove_invalid_cards(deck):
        # When you remove continue, it will not print error messages
        newDeck = deck.copy()
        for card, count in deck.items():
            code = card
            if len(code) != 7:
                print(f"remove_invalid_cards deck code length is {len(code)}")
                del newDeck[card]
                continue

            # check set code is numeric
            for char in code[:2]:
                if not char.isdigit():
                    print(f"remove_invalid_cards code is not digit: {char}")
                    del newDeck[card]
                    continue

            faction = faction_code_to_id.get(code[2:4], -1)
            if faction < 0:
                print(f"remove_invalid_cards faction code not in faction code list: {code[2:4]}")
                del newDeck[card]
                continue

            for char in code[4:]:
                if not char.isdigit():
                    print(f"remove_invalid_cards card number contains non digit: {char}")
                    del newDeck[card]
                    continue

            if count < 1:
                print("remove_invalid_cards less than one card: {count}")
                del newDeck[card]
                continue
        return newDeck

    @staticmethod
    def decode_deck(string):
        result = {}
        data = Base32.decode(string)
        byte_list = BytesIO(data)
        version = VarIntTransformer.popVarInt(byte_list)     
        if version > MAX_KNOWN_VERSION:
            raise ValueError("Please update to the latest version of twisted_fate")
        for i in range(3, 0, -1):
            numGroupOfs = VarIntTransformer.popVarInt(byte_list)
            for __ in range(numGroupOfs):
                numOfsInThisGroup = VarIntTransformer.popVarInt(byte_list)
                setNum = VarIntTransformer.popVarInt(byte_list)
                faction = VarIntTransformer.popVarInt(byte_list)
                for ___ in range(numOfsInThisGroup):
                    card = VarIntTransformer.popVarInt(byte_list)

                    setString = str(setNum).zfill(2)
                    factionString = id_to_faction_code[faction]
                    cardString = str(card).zfill(3)

                    card_code = setString + factionString + cardString
                    result[card_code] = i

        while len(bytearray(byte_list)) > 0:
            fpc = VarIntTransformer.popVarInt(byte_list)
            fps = VarIntTransformer.popVarInt(byte_list)
            fpf = VarIntTransformer.popVarInt(byte_list)
            fpn = VarIntTransformer.popVarInt(byte_list)

            fpss = str(fps).zfill(2)
            fpfs = id_to_faction_code[fpf]
            fpns = str(fpn).zfill(3)

            card_code = fpss + fpfs + fpns
            result[card_code] = fpc
        return result


class VarIntTransformer:
    @staticmethod
    def popVarInt(stream):
        #data = BytesIO(_bytes)
        shift = 0
        result = 0
        while True:
            c = stream.read(1)
            if c == b"" or c == "":
                raise EOFError("Unexpected EOF while reading varint")
            i = ord(c)
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break

        return result

    @staticmethod
    def getVarInt(value):
        value = int(value)
        AllButMSB = 0x7F
        JustMSB = 0x80

        buff = [10]
        current_index = 0

        if value == 0:
            return [0]

        while value != 0:
            byte_val = value & AllButMSB
            value >>= 7

            if value != 0:
                byte_val |= JustMSB

            try:
                buff[current_index] = byte_val
            except IndexError:
                buff.append(byte_val)

            current_index += 1

        return buff[:current_index]

    @staticmethod
    def encodeNOfs(nOfs):
        _bytes = []
        for card, count in nOfs:
            _bytes = [*_bytes, *VarIntTransformer.getVarInt(count)]

            setNum, factionCode, cardNum = DeckCode.parse_card_code(card)
            factionNum = faction_code_to_id[factionCode]

            _bytes = [*_bytes, *VarIntTransformer.getVarInt(setNum)]
            _bytes = [*_bytes, *VarIntTransformer.getVarInt(factionNum)]
            _bytes = [*_bytes, *VarIntTransformer.getVarInt(cardNum)]

        return _bytes

    @staticmethod
    def encodeGroupOf(groupOf):
        _bytes = []

        _bytes = [*_bytes, *VarIntTransformer.getVarInt(len(groupOf))]

        for cardList in groupOf:
            _bytes = [*_bytes, *VarIntTransformer.getVarInt(len(cardList))]

            current_card_code = cardList[0]
            current_set_num, current_faction_code, _ = DeckCode.parse_card_code(
                current_card_code)
            current_faction_num = faction_code_to_id[current_faction_code]

            _bytes = [*_bytes, *VarIntTransformer.getVarInt(current_set_num)]
            _bytes = [
                *_bytes, *VarIntTransformer.getVarInt(current_faction_num)
            ]

            for card in cardList:
                sequenceNumber = card[4:]
                _bytes = [
                    *_bytes, *VarIntTransformer.getVarInt(sequenceNumber)
                ]

        return _bytes
