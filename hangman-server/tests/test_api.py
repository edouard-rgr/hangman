from server import app
from unittest import TestCase
import json
import sys
import hangman


# Monkey patch the create game function so we can have a deterministic word to test with. This should
# probably read the words from some config and not rely on hardcoded vars but this is simpler.
original_hangman_create = hangman.create_hangman_game
def create_game_with_override_words(words=None, guess_limit=5):
    return original_hangman_create(words=['abac'], guess_limit=5)

hangman.create_hangman_game = create_game_with_override_words


def parse_response(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


class TestApiIntegration(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def post_guess(self, game_id, letter):
        return self.app.post(
            f'/api/hangman/{game_id}/guess',
            data=json.dumps({} if letter is None else {'letter': letter}),
            content_type='application/json'
        )

    def get_game(self, game_id):
        return self.app.get(f'/api/hangman/{game_id}')

    def test_full_game(self):
        response = parse_response(self.app.post('/api/hangman'))

        self.assertIn('gameId', response)
        self.assertEqual(response['state'], 'IN_PROGESS')
        self.assertEqual(response['revealedWord'], '____')
        self.assertEqual(response['numFailedGuessesRemaining'], 5)
        self.assertEqual(response['score'], 5 * 10)

        game_id = response['gameId']

        response = parse_response(self.post_guess(game_id, 'a'))
        self.assertEqual(response['result'], 'CORRECT')

        response = parse_response(self.get_game(game_id))
        self.assertEqual(response['state'], 'IN_PROGESS')
        self.assertEqual(response['revealedWord'], 'a_a_')
        self.assertEqual(response['numFailedGuessesRemaining'], 5)
        self.assertEqual(response['score'], 2 * 20 + 5 * 10)

        response = parse_response(self.post_guess(game_id, 'd'))
        self.assertEqual(response['result'], 'INCORRECT')

        response = parse_response(self.get_game(game_id))
        self.assertEqual(response['state'], 'IN_PROGESS')
        self.assertEqual(response['revealedWord'], 'a_a_')
        self.assertEqual(response['numFailedGuessesRemaining'], 4)
        self.assertEqual(response['score'], 2 * 20 + 4 * 10)

        response = parse_response(self.post_guess(game_id, 'b'))
        self.assertEqual(response['result'], 'CORRECT')

        response = parse_response(self.get_game(game_id))
        self.assertEqual(response['state'], 'IN_PROGESS')
        self.assertEqual(response['revealedWord'], 'aba_')
        self.assertEqual(response['numFailedGuessesRemaining'], 4)
        self.assertEqual(response['score'], 3 * 20 + 4 * 10)

        response = self.post_guess(game_id, 'a')
        self.assertEqual(response.status_code, 500)
        parsed_response = parse_response(response)
        self.assertEqual(parsed_response['error'], 'Letter already guessed')

        response = parse_response(self.post_guess(game_id, 'c'))
        self.assertEqual(response['result'], 'CORRECT')

        response = parse_response(self.get_game(game_id))
        self.assertEqual(response['state'], 'WON')
        self.assertEqual(response['revealedWord'], 'abac')
        self.assertEqual(response['numFailedGuessesRemaining'], 4)
        self.assertEqual(response['score'], 4 * 20 + 4 * 10)

        response = self.post_guess(game_id, 'a')
        self.assertEqual(response.status_code, 500)
        parsed_response = parse_response(response)
        self.assertEqual(parsed_response['error'], 'Game already over')

    def test_get_hangman_missing(self):
        invalid_game_id = 9999
        response = self.get_game(invalid_game_id)
        self.assertEqual(response.status_code, 404)

    def test_post_hangman_guess_missing(self):
        invalid_game_id = 9999
        response = self.post_guess(invalid_game_id, 'a')
        self.assertEqual(response.status_code, 404)

    def test_post_hangman_guess_invalid(self):
        response = parse_response(self.app.post('/api/hangman'))
        game_id = response['gameId']

        response = self.post_guess(game_id, 'aaaaaa')
        self.assertEqual(response.status_code, 400)
        parsed_response = parse_response(response)
        self.assertEqual(parsed_response['error'], 'Invalid input')

        response = self.post_guess(game_id, None)
        self.assertEqual(response.status_code, 400)
        parsed_response = parse_response(response)
        self.assertEqual(parsed_response['error'], '\'letter\' is required input')


