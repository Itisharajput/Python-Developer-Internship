# ============================================================
#   NUMBER GUESSING GAME — Level 1, Task 2 (Basic)
#   Randomly generates number between 1-100
#   User guesses with feedback: Too High / Too Low
# ============================================================

import random

def play_game():
    print("=" * 40)
    print("      NUMBER GUESSING GAME")
    print("=" * 40)
    print("\nI have picked a number between 1 and 100.")
    print("You have 10 attempts to guess it!\n")

    secret_number = random.randint(1, 100)
    max_attempts  = 10
    attempts      = 0

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        print(f"Attempts remaining: {remaining}")

        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Invalid input! Please enter a number.\n")
            continue

        attempts += 1

        if guess < 1 or guess > 100:
            print("Please guess a number between 1 and 100!\n")
            attempts -= 1
            continue

        if guess == secret_number:
            print(f"\n🎉 Congratulations! You guessed it in {attempts} attempt(s)!")
            print(f"The number was: {secret_number}")
            break
        elif guess < secret_number:
            print("Too Low! Try a higher number.\n")
        else:
            print("Too High! Try a lower number.\n")

    else:
        print(f"\nGame Over! You've used all {max_attempts} attempts.")
        print(f"The correct number was: {secret_number}")

def main():
    while True:
        play_game()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ["yes", "y"]:
            print("\nThanks for playing! Goodbye!")
            break
        print("\n" + "=" * 40)

if name == "main":
    main()
