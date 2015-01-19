<strong>Python translator game.</strong>

For adding more entries update the 'translator_game/dictionary.txt' file 
using the pattern 'en_word:de_word'.

The translator game also uses a high-score system. A file 'high_scores.cfg'
will be created after the first play in the game directory. From then on it will
store the best score and time for each type of game and number of rounds.
Deleting the 'high_scores.cfg' file resets the statistics.

USAGE:

  - run this module without arguments --> play translator game
  - run with '--print_dict' --> prints the contents of 'dictionary.txt'
    sorted by English words
  - run with '--sort_dict' --> sorts the 'dictionary.txt' in place
  - run with '-h' --> shows standard help message