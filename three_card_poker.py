import random

# Dec 22, 2022: Got the bets and calls for three card poker done.


def computer_fold(pot, p_score, c_score, p_card, c_card):
    p_score += pot
    print(f"My card was a {c_card} so I fold.\nYou win the pot of ${pot}\nYour score is {p_score} and mine is {c_score}." )
    pot = 0
    return pot, p_score

def player_win(pot, p_score, c_score, p_card, c_card):
    p_score += pot
    print(f"My card was a {c_card} so you win the pot of ${pot}\nYour score is {p_score} and mine is {c_score}." )
    pot = 0
    return pot, p_score

def computer_win(pot, p_score, c_score, p_card, c_card):
    c_score += pot
    print(f"My card was a {c_card} so I win the pot of ${pot}\nYour score is {p_score} and mine is {c_score}." )
    pot = 0
    return pot, c_score

def player_bet(pot, p_score, bet):
    return pot+bet, p_score-bet

def computer_bet(pot, c_score, bet):
    return pot+bet, c_score-bet

def play_round(p_score, c_score, ante, bet, chance):
    pot = 0

    value = input("Pick a card from Left, Middle, or Right. Press L, M, or R: ")
    
    pot     += ante + bet
    p_score -= bet
    c_score -= bet

    cards_p = ["K","Q","J"]
    p_card = chance.choice(cards_p)
    cards_c = [ c for c in cards_p if c!=p_card ]
    c_card = chance.choice(cards_c)
    
    print("your card is: ", p_card)
    
    assert c_card!=p_card, "ERROR:::::: The players have the same card!"

    v2 = input("Do you want to play first or second? Enter 1 or 2: ")
    
    if v2=="1":
        v3 = input("Do you want to bet? Y/N: ")
        if v3=="Y" or v3=="y":
            pot += bet; p_score -= bet
            if c_card=="K":
                pot, c_score = computer_bet(pot, c_score, bet)
                pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
            elif c_card=="Q":
                to_bet_or_not = chance.choice([1,2,3])
                if to_bet_or_not==1:
                    pot, c_score = computer_bet(pot, c_score, bet)
                    pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
                else:
                    pot, p_score = computer_fold(pot, p_score, c_score, p_card, c_card)
            else:
                pot, p_score = computer_fold(pot, p_score, c_score, p_card, c_card)
        else:
            pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
    elif v2=="2":
        if c_card=="K":
            pot, c_score = computer_bet(pot, c_score, bet)
            resp = input("I bet. Do you want to call? Y/N:")
            if resp=="Y" or resp=="y":
                pot, p_score = player_bet(pot, p_score, bet)
                pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
            else:
                pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
        elif c_card=="Q":
            pot, c_score = computer_bet(pot, c_score, bet)
            resp = input("I bet. Do you want to call? Y/N:")
            if resp=="Y" or resp=="y":
                pot, p_score = player_bet(pot, p_score, bet)
                if p_card=="K":
                    pot, p_score = player_win(pot, p_score, c_score, p_card, c_card)
                else: # p_card==J
                    pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
            else:
                pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
        else:  # c_card=="J"
            to_bet_or_not = chance.choice([1,2,3])
            if to_bet_or_not==1:
                pot, c_score = computer_bet(pot, c_score, bet)
                resp = input("I bet. Do you want to call? Y/N: ")
                if resp=="Y" or resp=="y":
                    pot, p_score = player_bet(pot, p_score, bet)
                    pot, p_score = player_win(pot, p_score, c_score, p_card, c_card)
                else:
                    pot, c_score = computer_win(pot, p_score, c_score, p_card, c_card)
            else:
                pot, p_score = computer_fold(pot, p_score, c_score, p_card, c_card)

    return p_score, c_score


if __name__=='__main__':
    resp = input("\nPress p to play:")
    p_score_main = 10
    c_score_main = 10
    ante_main    = 1
    bet_main     = 1
    chance = random.Random()
    while resp=="p":
        p_score_main,c_score_main = play_round(p_score_main,c_score_main,ante_main,bet_main,chance) 
        resp = input("\nPress p to play:")
    print("\nGood-bye!")
