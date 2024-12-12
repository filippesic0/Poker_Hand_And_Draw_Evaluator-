from collections import Counter

value_order = "AKQJT98765432"
    
def is_kicker(made_hand, hand, board):
    # Uklanjamo boje iz hand i board, ostavljamo samo vrednosti
    made_hand = [card[0] for card in made_hand]  # Uzimamo samo vrednosti iz hand
    hand = [card[0] for card in hand]  # Uzimamo samo vrednosti iz hand
    board = [card[0] for card in board]  # Uzimamo samo vrednosti iz board
    
    # Uklanjamo karte iz hand i board koje su već u made_hand
    hand = [card for card in hand if card not in made_hand]
    board = [card for card in board if card not in made_hand]
    
    # Kombinujemo ruku (made_hand) i preostale karte sa stola
    cards = made_hand + sorted(hand + board, key=lambda x: "AKQJT98765432".index(x[0])) 
    
    # Ako imamo više od 5 karata, uzimamo samo prvih 5
    if len(cards) > 5:
        cards = cards[:5]
    
    # Brojanje vrednosti karata
    value_counts = Counter(card for card in cards)
    
    # Ako imamo dva para i preostala karta u ruci formira treći par, kicker ne postoji
    if len(made_hand) == 2 and value_counts[made_hand[0]] == 2 and value_counts[made_hand[1]] == 2:
        remaining_cards = [card for card in hand if card not in made_hand]
        if remaining_cards and remaining_cards[0] in value_counts and value_counts[remaining_cards[0]] == 2:
            return "No kicker"
    
    # Ako kicker nije među 5 najjačih karata, vraćamo "No kicker"
    if len(hand)>0:
        if hand[0] in cards:
            return hand[0]  # Vraćamo kicker

    return 0

# Funkcija koja pronalazi i prepoznaje Straight Flush
def is_straight_flush(cards):
    
    # Mogući nizovi za kentu (5 uzastopnih karata)
    possible_straights = [
        ['A', 'K', 'Q', 'J', 'T'],
        ['K', 'Q', 'J', 'T', '9'],
        ['Q', 'J', 'T', '9', '8'],
        ['J', 'T', '9', '8', '7'],
        ['T', '9', '8', '7', '6'],
        ['9', '8', '7', '6', '5'],
        ['8', '7', '6', '5', '4'],
        ['7', '6', '5', '4', '3'],
        ['6', '5', '4', '3', '2'],
        ['5', '4', '3', '2', 'A']
    ]
    
    # Proveri sve karte u sortiranom nizu
    for card in cards:
        for straight in possible_straights:
            if card[0] == straight[0]:  # Provera cele karte (vrednost i boja)
                straight_cards = [c for c in cards if c[0] in straight and c[1]==card[1]]
                straight_cards = sorted(straight_cards, key=lambda x: "AKQJT98765432".index(x[0]))
                
                # Ako ima 5 karata u nizu
                if len(straight_cards) == 5:
                    #Provera da li su karte u nizu
                    check = True
                    for i in range(5):
                        if not straight_cards[i][0] == straight[i]:
                            check = False
                            break
                    if not check:
                        continue
                    # Proveri boje karata
                    highest_card_suit = card[1]  # Boja trenutne karte
                    if all(c[1] == highest_card_suit for c in straight_cards):
                        # Ako je Straight Flush A visoki, označavamo kao Royal Flush
                        if "A" in [c[0] for c in straight_cards] and "K" in [c[0] for c in straight_cards]:
                            return "Royal Flush", straight_cards
                        else:
                            return "Straight Flush", straight_cards  # Vraćamo odmah prvi pronađeni Straight Flush
    
    return []  # Ako nije pronađen Straight Flush
		
def is_flush(hand, board, door):#5-card flush je flush, 4-card flush je flush draw, a 3-card je backdoor draw
    # Vrednosti karata od A do 2
    values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    value_map = {value: i for i, value in enumerate(values)}
    all_cards = hand + board
    suit_counts = Counter(card[1] for card in all_cards)
    
    if any(count >= door for count in suit_counts.values()):
        flush_suit = [suit for suit, count in suit_counts.items() if count >= door][0]
        # Karte iste boje sa stola i ruke
        flush_cards = [card for card in all_cards if card[1] == flush_suit]
        # Sortiranje karata po vrednosti
        sorted_flush_cards = sorted(flush_cards, key=lambda x: value_map[x[0]])
        # Izbor 5 najjačih karata
        strongest_flush_cards = sorted_flush_cards[:5]
        # Prolazak kroz svaku kartu u strongest_flush_cards i proveravanje da li je ista kao karta u ruci
        for card in strongest_flush_cards:
            if card in hand:
                # Ako je karta u ruci, vraćamo x-high flush
                highest_flush_card = card[0]  # najjača karta iz ruke
                return highest_flush_card
        
        # Ako nema karata iz ruke, to je Board Flush
        return 1
    return 0

# Funkcija koja pronalazi Straight (kent) i prepoznaje x-high straight ili board straight
def is_straight(hand, board):
    # Vrednosti karata od A do 2
    valid_values = "AKQJT98765432"
    
    hand=[card[0] for card in hand]
    board=[card[0] for card in board]
    cards = hand + board
    cards = [card[0] for card in cards]
    
    # Mogući nizovi za kentu (5 uzastopnih karata)
    possible_straights = [
        ['A', 'K', 'Q', 'J', 'T'],
        ['K', 'Q', 'J', 'T', '9'],
        ['Q', 'J', 'T', '9', '8'],
        ['J', 'T', '9', '8', '7'],
        ['T', '9', '8', '7', '6'],
        ['9', '8', '7', '6', '5'],
        ['8', '7', '6', '5', '4'],
        ['7', '6', '5', '4', '3'],
        ['6', '5', '4', '3', '2'],
        ['5', '4', '3', '2', 'A']
    ]
    
    # Proveri sve karte u nizu
    for straight in possible_straights:
        count = 0
        for value in straight:
            if value in cards:
                count +=1
        if count == 5:
            hand_values=[card[0] for card in hand]
            hand_values = sorted(hand_values, key=lambda x: valid_values.index(x))
            
            # Ako postoji karta iz ruke među ovih 5, prepoznajemo kao x-high straight
            for card in straight[0:4]:
                if card in hand and not card in board:
                    return f"{straight[0]}-high straight", straight
            if straight[4] in hand and not straight[4]in board:
                return f"{straight[0]}-high idiot end straight", straight
            return "Board straight", straight
    
    return []  # Ako nije pronađen Straight

def is_trips(hand, board):
    # Kombinujemo ruku i board
    cards = hand + board
    
    # Brojanje vrednosti karata
    value_counts = Counter(card[0] for card in cards)
    max_value = max(value_counts, key=value_counts.get)
    if value_counts[max_value] < 3:
        return "No Trips or Set"
    
    trips_value = [key for key, count in value_counts.items() if count == 3]
    
    # Proveri za Set (par u ruci i treća karta na stolu)
    if trips_value[0] == hand[0][0] and trips_value[0] == hand[1][0]:
        return f"Set: {trips_value[0]}"
    
    # Proveri za Trips (različite karte u ruci i par na stolu)
    if trips_value[0] == hand[0][0] or trips_value[0] == hand[1][0]:
        # Odaberi ruku koju čine trips
        trips_cards = [card for card in cards if card[0] == trips_value[0]]
        
        # Dodaj dve najjače karte sa stola (koje nisu već deo trips)
        remaining_cards = [card for card in cards if card[0] != trips_value[0]]
        sorted_remaining_cards = sorted(remaining_cards, key=lambda x: "AKQJT98765432".index(x[0]))
        strongest_5_cards = trips_cards + sorted_remaining_cards[:2]  # Prvih 2 najjače karte
        
        # Sada proveravamo da li kicker iz ruke dolazi među 5 najjačih karata
        kicker = None
        for card in hand:
            if card[0] != trips_value[0] and card in strongest_5_cards:
                kicker = card[0]
                break
        
        if kicker:
            return f"Trips: {trips_value[0]}, Kicker: {kicker}"
        else:
            return f"Trips: {trips_value[0]}, No kicker"
    
    return f"Board Trips: {trips_value[0]}"

def is_two_pair(hand, board):
        
    # Kombinujemo ruku i board
    cards = sorted(hand + board, key=lambda x: "AKQJT98765432".index(x[0])) 
    
    # Brojanje vrednosti karata
    value_counts = Counter(card[0] for card in cards)
    
    # Pronaći vrednosti koje se pojavljuju dva puta
    two_pair_values = [key for key, count in value_counts.items() if count == 2]
    two_pair_values = two_pair_values[:2]
    
    # 1. Par u ruci i par na stolu
    if len(two_pair_values) == 2 and (hand[0][0] == hand[1][0] and hand[0][0] in two_pair_values):
        return f"Two Pair: {hand[0][0]} on paired board"
    
    # 2. Obe karte u ruci prave po par
    if len(two_pair_values) >= 2 and hand[0][0] in two_pair_values and hand[1][0] in two_pair_values:
        return f"Two Pair: {hand[0][0]} and {hand[1][0]}"
    
    # 3. Dva para na stolu
    if len(two_pair_values) >= 2 and not hand[0][0] in two_pair_values and not hand[1][0] in two_pair_values:
        return f"Board Two Pair: {two_pair_values[0]} and {two_pair_values[1]}"
    
    # 4. Različite karte u ruci i par na stolu + kicker
    if len(two_pair_values) == 2 and (hand[0][0] in two_pair_values or hand[1][0] in two_pair_values):
        made_pair = hand.copy()
        if hand[1][0] in two_pair_values:
            made_pair[0] = made_pair[1]
        else:
            made_pair[1] = made_pair[0]
        kicker=is_kicker(made_pair, hand, board)
        if kicker==0:
            return f"Two Pair: {made_pair[0][0]} on paired board, no kicker"
        else:
            return f"Two Pair: {made_pair[0][0]} on paired board, kicker: {kicker}"
    
    return "No Two Pair"

def is_one_pair(hand, board):
    # Kombinujemo ruku i board
    cards = hand + board

    # Sortiranje karata po vrednosti
    sorted_board = sorted([card[0] for card in board], key=lambda x: "AKQJT98765432".index(x))
    cards = sorted([card[0] for card in cards], key=lambda x: "AKQJT98765432".index(x))
    hand = sorted([card[0] for card in hand], key=lambda x: "AKQJT98765432".index(x))
    
    value_counts = Counter(card[0] for card in cards)
    board_counts = Counter(card[0] for card in board)
    
    # Pronaći sve karte koje se pojavljuju dva puta
    pairs_on_board = [key for key, count in board_counts.items() if count == 2]
    if len(pairs_on_board)>0:
        result = ", on paired board."
    else:
        result = ""
    
    # Pronaći par u ruci
    hand_pair=[]
    for card in hand:
        if card[0] in value_counts and value_counts[card[0]]==2:
            hand_pair=card[0]
            break
    if len(hand_pair)==0:
        return "No pair"
    
    made_pair = [hand_pair, hand_pair]
    kicker = is_kicker(made_pair,hand,board)
    kicker_text = f", kicker: {kicker}"
    if kicker==0:
        kicker_text = ", no kicker"
    if hand[0]==hand[1]:
        kicker_text = ""
    
    # Ako imamo par u ruci koji je jači od svih karata na stolu (Overpair)
    if value_order.index(hand_pair) < value_order.index(sorted_board[0]):
        return f"Overpair: {hand_pair}" + result
    
    # Ako je par iz ruke najjači na stolu (top pair)
    if value_order.index(hand_pair) == value_order.index(sorted_board[0]):
        return f"Top Pair: {hand_pair}" + result + kicker_text
    
    # Ako je par iz ruke drugi po jačini na stolu (second pair)
    if value_order.index(hand_pair) <= value_order.index(sorted_board[1]):
        return f"Second Pair: {hand_pair}" + result + kicker_text

    # Ako je par iz ruke treći po jačini na stolu (third pair)
    if value_order.index(hand_pair) <= value_order.index(sorted_board[2]):
        return f"Third Pair: {hand_pair}" + result + kicker_text

    # Ako je par iz ruke niži od trećeg para na stolu (low pair)
    return f"Low Pair: {hand_pair}" + result + kicker_text

# Funkcija za prepoznavanje Poker ruke (Straight Flush, Poker, Full House, Flush, Straight)
def evaluate_hand(hand, board):
    
    # Sortiranje karata:
    hand = sorted(hand, key=lambda x: "AKQJT98765432".index(x[0])) 
    board = sorted(board, key=lambda x: "AKQJT98765432".index(x[0])) 

    # Kombinujemo karte sa stola i ruke
    all_cards = hand + board
    value_counts = Counter(card[0] for card in all_cards)

    # 1. Provera za Straight Flush
    straight_flush_result = is_straight_flush(all_cards)
    if straight_flush_result:
        return straight_flush_result[0]  # Vraća "Royal Flush" ili "Straight Flush"

    # 2. Provera za Poker (Four of a Kind)
    if 4 in value_counts.values():
        four_of_a_kind_value = [key for key, count in value_counts.items() if count == 4][0]
        return f"Poker: {four_of_a_kind_value}"

    # 3. Provera za Full House
    if 3 in value_counts.values() and 2 in value_counts.values():
        three_of_a_kind_value = [key for key, count in value_counts.items() if count == 3][0]
        pair_value = [key for key, count in value_counts.items() if count == 2][0]
        return f"Full House: {three_of_a_kind_value} over {pair_value}"

    # 4. Provera za Flush
    flush_result = is_flush(hand, board, 5)
	
    if flush_result == 1:
    	return "Board Flush"
    elif not flush_result == 0:
    	return f"Flush: {flush_result}-high"

    # 5. Provera za Straight (na kraju)
    straight_result = is_straight(hand, board)
    if straight_result:
        return straight_result[0] # Vraća "x-high straight" ili "Board straight"

    # 6. Provera za Triling
    triling_result = is_trips(hand, board)
    if not "No Trips" in triling_result:
        return triling_result

    # 7. Provera za 2 para
    two_pair = is_two_pair(hand, board)
    if not "No Two" in two_pair:
        return two_pair

    # 8. Provera za 1 par
    return is_one_pair(hand, board)

def calculate_straight_outs(hand, board):
    ranks = 'AKQJT98765432'
    rank_count = Counter(card[0] for card in hand + board)
    
    outs = 0
    for rank in ranks:
        card = [(rank, 'h')]
        straight = is_straight(hand, board + card)
        if straight and not "idiot" in straight[0]:
            outs += 4
            # Provera za Board flush draw
            suit_count = Counter(card[-1] for card in board)
            for suit, count in suit_count.items():
                if count == 3:  # Ako imamo flush draw na boardu
                    outs -= 1
    return outs

def is_full_house_draw(hand, board):
    all_cards = hand + board
    rank_count = Counter(card[0] for card in all_cards)
    
    flush_draw=is_flush([], board, 4)
    
    if 3 in rank_count.values():
        if not flush_draw == 0:# or calculate_straight_outs(board)>0:
            return True
    return False

def identify_draws(hand, board):
    draws = []
    
    #Ako imamo veoma jaku ruku, draw je dead, pa se ne računa.
    made_hand = evaluate_hand(hand, board)
    if " Flush" in made_hand or "Poker" in made_hand or "Full" in made_hand or "Board" in made_hand:
        return draws
    
    #Ako je Flush, samo Full house draw je bitan.
    if is_full_house_draw(hand, board):
        draws.append("Full house draw")
    if "Flush" in made_hand:
        return draws
    
    flush_draw=is_flush(hand, board, 4)
    if flush_draw == 1:
        draws.append("Board flush draw")
    elif not flush_draw == 0:
        draws.append(f"{flush_draw}-high flush draw")
    elif is_flush_draw(hand, board, 3)>1:
        draws.append(f"{flush_draw}-high backdoor flush draw")
    
    if "Straight" in made_hand:
        return draws
    
    straight_outs=calculate_straight_outs(hand, board)
    print(straight_outs)
    if straight_outs>3:
        draws.append(f"{straight_outs}-out straight draw")
    
    return draws

# Test primer
#hand = [('6', 'h'), ('7', 'h')]  
#board = [('Q', 'h'), ('9', 'h'), ('8', 'c'), ('4', 'c'), ('4', 's')]  
#print(evaluate_hand(hand, board))

#hand = [('6', 'h'), ('7', 'c')]  
#board = [('Q', 'h'), ('9', 'h'), ('8', 'h'), ('4', 'c')]  
#for draw in identify_draws(hand,board):
#    print(draw)
