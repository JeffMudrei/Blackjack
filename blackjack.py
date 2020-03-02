# Embaralhas cartas
import random

playing = False
chip_pool = 100

bet = 1

restart_phrase = "Aperte 'd' para embaralhar novamente ou aperte 'q' para sair."

suits = ('Copas', 'Ouro', 'Paus', 'Espada')
ranking = ('A', '2', '3', '4', '5', '6', '7', '8','9', '10', 'J', 'Q', 'K')

card_val = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank

    def grab_suit(self):
        return self.suit

    def grab_rank(self):
        return self.rank

    def draw(self):
        print(self.suit + self.rank)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = False

    def __str__(self):
        hand_comp = ""

        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name

        return "A mão tem {}".format(hand_comp)

    def card_add(self, card):
        self.cards.append(card)

        if card.rank == 'A':
            self.ace = True
        self.value += card_val[card.rank]

    def calc_val(self):
        if (self.ace == 'True' and self.value < 12):
            return self.value + 10
        else:
            return self.value

    def draw(self, hidden):
        if hidden == True and playing == True:
            starting_card = 1
        else:
            starting_card = 0
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()


class Deck:

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += " " + card.__str__()

        return "O baralho tem " + deck_comp


def make_bet():
    global bet
    bet = 0

    print("Qual a quantidade de fichas que você gostaria de apostar? (Informe um numero inteiro, por favor)")

    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)

        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print("Aposta invalida. você possui " + str(chip_pool) + " fichas restantes.")


def deal_cards():
    global result, playing, deck, player_hand, dealer_hand, chip_pool, bet

    deck = Deck()
    deck.shuffle()

    make_bet()

    player_hand = Hand()
    dealer_hand = Hand()

    # 2 Cartas para o Jogador
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())

    # 2 Cartas para o Dealer
    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())

    result = "Apostar(digite 'h') ou parar(digite 's')? :"

    playing = True
    game_step()


def hit():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    if playing:
        if player_hand.calc_val() <= 21:
            player_hand.card_add(deck.deal())
        print("Mão do jogador é %s" % player_hand)

        if player_hand.calc_val() >= 21:
            result = "Estourou! " + restart_phrase
            chip_pool -= bet
            playing = False

    else:
        result = "Desculpe, não pode bater! " + restart_phrase

    game_step()


def stand():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    if playing == False:
        if player_hand.calc_val() > 0:
            result = "Desculpe, não pode continuar!"

    else:
        while dealer_hand.calc_val() < 17:
            dealer_hand.card_add(deck.deal())

        if dealer_hand.calc_val() > 21:
            result = "Dealer estourou, você venceu! " + restart_phrase
            chip_pool += bet
            playing = False

        elif dealer_hand.calc_val() < player_hand.calc_val():
            result = "Sua mão é melhor que a do dealer! Você venceu!!!!" + restart_phrase
            chip_pool += bet
            playing = False

        elif dealer_hand.calc_val() == player_hand.calc_val():
            result = "Empate! " + restart_phrase
            playing = False

        else:
            result = 'Dealer venceu! ' + restart_phrase
            chip_pool -= bet
            playing = False
    game_step()


def game_step():
    print("")
    print("Mão do jogador é:")
    player_hand.draw(hidden=False)
    print("O total da mão do jogador é: " + str(player_hand.calc_val()))

    print("")
    print("A mão do dealer é: ")
    dealer_hand.draw(hidden=True)
    print("O total da mao do dealer é: " + str(dealer_hand.calc_val()))

    if playing == False:
        print("Total de fichas: " + str(chip_pool))

    print(result)

    player_input()


def game_exit():
    print("Obrigado por jogar!!")
    exit()


def player_input():
    plin = input().lower()

    if plin == 'h':
        hit()
    elif plin == 's':
        stand()
    elif plin == 'd':
        deal_cards()
    elif plin == 'q':
        game_exit()
    else:
        print("Entrada invalida... Insira 'h', 's', 'd' ou 'q': ")
        player_input()

def intro():
    print('-'*100)
    statement = """    Bem-vindo ao BlackJack! Chegue o mais perto possível dos 21 sem estourar!
    O dealer pedira cartas ate que chegue a 17. Os ases contam como 1 ou 11.
    As cartas são contadas de acordo com a notação
    Você inicia com 100 fichas."""
    print(statement)
    print('-'*100)



deck = Deck()
deck.shuffle()

player_hand = Hand()
dealder_hand = Hand()

intro()
deal_cards()