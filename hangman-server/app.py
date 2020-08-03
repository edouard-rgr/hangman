from hangman import GameState, GuessResult, create_hangman_game, HangmanGameScorer

# This is missing highscore support

game = create_hangman_game()

while game.state == GameState.IN_PROGRESS:
    display_word = "".join([f"{l} " for l in game.revealed_word])

    print(display_word)
    print(f'Guesses remaining: {game.num_failed_guesses_remaining}')

    guess = input(f"Choose a letter : ")

    result = game.guess(guess)

    if result == GuessResult.FAIL_INVALID_INPUT:
        print("Invalid input")
    elif result == GuessResult.FAIL_ALREADY_GAME_OVER:
        print("Game is already over")
    elif result == GuessResult.FAIL_ALREADY_GUESSED:
        print("Letter was already guessed")


if game.state == GameState.WON:
    print("You won!")
elif game.state == GameState.LOST:
    print("You lost!")

score = HangmanGameScorer.score(game)
print(f"Score: {score}")
