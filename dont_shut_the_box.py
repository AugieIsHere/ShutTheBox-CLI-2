import random
import time
import os
import sys
from typing import List, Dict, Tuple, Optional
from animations import (
    clear_screen, animate_text, animate_game_title, show_loading_bar, 
    animate_dice_roll, animate_box_closing, celebrate_win,
    draw_sidebar, clear_main_area, move_to_main_area,
    sidebar_animate_dice_roll, sidebar_animate_box_closing, sidebar_celebrate_win
)

class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.is_ai = is_ai
        self.total_score = 0
        self.board = list(range(1, 10))  # Numbers 1-9
        self.index = 0  # Player index in the game
        
    def reset_board(self):
        """Reset the player's board for a new round"""
        self.board = list(range(1, 10))
        
    def shut_number(self, number: int):
        """Shut a number on the board"""
        if number in self.board:
            self.board.remove(number)
            
    def get_available_numbers(self) -> List[int]:
        """Get the list of numbers that are still available (not shut)"""
        return self.board.copy()
        
    def make_decision(self, dice_sum: int, available_numbers: List[int], combinations: List[List[int]]) -> List[int]:
        """Make a decision on which numbers to shut based on the dice sum and available numbers"""
        raise NotImplementedError("Subclasses must implement this method")

class HumanPlayer(Player):
    def __init__(self, name: str, advanced_mode: bool):
        super().__init__(name, is_ai=False)
        self.advanced_mode = advanced_mode
    
    def make_decision(self, dice_sum: int, available_numbers: List[int], combinations: List[List[int]]) -> List[int]:
        """Let the human player make a decision"""
        # This method is not used directly for human players - the game handles the user input
        # But we provide a simple implementation for consistency
        if not combinations:
            return []
        
        print("Valid combinations:")
        for i, combo in enumerate(combinations, 1):
            print(f"{i}. {combo}")
            
        while True:
            try:
                choice = int(input("Enter the number of your choice (0 to end turn): "))
                if choice == 0:
                    return []
                if 1 <= choice <= len(combinations):
                    return combinations[choice - 1]
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")

class AIPlayer(Player):
    def __init__(self, name: str = "AI", difficulty: str = "medium", advanced_mode: bool = False):
        super().__init__(name, is_ai=True)
        self.difficulty = difficulty
        self.advanced_mode = advanced_mode
    
    def make_decision(self, dice_sum: int, available_numbers: List[int], combinations: List[List[int]]) -> List[int]:
        """Make a decision on which numbers to shut based on AI difficulty"""
        if not combinations:
            return []
        
        if self.difficulty == "easy":
            # Easy AI - randomly choose from valid combinations
            return random.choice(combinations)
        elif self.difficulty == "medium":
            # Medium AI - prefer shutting more numbers at once
            max_len = max(len(combo) for combo in combinations)
            best_combos = [combo for combo in combinations if len(combo) == max_len]
            return random.choice(best_combos)
        else:  # hard
            # First prioritize shutting 7, 8, 9 if possible
            high_priority = [7, 8, 9]
            
            # Find combinations that include high priority numbers
            combos_with_high_priority = []
            for combo in combinations:
                if any(num in high_priority for num in combo):
                    combos_with_high_priority.append(combo)
            
            if combos_with_high_priority:
                # Find the one that shuts the most numbers
                max_len = max(len(combo) for combo in combos_with_high_priority)
                best_combos = [combo for combo in combos_with_high_priority if len(combo) == max_len]
                return max(best_combos, key=lambda x: sum(x))
            
            # If no high priority numbers can be shut, maximize number of shut tiles
            max_len = max(len(combo) for combo in combinations)
            best_combos = [combo for combo in combinations if len(combo) == max_len]
            return max(best_combos, key=lambda x: sum(x))

class Game:
    def __init__(self, players: List[Player], advanced_mode: bool = False):
        self.players = players
        self.current_player_idx = 0
        self.advanced_mode = advanced_mode
        self.max_number = 9
        
        # Set player indexes for sidebar reference
        for i, player in enumerate(players):
            player.index = i
    
    def current_player(self) -> Player:
        """Get the current player"""
        return self.players[self.current_player_idx]
    
    def next_player(self):
        """Move to the next player"""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
    
    def display_board(self, player: Player):
        """Display the player's board"""
        available_numbers = player.get_available_numbers()
        closed = [n for n in range(1, self.max_number + 1) if n not in available_numbers]
        
        board_display = " ".join(str(n) for n in range(1, self.max_number + 1))
        status_display = " ".join("X" if n in closed else "O" for n in range(1, self.max_number + 1))
        
        print(f"\n{player.name}'s board:")
        print(board_display)
        print(status_display)
        print(f"Open numbers: {available_numbers}")
    
    def get_sidebar_data(self) -> Dict:
        """Get data for sidebar display"""
        data = {
            "players": [p.name for p in self.players],
            "boards": [p.get_available_numbers() for p in self.players],
            "scores": [p.total_score for p in self.players],
            "active_player": self.current_player().name,
            "max_number": self.max_number
        }
        return data
    
    def roll_dice(self, num_dice: int = 2, game_data: Dict = None) -> int:
        """Roll the specified number of dice and return the sum"""
        if num_dice not in [1, 2]:
            raise ValueError("Can only roll 1 or 2 dice")
        
        if self.advanced_mode and game_data:
            return sidebar_animate_dice_roll(num_dice, 1.0, game_data)
        else:
            return animate_dice_roll(num_dice, 1.0)
    
    def play_turn(self, player: Player) -> int:
        """Play a single turn for the given player"""
        if self.advanced_mode:
            clear_main_area()
        else:
            clear_screen()
        
        # Display whose turn it is
        print(f"\n{player.name}'s turn")
        
        # Display the player's board
        available_numbers = player.get_available_numbers()
        
        if not available_numbers:  # All numbers are shut
            print("All numbers are shut! Perfect round!")
            return 0
        
        # Show the player's board
        self.display_board(player)
        
        # Check if player can use single die
        can_use_single_die = all(n not in available_numbers for n in [7, 8, 9])
        
        # Determine how many dice to roll
        num_dice = 2
        if can_use_single_die and available_numbers and max(available_numbers) <= 6:
            if player.is_ai:
                # AI always chooses 1 die when possible for best odds
                num_dice = 1
                print(f"{player.name} chooses to roll 1 die (numbers 7-9 are shut)")
            else:
                choice = input("All numbers 7-9 are shut. Do you want to roll 1 die instead of 2? (y/n): ").lower()
                num_dice = 1 if choice.startswith('y') else 2
        
        # Roll the dice
        if self.advanced_mode:
            dice_sum, dice_values = sidebar_animate_dice_roll(
                num_dice, 0.8 if player.is_ai else 1.0,
                self.get_sidebar_data()
            )
        else:
            dice_sum, dice_values = animate_dice_roll(num_dice, 0.8 if player.is_ai else 1.0)
        
        print(f"Rolled: {dice_sum}")
        
        turn_ended = False
        while not turn_ended:
            available_numbers = player.get_available_numbers()
            valid_combinations = find_valid_combinations(dice_sum, available_numbers)
            
            if not valid_combinations:
                print(f"No valid moves for {dice_sum}.")
                score = sum(available_numbers)
                print(f"Turn ends with score: {score}")
                return score
            
            # Get player decision
            if player.is_ai:
                # Add a delay to make it seem like the AI is thinking
                time.sleep(1)
                numbers_to_shut = player.make_decision(dice_sum, available_numbers, valid_combinations)
                print(f"{player.name} chooses: {numbers_to_shut}")
            else:
                # Display valid combinations to human player
                print("Valid combinations:")
                for i, combo in enumerate(valid_combinations, 1):
                    print(f"{i}. {combo}")
                
                while True:
                    try:
                        choice = int(input("Enter the number of your choice (0 to end turn): "))
                        if choice == 0:
                            score = sum(available_numbers)
                            print(f"Turn ends with score: {score}")
                            return score
                        if 1 <= choice <= len(valid_combinations):
                            numbers_to_shut = valid_combinations[choice - 1]
                            break
                        print("Invalid choice. Try again.")
                    except ValueError:
                        print("Please enter a number.")
            
            # Animate shutting the chosen numbers
            if self.advanced_mode:
                sidebar_animate_box_closing(
                    numbers_to_shut, player.get_available_numbers(),
                    player.index, self.get_sidebar_data()
                )
            else:
                animate_box_closing(numbers_to_shut, player.get_available_numbers())
            
            # Shut the numbers
            for num in numbers_to_shut:
                player.shut_number(num)
            
            # Check if all numbers are shut
            if not player.get_available_numbers():
                print(f"{player.name} has shut the box! Perfect round!")
                if self.advanced_mode:
                    sidebar_celebrate_win(player.name, self.get_sidebar_data())
                else:
                    celebrate_win()
                return 0
            
            # Show the updated board
            self.display_board(player)
            
            # Roll again
            print(f"{player.name} rolls again...")
            
            # Check if can use single die
            can_use_single_die = all(n not in player.get_available_numbers() for n in [7, 8, 9])
            
            num_dice = 2
            if can_use_single_die and player.get_available_numbers() and max(player.get_available_numbers()) <= 6:
                if player.is_ai:
                    num_dice = 1
                    print(f"{player.name} chooses to roll 1 die (numbers 7-9 are shut)")
                else:
                    choice = input("All numbers 7-9 are shut. Do you want to roll 1 die instead of 2? (y/n): ").lower()
                    num_dice = 1 if choice.startswith('y') else 2
            
            # Roll the dice
            if self.advanced_mode:
                dice_sum, dice_values = sidebar_animate_dice_roll(
                    num_dice, 0.8 if player.is_ai else 1.0,
                    self.get_sidebar_data()
                )
            else:
                dice_sum, dice_values = animate_dice_roll(num_dice, 0.8 if player.is_ai else 1.0)
            
            print(f"Rolled: {dice_sum}")
    
    def play_game(self, num_rounds: int = 3):
        """Play the game for the specified number of rounds"""
        for round_num in range(1, num_rounds + 1):
            if self.advanced_mode:
                clear_screen()
                print(f"=== ROUND {round_num} of {num_rounds} ===")
            else:
                clear_screen()
                print(f"=== ROUND {round_num} of {num_rounds} ===")
            
            # Display current scores
            print("\nCurrent scores:")
            for player in self.players:
                print(f"{player.name}: {player.total_score}")
            
            # Reset boards for each player
            for player in self.players:
                player.reset_board()
            
            # Determine starting player with highest dice roll
            print("\nRolling to determine who goes first...")
            
            # Roll for each player
            rolls = {}
            for player in self.players:
                if self.advanced_mode:
                    roll_sum, roll_values = sidebar_animate_dice_roll(2, 0.8 if player.is_ai else 1.0, self.get_sidebar_data())
                else:
                    roll_sum, roll_values = animate_dice_roll(2, 0.8 if player.is_ai else 1.0)
                rolls[player] = roll_sum
                print(f"{player.name} rolled {roll_sum}")
            
            # Find player with highest roll
            starting_player = max(rolls, key=lambda player: rolls[player])
            print(f"{starting_player.name} goes first.")
            
            # Set current player
            self.current_player_idx = self.players.index(starting_player)
            
            # Each player takes a turn
            for _ in range(len(self.players)):
                player = self.current_player()
                round_score = self.play_turn(player)
                player.total_score += round_score
                self.next_player()
            
            # Round summary
            if self.advanced_mode:
                clear_screen()
            else:
                clear_screen()
            
            print(f"\n=== Round {round_num} Results ===")
            for player in self.players:
                print(f"{player.name}: {player.total_score}")
            
            if round_num < num_rounds:
                input("\nPress Enter to continue to the next round...")
        
        # Game over - find winner
        winner = min(self.players, key=lambda player: player.total_score)
        
        if self.advanced_mode:
            clear_screen()
        else:
            clear_screen()
        
        print("\n=== GAME OVER ===")
        print(f"Final scores after {num_rounds} rounds:")
        for player in self.players:
            print(f"{player.name}: {player.total_score}")
        
        print(f"\n{winner.name} wins!")
        
        if self.advanced_mode:
            sidebar_celebrate_win(winner.name, self.get_sidebar_data())
        else:
            celebrate_win()

def find_valid_combinations(dice_sum: int, available_numbers: List[int]) -> List[List[int]]:
    """Find all valid combinations of available numbers that sum to dice_sum"""
    valid_combinations = []
    
    # If the dice sum itself is available, that's a valid option
    if dice_sum in available_numbers:
        valid_combinations.append([dice_sum])
    
    # Find all combinations of available numbers that sum to dice_sum
    find_combinations_recursive(dice_sum, available_numbers, [], valid_combinations)
    
    return valid_combinations

def find_combinations_recursive(target: int, numbers: List[int], current: List[int], results: List[List[int]]):
    """Recursively find all combinations of numbers that sum to target"""
    if target == 0:
        # Sort to avoid duplicates
        result = sorted(current)
        if result not in results:
            results.append(result)
        return
    
    if target < 0:
        return
    
    for i, num in enumerate(numbers):
        if num <= target:
            # Use this number
            find_combinations_recursive(
                target - num,
                numbers[:i] + numbers[i+1:],  # Remove the used number
                current + [num],
                results
            )

def display_welcome_screen() -> Tuple[str, str, int]:
    """Display welcome screen and get user preferences for the game."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("===== DON'T SHUT THE BOX =====")
    
    # Get player name
    player_name = input("\nEnter your name (default: Player): ").strip()
    if not player_name:
        player_name = "Player"
    
    # Get AI difficulty
    print("\nSelect AI difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    while True:
        difficulty_choice = input("\nEnter your choice (1/2/3): ").strip()
        if difficulty_choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")
    
    ai_difficulty = ["easy", "medium", "hard"][int(difficulty_choice) - 1]
    
    # Get number of rounds
    while True:
        try:
            num_rounds_input = input("\nEnter number of rounds (1-10, default: 3): ").strip()
            if not num_rounds_input:
                num_rounds = 3
                break
            num_rounds = int(num_rounds_input)
            if 1 <= num_rounds <= 10:
                break
            print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    return player_name, ai_difficulty, num_rounds

def display_game_rules():
    """Display the game rules with animation, but allow skipping with Enter."""
    clear_screen()
    print("===== DON'T SHUT THE BOX =====")
    
    # List of rules to display one by one
    rules = [
        "\nGame Rules: (press Enter anytime to skip)",
        "1. Roll the dice and shut numbers that sum to your roll",
        "2. If you successfully shut numbers, roll again",
        "3. Your turn ends when you cannot shut any more numbers",
        "4. Your score is the sum of numbers that remain open",
        "5. Lowest score wins!",
        "\nSpecial Rule: If numbers 7-9 are shut, you can choose to roll only one die"
    ]
    
    # Show first line without animation
    print(rules[0])
    
    # Use the animate_text function from animations.py with skip_enabled=True
    animate_text("\n".join(rules[1:]), delay=0.05, skip_enabled=True)
    
    input("\nPress Enter to continue... ")

def main():
    # Parse command-line arguments
    skip_intro = "--skip-intro" in sys.argv or "-s" in sys.argv
    simple_mode = "--simple" in sys.argv or "-sm" in sys.argv
    
    # Display game rules if not skipped
    if not skip_intro:
        display_game_rules()
    
    # Get game preferences
    player_name, ai_difficulty, num_rounds = display_welcome_screen()
    
    # Create players - simple mode only affects the UI, not the difficulty
    human_player = HumanPlayer(player_name, not simple_mode)
    if ai_difficulty == "easy":
        ai_player = AIPlayer("AI", "easy", not simple_mode)
    elif ai_difficulty == "medium":
        ai_player = AIPlayer("AI", "medium", not simple_mode)
    else:
        ai_player = AIPlayer("AI", "hard", not simple_mode)
    
    # Create and play the game with advanced mode by default unless simple flag is used
    game = Game([human_player, ai_player], not simple_mode)
    game.play_game(num_rounds)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Game terminated. Please try again.") 