import time
import random
import os
import sys

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_text(text, delay=0.05, skip_enabled=False):
    """
    Print text with a typing animation effect.
    If skip_enabled is True, allows skipping the animation by pressing Enter.
    """
    # Simple case - if skip not enabled, just animate normally
    if not skip_enabled:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        return
    
    # Windows implementation with error handling
    if os.name == 'nt':
        try:
            import msvcrt
            if msvcrt.kbhit():  # Check if a key is in the buffer
                msvcrt.getch()  # Clear the input buffer
                print(text)  # Print all text at once
                return
        except ImportError:
            # If msvcrt not available, just print the text
            print(text)
            return
    
    # Unix implementation - first check if termios is available
    try:
        # Import the modules first to check availability
        import select
        import termios
        import tty
        
        # Only proceed with termios if we can successfully get terminal attributes
        try:
            # Check if we can get terminal attributes (will fail in some environments)
            old_settings = termios.tcgetattr(sys.stdin)
            has_termios = True
        except (termios.error, OSError):
            has_termios = False
            
        if has_termios:
            try:
                # Set terminal to raw mode to read single keystrokes
                tty.setcbreak(sys.stdin.fileno())
                
                for char in text:
                    # Check if a key was pressed
                    if select.select([sys.stdin], [], [], 0)[0]:
                        sys.stdin.read(1)  # Clear the input
                        # Skip animation and print all at once
                        print(text[text.index(char):])
                        break
                    
                    # Normal animation if no key press
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(delay)
                else:
                    # If loop completes without breaking, add final newline
                    print()
                    
            finally:
                # Restore terminal settings
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                return
        
        # If we get here, termios is available but we couldn't get terminal settings
        # Fall through to the fallback method
        
    except (ImportError, AttributeError):
        pass  # Fall through to fallback method
    
    # Fallback method when advanced terminal handling isn't available
    print(text)

def animate_dice_roll(num_dice=2, duration=1.0):
    """
    Animate dice rolling in terminal.
    Returns a tuple of (dice_sum, dice_values).
    """
    # ASCII dice faces
    dice_faces = [
        [
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘"
        ]
    ]
    
    # Number of animation frames
    frames = int(duration / 0.1)
    height = len(dice_faces[0])
    
    final_values = []
    for _ in range(num_dice):
        final_values.append(random.randint(1, 6))
    
    # Animate rolling
    for frame in range(frames):
        clear_screen()
        print("Rolling dice...")
        
        # For last frame, use the final values
        if frame == frames - 1:
            dice_values = final_values
        else:
            dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        
        # Print dice side by side
        for row in range(height):
            line = ""
            for dice_value in dice_values:
                line += dice_faces[dice_value - 1][row] + "  "
            print(line)
        
        time.sleep(0.1)
    
    # Print result
    result_sum = sum(final_values)
    print(f"\nYou rolled: {' + '.join(str(val) for val in final_values)} = {result_sum}")
    
    return result_sum, final_values

def animate_box_closing(numbers, board, delay=0.2):
    """Animate the closing of numbers on the board"""
    max_number = max(board + numbers)
    
    # Save current board state
    closed = [n for n in range(1, max_number + 1) if n not in board and n not in numbers]
    
    for num in numbers:
        clear_screen()
        print("\nClosing numbers:")
        
        # Display board with current number being closed
        board_display = " ".join(str(n) for n in range(1, max_number + 1))
        status_display = ""
        
        for n in range(1, max_number + 1):
            if n in closed:
                status_display += "# "
            elif n == num:
                status_display += "* "  # Highlight the number being closed
            else:
                status_display += "O "
        
        print(board_display)
        print(status_display)
        print(f"\nClosing: {num}")
        
        time.sleep(delay)
        closed.append(num)
    
    # Final state
    clear_screen()
    print("\nNumbers closed:")
    board_display = " ".join(str(n) for n in range(1, max_number + 1))
    status_display = " ".join("#" if n in closed else "O" for n in range(1, max_number + 1))
    
    print(board_display)
    print(status_display)
    print(f"\nClosed numbers: {sorted(numbers)}")
    time.sleep(delay)

def celebrate_win():
    """Simple celebration animation for winning"""
    celebration = [
        "*** YOU WIN! ***",
        "/// CHAMPION! \\\\\\",
        "=== VICTORY! ===",
        "<<< GAME MASTER! >>>",
        "*** PERFECT! ***"
    ]
    
    for _ in range(5):
        clear_screen()
        message = random.choice(celebration)
        print("\n\n")
        print(" " * 10 + message)
        print("\n\n")
        time.sleep(0.3)

def animate_game_title():
    """Animate the game title"""
    title = """
    ╔╦╗╔═╗╔╗╔╔╦╗  ╔═╗╦ ╦╦ ╦╔╦╗  ╔╦╗╦ ╦╔═╗  ╔╗ ╔═╗═╗ ╦
     ║║║ ║║║║ ║   ╚═╗╠═╣║ ║ ║    ║ ╠═╣║╣   ╠╩╗║ ║╔╩╦╝
    ═╩╝╚═╝╝╚╝ ╩   ╚═╝╩ ╩╚═╝ ╩    ╩ ╩ ╩╚═╝  ╚═╝╚═╝╩ ╚═
    """
    
    clear_screen()
    animate_text(title, 0.002)
    time.sleep(1)

def show_loading_bar(message="Loading", duration=1.0, width=30):
    """Show a loading bar animation"""
    clear_screen()
    print(f"{message}...")
    
    for i in range(width + 1):
        progress = i / width
        bar = "█" * i + "░" * (width - i)
        percent = int(progress * 100)
        
        sys.stdout.write(f"\r[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(duration / width)
    
    print("\nComplete!")
    time.sleep(0.3)

# Advanced sidebar animations
def get_terminal_size():
    """Get the terminal size"""
    try:
        columns, lines = os.get_terminal_size()
        return columns, lines
    except:
        return 80, 24  # fallback values

def clear_main_area(sidebar_width=30):
    """Clear only the main content area, leaving sidebar intact"""
    # Get terminal dimensions
    term_width, term_height = get_terminal_size()
    main_width = term_width - sidebar_width - 1  # -1 for separator
    
    # Save cursor position
    sys.stdout.write("\033[s")
    
    # Clear each line in the main area
    for i in range(3, term_height - 1):  # Start after header
        sys.stdout.write(f"\033[{i};0H")  # Move to beginning of line
        sys.stdout.write(" " * main_width)
    
    # Move cursor back to top of main area
    sys.stdout.write("\033[3;0H")
    
    # Restore cursor position
    sys.stdout.write("\033[u")

def move_to_main_area():
    """Position cursor at the start of the main content area"""
    sys.stdout.write("\033[3;0H")  # Row 3, column 0

def draw_sidebar(game_data, sidebar_width=30):
    """Draw the sidebar with game info on the right side of the screen"""
    term_width, term_height = get_terminal_size()
    
    # Calculate positions
    sidebar_start_col = term_width - sidebar_width
    main_area_width = sidebar_start_col - 1  # -1 for separator
    
    # Draw vertical separator line
    for i in range(1, term_height):
        sys.stdout.write(f"\033[{i};{sidebar_start_col - 1}H│")
    
    # Draw horizontal lines at top and bottom
    sys.stdout.write(f"\033[0;0H" + "=" * term_width)
    sys.stdout.write(f"\033[1;0H" + "DON'T SHUT THE BOX".center(term_width))
    sys.stdout.write(f"\033[2;0H" + "=" * term_width)
    
    # Draw the sidebar content
    current_row = 3  # Start after header
    
    # Get player data - handles both old dict format and new list format
    player_names = game_data.get("players", [])
    player_boards = game_data.get("boards", [])
    player_scores = game_data.get("scores", [])
    
    # Display each player's information
    for i, player_name in enumerate(player_names):
        # Get the player's board and score
        board = player_boards[i] if i < len(player_boards) else []
        score = player_scores[i] if i < len(player_scores) else 0
        
        # Player name and score
        player_info = f"{player_name}'s Box (Score: {score})"
        sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H{player_info}")
        current_row += 1
        
        # Board representation
        max_number = game_data.get("max_number", 9)
        closed = [n for n in range(1, max_number + 1) if n not in board]
        board_display = " ".join(str(n) for n in range(1, max_number + 1))
        status_display = " ".join("#" if n in closed else "O" for n in range(1, max_number + 1))
        
        sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H{board_display}")
        current_row += 1
        sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H{status_display}")
        current_row += 1
        
        open_nums = f"Open: {board}"
        if len(open_nums) > sidebar_width:
            open_nums = open_nums[:sidebar_width-3] + "..."
        sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H{open_nums}")
        current_row += 1
        
        # Separator between players
        sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H" + "-" * sidebar_width)
        current_row += 1
    
    # Game status
    round_info = f"Round {game_data.get('round', 1)} of {game_data.get('total_rounds', 1)}"
    sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H{round_info}")
    current_row += 1
    
    if "active_player" in game_data:
        turn_info = f"Current Turn: {game_data['active_player']}"
        sys.stdout.write(f"\033[{current_row};{sidebar_start_col}H{turn_info}")
        current_row += 1
    
    # Position cursor in main area for content
    move_to_main_area()

def sidebar_animate_dice_roll(num_dice=2, duration=1.0, sidebar_data=None, sidebar_width=30):
    """
    Animate dice rolling in terminal with sidebar.
    Returns a tuple of (dice_sum, dice_values).
    """
    if sidebar_data:
        draw_sidebar(sidebar_data, sidebar_width)
    
    # Clear the main area but keep sidebar
    clear_main_area(sidebar_width)
    move_to_main_area()
    
    # ASCII dice faces
    dice_faces = [
        [
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        [
            "┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘"
        ]
    ]
    
    # Number of animation frames
    frames = int(duration / 0.1)
    height = len(dice_faces[0])
    
    final_values = []
    for _ in range(num_dice):
        final_values.append(random.randint(1, 6))
    
    # Animate rolling
    for frame in range(frames):
        clear_main_area(sidebar_width)
        move_to_main_area()
        print("Rolling dice...")
        
        # For last frame, use the final values
        if frame == frames - 1:
            dice_values = final_values
        else:
            dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        
        # Print dice side by side
        for row in range(height):
            line = ""
            for dice_value in dice_values:
                line += dice_faces[dice_value - 1][row] + "  "
            print(line)
        
        time.sleep(0.1)
    
    # Print result
    result_sum = sum(final_values)
    print(f"\nYou rolled: {' + '.join(str(val) for val in final_values)} = {result_sum}")
    
    return result_sum, final_values

def sidebar_animate_box_closing(numbers, board, player_idx=0, sidebar_data=None, delay=0.2, sidebar_width=30):
    """Animate the closing of numbers on the board with sidebar"""
    if sidebar_data:
        draw_sidebar(sidebar_data, sidebar_width)
    
    clear_main_area(sidebar_width)
    move_to_main_area()
    
    max_number = max(board + numbers) if board else 9
    
    # Save current board state
    closed = [n for n in range(1, max_number + 1) if n not in board and n not in numbers]
    
    for num in numbers:
        clear_main_area(sidebar_width)
        move_to_main_area()
        print("\nClosing numbers:")
        
        # Display board with current number being closed
        board_display = " ".join(str(n) for n in range(1, max_number + 1))
        status_display = ""
        
        for n in range(1, max_number + 1):
            if n in closed:
                status_display += "# "
            elif n == num:
                status_display += "* "  # Highlight the number being closed
            else:
                status_display += "O "
        
        print(board_display)
        print(status_display)
        print(f"\nClosing: {num}")
        
        time.sleep(delay)
        closed.append(num)
        
        # Update sidebar data if provided
        if sidebar_data and "boards" in sidebar_data and player_idx < len(sidebar_data["boards"]):
            new_board = [n for n in sidebar_data["boards"][player_idx] if n != num]
            sidebar_data["boards"][player_idx] = new_board
            draw_sidebar(sidebar_data, sidebar_width)
    
    # Final state
    clear_main_area(sidebar_width)
    move_to_main_area()
    print("\nNumbers closed:")
    board_display = " ".join(str(n) for n in range(1, max_number + 1))
    status_display = " ".join("#" if n in closed else "O" for n in range(1, max_number + 1))
    
    print(board_display)
    print(status_display)
    print(f"\nClosed numbers: {sorted(numbers)}")
    time.sleep(delay)

def sidebar_celebrate_win(winner_name="You", sidebar_data=None, sidebar_width=30):
    """Simple celebration animation for winning with sidebar"""
    celebration = [
        f"*** {winner_name} WINS! ***",
        f"/// {winner_name} IS THE CHAMPION! \\\\\\",
        f"=== VICTORY FOR {winner_name}! ===",
        f"<<< GAME MASTER {winner_name}! >>>",
        f"*** PERFECT GAME, {winner_name}! ***"
    ]
    
    for _ in range(5):
        if sidebar_data:
            draw_sidebar(sidebar_data, sidebar_width)
        
        clear_main_area(sidebar_width)
        move_to_main_area()
        
        message = random.choice(celebration)
        print("\n\n")
        print(" " * 10 + message)
        print("\n\n")
        time.sleep(0.3)

if __name__ == "__main__":
    # Test animations
    animate_game_title()
    time.sleep(1)
    
    show_loading_bar("Setting up game", 2.0)
    
    roll, dice_values = animate_dice_roll(2, 1.5)
    print(f"You rolled: {roll}")
    
    animate_box_closing([3, 5, 7], list(range(1, 10)))
    
    celebrate_win() 