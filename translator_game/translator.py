"""EN - DE / DE - EN translation game based on a key:value dict file.

For adding more entries update the 'translator_game/dictionary.txt' file 
using the pattern 'en_word:de_word'.
"""


import os
import codecs
import random
import ConfigParser
import datetime
import sys
import ast


HS_FILE = 'high_scores.cfg'
DICT_FILE = 'dictionary.txt'
EN_DE = 'EN_DE'
DE_EN = 'DE_EN'


class TranslatorGame():
  
  def __init__(self):
    self.path_to_dir = os.path.abspath(os.path.dirname(__file__))
    self.score_file = os.path.join(self.path_to_dir, HS_FILE)
    self.dict_file = os.path.join(self.path_to_dir, DICT_FILE)
    self.score_parser = ConfigParser.RawConfigParser()
    self.game_type = None
    self.rounds = None
    self.duration = None
    self.score = 0
    self.words = {}
    self.best_score = 'N/A'
    self.best_time = 'N/A'

  def PrintGameHelp(self):
    """Prints game instructions."""

    print ('\n##################################\n'
           '1.  Select game type EN-DE or DE-EN\n'
           '2.  Choose number of rounds between 1 and 30\n'
           '3.  Type the translation\n'
           '4.  Score 3 if you get it right first try, 1 for second try\n'
           '*   English verbs start with \'to \'\n'
           '**  Each key has one value only\n'
           '*** Type \'exit()\' at any time to abort\n' 
           '##################################\n')

  def SetGameType(self):
    """Sets translation game type (English to German or viceversa)."""

    user_input = None
    while user_input not in ['en', 'de']:
      if user_input:
        print "Accepted values are 'en' or 'de' "
      user_input = raw_input("Play EN-DE ('en') or DE-EN ('de')? \n")
      game_type = EN_DE if user_input == 'en' else DE_EN
    return game_type

  def DictionaryBuilder(self):
    """Builds dictionary based on 'DICT_FILE' file ."""

    words = {}
    with codecs.open(self.dict_file, 'r', 'utf-8') as my_file:
      for line in my_file:
        if line.strip():
          if self.game_type == EN_DE:
            key, value = line.strip().split(':')
          else:
            value, key = line.strip().split(':')
          words[key] = value
    return words

  def SetRounds(self):
    """Sets number of rounds for the game."""

    rounds =  None
    while rounds not in range(1,31):
      rounds = raw_input("Number of rounds: \n")
      try:
        rounds = int(rounds)
        if rounds > 30 or rounds < 1:
          print 'min. rounds is one, max. is 30'
      except:
        print "'%s' is not an integer" % (rounds)
    return rounds

  def SetGameVars(self):
    """Sets instance variables."""

    self.game_type = self.SetGameType()
    self.words = self.DictionaryBuilder()
    self.rounds = self.SetRounds()

  def RunGame(self):
    """Runs translation game."""

    print 'Starting...\n'
    tick = datetime.datetime.now()
    for i in range(self.rounds):
      key = random.choice(self.words.keys())
      value = self.words[key]
      print key
      answer = raw_input()
      if answer == 'exit()':
        sys.exit('Bye')
      if answer.decode('utf-8') == value:
        self.score += 3
        print '\nOK\n'
      else:
        hint = '%s...' %(value [0:4] if value.startswith('to ')
                         else value [0:2])
        print hint
        answer_2 = raw_input()
        if answer_2.decode('utf-8') == value:
          self.score += 1
          print '\nOK\n'
        else:
          print '\nIt was: %s\n' %(value)
    tock = datetime.datetime.now()
    t_delta = tock-tick
    self.duration = datetime.timedelta(seconds=round(
        t_delta.total_seconds(), 2))

  def _ValidateHighScoreFile(self):
    """Creates high-score.
    
    Creates high-score file if it is not found on drive at path 
    'self.score_file' and adds EN_DE and DE_EN sections.
    """

    if not os.path.isfile(self.score_file):
      with open(self.score_file, 'w+') as score_file:
        score_file.write('[%s]\n[%s]\n'% (EN_DE, DE_EN))

  def _ReadHighScoreFile(self):
    """Reads high-score file."""

    self._ValidateHighScoreFile()
    self.score_parser.read(self.score_file)

  def SetHighScore(self):
    """Sets high score.
    
    Evaluates high-score file statistics and compares with current score and
    time. If the new values are better sets self.best_time and self.best_score
    and overrites them in the score file.
    
    Returns:
      high_score: True if new high score set, else False
    """

    self._ReadHighScoreFile()
    high_score = False
    option = '%s_rounds' % self.rounds
    new_statistics = [self.score, self.duration.total_seconds()]
    if self.score_parser.has_option(self.game_type, option):
      current_statistics = ast.literal_eval(self.score_parser.get(
          self.game_type, option))
      self.best_score = int(current_statistics[0])
      self.best_time = datetime.timedelta(seconds=float(current_statistics[1]))

      if 0 < self.score > self.best_score:
        high_score = True
      elif self.score == self.best_score:
        if self.duration < self.best_time:
          high_score = True
    else:
      if self.score > 0:
        high_score = True
    if high_score:
      self.best_score = self.score
      self.best_time = self.duration
      self.score_parser.set(self.game_type, option, new_statistics)
    with open(self.score_file, 'wb') as high_score_file:
      self.score_parser.write(high_score_file)
    return high_score

  def PrintGameStatistics(self):
    """Prints game statistics."""

    set_score = self.SetHighScore()
    print 'Statistics:\n##################################'
    if set_score:
      print 'NEW HIGH SCORE!!! %s / %s' % (self.best_score,
                                           str(self.best_time)[:-4])
    print ('Game type: %s\nRounds:  %s\nScore: %s\nDuration: %s\n'
           'Max. possible score for %s rounds: %s\nCurrent High Score: %s / %s\n'
           '##################################' % (self.game_type, self.rounds,
            self.score, str(self.duration)[:-4], self.rounds, (3 * self.rounds),
            self.best_score, str(self.best_time)[:-4]))

  def Play(self):
    self.PrintGameHelp()
    self.SetGameVars()
    self.RunGame()
    self.PrintGameStatistics()

if __name__=="__main__":
  game_player = TranslatorGame()
  game_player.Play()
