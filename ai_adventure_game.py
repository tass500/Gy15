from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import random
from enum import Enum
from typing import List, Optional, Dict, Tuple

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
    TWO = (2, "2")
    THREE = (3, "3")
    FOUR = (4, "4")
    FIVE = (5, "5")
    SIX = (6, "6")
    SEVEN = (7, "7")
    EIGHT = (8, "8")
    NINE = (9, "9")
    TEN = (10, "10")
    JACK = (11, "J")
    QUEEN = (12, "Q")
    KING = (13, "K")
    ACE = (14, "A")

    def __init__(self, value: int, symbol: str):
        self._value_ = value
        self.symbol = symbol

class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank.symbol}{self.suit.value}"
    
    def __repr__(self):
        return str(self)

class HandRank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class PokerAI:
    def __init__(self):
        print("Betöltöm az AI modellt, kérlek várj...")
        self.pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta")
    
    def get_ai_decision(self, game_state: str) -> str:
        prompt = f"""
        [Rendszer]
        Te egy póker játékban vagy az AI játékos. A következő információkkal rendelkezel:
        {game_state}
        
        Válassz egy műveletet a következők közül:
        - 'call' (tartás)
        - 'raise' (emelés)
        - 'fold' (passz)
        
        Válaszolj CSAK a művelet nevével, semmi mással.
        
        Válasz: """
        
        response = self.pipe(prompt, max_new_tokens=10, do_sample=True, temperature=0.7)[0]['generated_text']
        decision = response.split("Válasz: ")[-1].strip().lower()
        
        # Basic validation
        if 'call' in decision:
            return 'call'
        elif 'raise' in decision:
            return 'raise'
        elif 'fold' in decision:
            return 'fold'
        return random.choice(['call', 'raise', 'fold'])

class PokerGame:
    def __init__(self):
        self.deck = []
        self.player_hand: List[Card] = []
        self.ai_hand: List[Card] = []
        self.community_cards: List[Card] = []
        self.pot = 0
        self.player_chips = 1000
        self.ai_chips = 1000
        self.current_bet = 0
        self.ai = PokerAI()
        self.initialize_deck()
    
    def initialize_deck(self):
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        random.shuffle(self.deck)
    
    def deal_initial_hands(self):
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.ai_hand = [self.deck.pop(), self.deck.pop()]
    
    def deal_community_cards(self, count: int):
        for _ in range(count):
            self.community_cards.append(self.deck.pop())
    
    def evaluate_hand(self, hand: List[Card]) -> Tuple[HandRank, List[int]]:
        all_cards = hand + self.community_cards
        ranks = sorted([card.rank._value_ for card in all_cards], reverse=True)
        suits = [card.suit for card in all_cards]
        
        # Hand evaluation logic (simplified)
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        
        # Check for flush
        flush = any(suits.count(suit) >= 5 for suit in Suit)
        
        # Check for straight
        unique_ranks = sorted(list(set(ranks)), reverse=True)
        straight = False
        straight_high = 0
        
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                straight = True
                straight_high = unique_ranks[i]
                break
        
        if set([14, 2, 3, 4, 5]).issubset(set(ranks)):
            straight = True
            straight_high = 5
        
        if flush and straight:
            if set([10, 11, 12, 13, 14]).issubset(set(ranks)):
                return (HandRank.ROYAL_FLUSH, [14])
            return (HandRank.STRAIGHT_FLUSH, [straight_high])
        
        if 4 in rank_counts.values():
            quad_rank = [rank for rank, count in rank_counts.items() if count == 4][0]
            kicker = max(rank for rank in ranks if rank != quad_rank)
            return (HandRank.FOUR_OF_A_KIND, [quad_rank, kicker])
        
        if sorted(rank_counts.values()) == [2, 3]:
            trips = [rank for rank, count in rank_counts.items() if count == 3][0]
            pair = [rank for rank, count in rank_counts.items() if count == 2][0]
            return (HandRank.FULL_HOUSE, [trips, pair])
        
        if flush:
            flush_suit = [suit for suit in Suit if suits.count(suit) >= 5][0]
            flush_ranks = sorted([card.rank._value_ for card in all_cards if card.suit == flush_suit], reverse=True)[:5]
            return (HandRank.FLUSH, flush_ranks)
        
        if straight:
            return (HandRank.STRAIGHT, [straight_high])
        
        if 3 in rank_counts.values():
            trips = [rank for rank, count in rank_counts.items() if count == 3][0]
            kickers = sorted([rank for rank in ranks if rank != trips], reverse=True)[:2]
            return (HandRank.THREE_OF_A_KIND, [trips] + kickers)
        
        pairs = [rank for rank, count in rank_counts.items() if count == 2]
        if len(pairs) >= 2:
            pairs = sorted(pairs, reverse=True)[:2]
            kicker = max(rank for rank in ranks if rank not in pairs)
            return (HandRank.TWO_PAIR, pairs + [kicker])
        
        if len(pairs) == 1:
            pair_rank = pairs[0]
            kickers = sorted([rank for rank in ranks if rank != pair_rank], reverse=True)[:3]
            return (HandRank.PAIR, [pair_rank] + kickers)
        
        return (HandRank.HIGH_CARD, sorted(ranks, reverse=True)[:5])
    
    def compare_hands(self) -> int:
        player_rank, player_values = self.evaluate_hand(self.player_hand)
        ai_rank, ai_values = self.evaluate_hand(self.ai_hand)
        
        if player_rank.value > ai_rank.value:
            return 1
        elif ai_rank.value > player_rank.value:
            return -1
        else:
            for p_val, a_val in zip(player_values, ai_values):
                if p_val > a_val:
                    return 1
                elif a_val > p_val:
                    return -1
            return 0
    
    def get_game_state_for_ai(self) -> str:
        return f"""
        Te egy póker játékban vagy. Itt a jelenlegi állás:
        - Közös kártyák: {', '.join(str(card) for card in self.community_cards) or 'Még nincsenek közös kártyák'}
        - A te kezed: {', '.join(str(card) for card in self.ai_hand)}
        - Pot: {self.pot} zseton
        - Jelenlegi tét: {self.current_bet} zseton
        - A játékos emelt: {self.current_bet} zseton
        """
    
    def play_round(self):
        print("\n=== Új kör kezdődik! ===")
        print(f"A te zsetonjaid: {self.player_chips} | AI zsetonjai: {self.ai_chips}")
        
        # Reset game state
        self.deck = [Card(suit, rank) for suit in Suit for rank in Rank]
        random.shuffle(self.deck)
        self.community_cards = []
        self.current_bet = 0
        self.pot = 0
        
        # Deal initial hands
        self.deal_initial_hands()
        
        # Pre-flop betting
        print("\n--- Pre-flop ---")
        print(f"A te kártyáid: {', '.join(str(card) for card in self.player_hand)}")
        
        if not self.betting_round():
            return  # Round ended due to fold
        
        # Flop
        print("\n--- Flop ---")
        self.deal_community_cards(3)
        print(f"Közös kártyák: {', '.join(str(card) for card in self.community_cards)}")
        print(f"A te kártyáid: {', '.join(str(card) for card in self.player_hand)}")
        
        if not self.betting_round():
            return
        
        # Turn
        print("\n--- Turn ---")
        self.deal_community_cards(1)
        print(f"Közös kártyák: {', '.join(str(card) for card in self.community_cards)}")
        print(f"A te kártyáid: {', '.join(str(card) for card in self.player_hand)}")
        
        if not self.betting_round():
            return
        
        # River
        print("\n--- River ---")
        self.deal_community_cards(1)
        print(f"Közös kártyák: {', '.join(str(card) for card in self.community_cards)}")
        print(f"A te kártyáid: {', '.join(str(card) for card in self.player_hand)}")
        
        if not self.betting_round():
            return
        
        # Showdown
        self.showdown()
    
    def betting_round(self) -> bool:
        self.current_bet = 0
        
        # Player's turn
        while True:
            print(f"\nPot: {self.pot} zseton | Jelenlegi tét: {self.current_bet} zseton")
            print("Válassz: call, raise, fold")
            action = input("Te cselekszel: ").lower().strip()
            
            if action == "fold":
                print("Összecsuktad a kártyádat! Az AI nyeri a kört!")
                self.ai_chips += self.pot
                self.pot = 0
                return False
            elif action == "call":
                call_amount = self.current_bet
                if call_amount > self.player_chips:
                    print("Nincs elég zsetonod!")
                    continue
                self.player_chips -= call_amount
                self.pot += call_amount
                print(f"Tartasz {call_amount} zsetonért")
                break
            elif action == "raise":
                try:
                    amount = int(input("Mennyivel emelsz? "))
                    total_bet = self.current_bet + amount
                    if total_bet > self.player_chips:
                        print("Nincs elég zsetonod!")
                        continue
                    self.player_chips -= total_bet
                    self.pot += total_bet
                    self.current_bet = total_bet
                    print(f"{total_bet} zsetonra emelsz")
                    break
                except ValueError:
                    print("Kérlek számot adj meg!")
            else:
                print("Érvénytelen választás. Válassz a következőkből: call, raise, fold")
        
        # AI's turn
        print("\nAz AI gondolkozik...")
        game_state = self.get_game_state_for_ai()
        ai_action = self.ai.get_ai_decision(game_state)
        
        if ai_action == "fold":
            print("Az AI összecsukta! Te nyerted a kört!")
            self.player_chips += self.pot
            self.pot = 0
            return False
        elif ai_action == "call":
            call_amount = min(self.current_bet, self.ai_chips)
            self.ai_chips -= call_amount
            self.pot += call_amount
            print(f"Az AI tart {call_amount} zsetonért")
        elif ai_action == "raise":
            max_raise = min(self.ai_chips, self.current_bet * 2)
            if max_raise > 0:
                ai_raise = random.randint(1, max_raise)
                total_bet = self.current_bet + ai_raise
                self.ai_chips -= total_bet
                self.pot += total_bet
                self.current_bet = total_bet
                print(f"Az AI {total_bet} zsetonra emel")
                return self.betting_round()
            else:
                call_amount = min(self.current_bet, self.ai_chips)
                self.ai_chips -= call_amount
                self.pot += call_amount
                print(f"Az AI tart {call_amount} zsetonért")
        
        return True
    
    def showdown(self):
        print("\n--- Showdown! ---")
        print(f"A te kártyáid: {', '.join(str(card) for card in self.player_hand)}")
        print(f"Az AI kártyái: {', '.join(str(card) for card in self.ai_hand)}")
        print(f"Közös kártyák: {', '.join(str(card) for card in self.community_cards)}")
        
        result = self.compare_hands()
        
        if result > 0:
            print("\nTe nyerted a kört!")
            self.player_chips += self.pot
        elif result < 0:
            print("\nAz AI nyerte a kört!")
            self.ai_chips += self.pot
        else:
            print("\nDöntetlen! A pot megosztva.")
            self.player_chips += self.pot // 2
            self.ai_chips += (self.pot + 1) // 2
        
        self.pot = 0
        print(f"A te zsetonjaid: {self.player_chips} | AI zsetonjai: {self.ai_chips}")

def main():
    print("=== Üdvözöllek a Póker játékban! ===")
    print("Játssz az AI ellen Texas Hold'em pókerben.")
    print("Minden körben 100 zsetonnal kezdesz. Sok szerencsét!\n")
    
    game = PokerGame()
    
    while True:
        game.play_round()
        
        if game.player_chips <= 0:
            print("\nKifogytál a zsetonokból! Vége a játéknak.")
            break
        if game.ai_chips <= 0:
            print("\nKifogyott az AI zsetonja! Nyertél!")
            break
        
        play_again = input("\nSzeretnél még egy kört játszani? (i/n): ").lower()
        if play_again != 'i':
            break
    
    print("\nKöszönöm, hogy játszottál!")
    print(f"Végeredmény - Te: {game.player_chips} zseton | AI: {game.ai_chips} zseton")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Hiba történt: {e}")
        print("Sajnálom, valami hiba történt a játék közben.")
