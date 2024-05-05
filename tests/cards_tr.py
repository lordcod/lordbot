num_values = {
    "ace": (1, None),
    "two": (2, 2),
    "three": (3, 3),
    "four": (4, 4),
    "five": (5, 5),
    "six": (6, 6),
    "seven": (7, 7),
    "eight": (8, 8),
    "nine": (9, 9),
    "ten": (10, 10),
    "jack": (11, 10),
    "queen": (12, 10),
    "king": (13, 10),
}


old = {'clubs_of_ace': '<:clubs_of_ace:1236254878867918881>', 'clubs_of_eight': '<:clubs_of_eight:1236254880981586021>', 'clubs_of_five': '<:clubs_of_five:1236254882533740614>', 'clubs_of_four': '<:clubs_of_four:1236254884232167474>', 'clubs_of_jack': '<:clubs_of_jack:1236254886119739423>', 'clubs_of_king': '<:clubs_of_king:1236254887474368533>', 'clubs_of_nine': '<:clubs_of_nine:1236254888833581116>', 'clubs_of_queen': '<:clubs_of_queen:1236254890234347540>', 'clubs_of_seven': '<:clubs_of_seven:1236254891572334644>', 'clubs_of_six': '<:clubs_of_six:1236254893015175220>', 'clubs_of_ten': '<:clubs_of_ten:1236254894525120522>', 'clubs_of_three': '<:clubs_of_three:1236254896026812508>', 'clubs_of_two': '<:clubs_of_two:1236254897243029607>', 'diamonds_of_ace': '<:diamonds_of_ace:1236254898799247441>', 'diamonds_of_eight': '<:diamonds_of_eight:1236254900338430042>', 'diamonds_of_five': '<:diamonds_of_five:1236254901835661333>', 'diamonds_of_four': '<:diamonds_of_four:1236254903140220988>', 'diamonds_of_jack': '<:diamonds_of_jack:1236254904931061800>', 'diamonds_of_king': '<:diamonds_of_king:1236254906562777191>', 'diamonds_of_nine': '<:diamonds_of_nine:1236254908164870164>', 'diamonds_of_queen': '<:diamonds_of_queen:1236254909813358602>', 'diamonds_of_seven': '<:diamonds_of_seven:1236254911797268500>', 'diamonds_of_six': '<:diamonds_of_six:1236254913412202496>', 'diamonds_of_ten': '<:diamonds_of_ten:1236254914867626064>', 'diamonds_of_three': '<:diamonds_of_three:1236254916394225696>', 'diamonds_of_two': '<:diamonds_of_two:1236254917266636912>',
       'hearts_of_ace': '<:hearts_of_ace:1236254919347142688>', 'hearts_of_eight': '<:hearts_of_eight:1236254921272066078>', 'hearts_of_five': '<:hearts_of_five:1236254923050586212>', 'hearts_of_four': '<:hearts_of_four:1236254924757536799>', 'hearts_of_jack': '<:hearts_of_jack:1236254926263418932>', 'hearts_of_king': '<:hearts_of_king:1236254928104587336>', 'hearts_of_nine': '<:hearts_of_nine:1236254929803280394>', 'hearts_of_queen': '<:hearts_of_queen:1236254931464228905>', 'hearts_of_seven': '<:hearts_of_seven:1236254933309718641>', 'hearts_of_six': '<:hearts_of_six:1236254934920593438>', 'hearts_of_ten': '<:hearts_of_ten:1236254936514428948>', 'hearts_of_three': '<:hearts_of_three:1236254938158338088>', 'hearts_of_two': '<:hearts_of_two:1236254940016545843>', 'spades_of_ace': '<:spades_of_ace:1236254941820092506>', 'spades_of_eight': '<:spades_of_eight:1236254943632162857>', 'spades_of_four': '<:spades_of_four:1236254946454667325>', 'spades_of_jack': '<:spades_of_jack:1236254949072048200>', 'spades_of_king': '<:spades_of_king:1236254951001292840>', 'spades_of_nine': '<:spades_of_nine:1236254952901316659>', 'spades_of_queen': '<:spades_of_queen:1236254955099262996>', 'spades_of_seven': '<:spades_of_seven:1236256156834594836>', 'spades_of_six': '<:spades_of_six:1236256158835277846>', 'spades_of_ten': '<:spades_of_ten:1236256161024708619>', 'spades_of_three': '<:spades_of_three:1236256162933112862>', 'spades_of_five': '<:spades_of_five:1236256181433929768>', 'spades_of_two': '<:spades_of_two:1236256183048863836>'}
new = {}
_new = {}
suits = set()


for name, emoji in old.items():
    suit, card = name.split('_of_')
    suits.add(suit)
    new.setdefault(suit, {})
    new[suit][card] = emoji

for s in suits:
    cards = new[s]
    cards = dict(
        sorted(cards.items(), key=lambda item: num_values[item[0]][0]))
    new_cards = {}
    for name, emoji in cards.items():
        new_cards[emoji] = num_values[name][1]
    _new.update(new_cards)

print(_new)
