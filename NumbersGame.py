import random
import sys


def play_guess_the_number():
	print("Welcome to Guess the Number!")
	difficulties = {
		"1": (10, 6),    # range 1-10, 6 attempts
		"2": (50, 8),    # range 1-50, 8 attempts
		"3": (100, 10),  # range 1-100, 10 attempts
	}

	while True:
		print("Choose difficulty: 1) Easy 2) Medium 3) Hard")
		choice = input("Enter 1, 2 or 3 (or q to return): ").strip()
		if choice.lower() == 'q':
			return
		if choice not in difficulties:
			print("Invalid choice. Try again.")
			continue

		high, max_attempts = difficulties[choice]
		number = random.randint(1, high)
		attempts = 0
		print(f"I'm thinking of a number between 1 and {high}.")

		while attempts < max_attempts:
			attempts += 1
			try:
				guess = input(f"Attempt {attempts}/{max_attempts}. Your guess: ")
			except (KeyboardInterrupt, EOFError):
				print("\nGoodbye!")
				sys.exit(0)

			if not guess.isdigit():
				print("Please enter a whole number.")
				attempts -= 1
				continue

			guess = int(guess)
			if guess == number:
				print(f"Correct! You found it in {attempts} attempts.")
				break
			elif guess < number:
				print("Too low.")
			else:
				print("Too high.")

		else:
			print(f"Out of attempts! The number was {number}.")

		again = input("Play again? (y/n): ").strip().lower()
		if again != 'y':
			return


def main_menu():
	print("Simple Python Games — quick test harness")
	while True:
		print("\nMenu:\n1) Guess the Number\nq) Quit")
		choice = input("Choose an option: ").strip().lower()
		if choice == '1':
			play_guess_the_number()
		elif choice == 'q':
			print("Thanks for playing — goodbye!")
			break
		else:
			print("Unknown option. Please choose 1 or q.")


if __name__ == '__main__':
	try:
		main_menu()
	except (KeyboardInterrupt, EOFError):
		print("\nExiting. Bye!")





