# Hangman - Revisited
It is the year 2034. 
The COVID pandemic rages on. 
People around the world have exhausted their supply of entertainment and are now turning to other sources to cure their boredom. 
One game stands out above all others in providing people with endless joy: Hangman.

Here at Hangman Hubs, we empower strangers, friends, coworkers, families, and people that have oddly close relationships with their pets to connect to each other at a deeper level. 
We do that through the classic game of hangman.

If you don’t know what hangman is, no worries! 
It’s a simple word game where the player has a limited number of chances to guess a random word. 

Here are the rules:
* A random word is chosen at the beginning of the game.
* The word is hidden from the player.
* The player has to guess, one letter at a time, what the word is.
* Each successful guess will reveal the letter in the hidden word.
* If they guess incorrectly 5 times, then it’s game over.
* If they guess the word correctly and the whole word is revealed, they win!

However, after literally millions of user interviews with hangman enthusiasts and analysis of petabytes worth of user data, the hangman product team has decided that the source of most user frustration is the inability to rewind time. 

Quote from an actual user:
> “My biggest regret in life is when I accidentally guessed an ‘R’ back in the World Hangman Olympics of `97. If I could do it all over, I would. I would trade anything for it.”

So the team has decided that adding the ability for users to undo their last guess will be the killer feature that brings the company millions of bitcoins in revenue.

## The Requirements
* “Undo” will remove the last guess and reset the player to the state there were in before they made their last guess.
* There should be a button in the UI that will allow the user to undo.
* The player is only allowed to undo once per game (time travel is expensive).
* Using the undo reduces their score by 50%.

## What are we looking for?

**Please take no longer than 5 hours to work on this exercise.**

When reviewing your solution we will check: 
* The feature works as described.
* All requirements are fulfilled.
* The code is of good quality.
* Automated tests are always a plus.

During your in person interview, we’ll do a live code review where we’ll go over your change and have you talk through some decisions you made while implementing the feature. 
We want to see how well you can understand an existing codebase and make a meaningful change to it.

## How should you submit your solution?
1. Fork this repository to your Github account and keep it private.
2. Once you're done share your repository with us.

## What does this repository include?
A simple hangman ui and server using js, react, python and flask!

It's split into two projects:
- [hangman-server](hangman-server)
- [hangman-web-app](hangman-web-app)

## Getting started

Get the server up and running
```
cd hangman-server
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

Get the web-app running
```
cd hangman-web-app
npm install
npm run start
```

Play some hangman!
```
http://localhost:3000
```

Bonus: Try out the command line app
```
cd hangman-server
python app.py
```

Good luck and have fun!
