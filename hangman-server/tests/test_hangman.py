import unittest

from hangman import GameState, GuessResult, HangmanGameScorer, HangmanGame


class TestHangmanGame(unittest.TestCase):
    def test_guess_failed_limit_raises_exception(self):
        self.assertRaises(ValueError, HangmanGame, 'a', 0)
        self.assertRaises(ValueError, HangmanGame, 'a', -1)

    def test_empty_word_raises_exception(self):
        self.assertRaises(ValueError, HangmanGame, '', 1)

    def test_win(self):
        game = HangmanGame('a', 1)

        self.assertEqual(game.state, GameState.IN_PROGRESS)
        self.assertEqual(game.guesses, [])
        self.assertEqual(game.failed_guess_limit, 1)
        self.assertEqual(game.num_failed_guesses_remaining, 1)
        self.assertEqual(game.revealed_word, '_')
        self.assertEqual(game.num_revealed_letters, 0)

        result = game.guess('a')

        self.assertEqual(result, GuessResult.CORRECT)
        self.assertEqual(game.state, GameState.WON)
        self.assertEqual(game.guesses, ['a'])
        self.assertEqual(game.failed_guess_limit, 1)
        self.assertEqual(game.num_failed_guesses_remaining, 1)
        self.assertEqual(game.revealed_word, 'a')
        self.assertEqual(game.num_revealed_letters, 1)

    def test_lose(self):
        game = HangmanGame('a', 1)

        self.assertEqual(game.state, GameState.IN_PROGRESS)
        self.assertEqual(game.guesses, [])
        self.assertEqual(game.failed_guess_limit, 1)
        self.assertEqual(game.num_failed_guesses_remaining, 1)
        self.assertEqual(game.revealed_word, '_')
        self.assertEqual(game.num_revealed_letters, 0)

        result = game.guess('b')

        self.assertEqual(result, GuessResult.INCORRECT)
        self.assertEqual(game.state, GameState.LOST)
        self.assertEqual(game.guesses, ['b'])
        self.assertEqual(game.failed_guess_limit, 1)
        self.assertEqual(game.num_failed_guesses_remaining, 0)
        self.assertEqual(game.revealed_word, '_')
        self.assertEqual(game.num_revealed_letters, 0)

    def test_invalid_input(self):
        game = HangmanGame('a', 1)
        result = game.guess('aaaaaaa')
        self.assertEqual(result, GuessResult.FAIL_INVALID_INPUT)
        self.assertEqual(game.state, GameState.IN_PROGRESS)
        self.assertEqual(game.guesses, [])
        self.assertEqual(game.failed_guess_limit, 1)
        self.assertEqual(game.num_failed_guesses_remaining, 1)
        self.assertEqual(game.revealed_word, '_')
        self.assertEqual(game.num_revealed_letters, 0)

        result = game.guess('.')
        self.assertEqual(result, GuessResult.FAIL_INVALID_INPUT)

        result = game.guess('!')
        self.assertEqual(result, GuessResult.FAIL_INVALID_INPUT)

    def test_valid_input(self):
        valid_chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
        game = HangmanGame(valid_chars, 1)

        for char in valid_chars:
            result = game.guess(char)
            self.assertEqual(result, GuessResult.CORRECT)
            self.assertIn(char, game.guesses)

        self.assertEqual(game.state, GameState.WON)

    def test_uppercase_input(self):
        game = HangmanGame('a', 1)

        result = game.guess('A')
        self.assertEqual(result, GuessResult.CORRECT)
        self.assertIn('a', game.guesses)
        self.assertEqual(game.state, GameState.WON)

    def test_cant_guess_when_game_over(self):
        game = HangmanGame('a', 1)
        game.guess('a')
        self.assertEqual(game.state, GameState.WON)

        result = game.guess('b')
        self.assertEqual(result, GuessResult.FAIL_ALREADY_GAME_OVER)
        self.assertEqual(game.guesses, ['a'])

        game = HangmanGame('a', 1)
        game.guess('b')
        self.assertEqual(game.state, GameState.LOST)

        result = game.guess('a')
        self.assertEqual(result, GuessResult.FAIL_ALREADY_GAME_OVER)
        self.assertEqual(game.guesses, ['b'])

    def test_cant_duplicate_guess(self):
        game = HangmanGame('ab', 2)
        game.guess('a')
        result = game.guess('a')
        self.assertEqual(result, GuessResult.FAIL_ALREADY_GUESSED)

        game = HangmanGame('ab', 2)
        game.guess('c')
        result = game.guess('c')
        self.assertEqual(result, GuessResult.FAIL_ALREADY_GUESSED)

    def test_revealed_word(self):
        game = HangmanGame('abac', 2)

        game.guess('b')
        self.assertEqual(game.revealed_word, '_b__')
        self.assertEqual(game.num_revealed_letters, 1)

        game.guess('a')
        self.assertEqual(game.revealed_word, 'aba_')
        self.assertEqual(game.num_revealed_letters, 3)

        game.guess('c')
        self.assertEqual(game.revealed_word, 'abac')
        self.assertEqual(game.num_revealed_letters, 4)

        self.assertEqual(game.state, GameState.WON)


class TestHangmanScorer(unittest.TestCase):
    def test_scorer(self):
        game = HangmanGame('abc', 2)
        score = HangmanGameScorer.score(game)
        self.assertEqual(score, 20)

        game.guess('a')
        score = HangmanGameScorer.score(game)
        self.assertEqual(score, 40)

        game.guess('d')
        score = HangmanGameScorer.score(game)
        self.assertEqual(score, 30)

        game.guess('b')
        score = HangmanGameScorer.score(game)
        self.assertEqual(score, 50)

        game.guess('c')
        score = HangmanGameScorer.score(game)
        self.assertEqual(score, 70)

