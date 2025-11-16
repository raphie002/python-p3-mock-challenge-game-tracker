# lib/classes/many_to_many.py
class Game:
    def __init__(self, title):
        self._title = None
        self.title = title

    def results(self):
        # Returns a list of all Result objects for this game.
        return [result for result in Result.all if result.game is self]

    def players(self):
        # Returns a list of all unique Player objects who have played this game.
        players_list = [result.player for result in self.results()]
        # Use a dictionary to maintain insertion order and ensure uniqueness
        unique_players = list(dict.fromkeys(players_list))
        return unique_players

    def average_score(self, player):
        # Calculates the average score for a specific player in this game.
        player_results = [
            result.score
            for result in self.results()
            if result.player is player
        ]
        if not player_results:
            return 0  # Should not happen based on test, but good practice
        return sum(player_results) / len(player_results)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title_value):
        # Validation checks for title (immutable string, length > 0)
        # Note: The test for immutability is handled by only allowing setting in __init__
        # and checking the type/length constraints. If exceptions were used, it would be different.
        if isinstance(title_value, str) and len(title_value) > 0 and self._title is None:
            self._title = title_value
        elif self._title is not None:
            # For the immutability test: only allow initial set
            return
        elif not isinstance(title_value, str) or len(title_value) == 0:
            # Prevent initial invalid title set if not already set (or if using exceptions)
            # Based on the test, we only allow initial valid assignment.
            pass


class Player:
    def __init__(self, username):
        self._username = None
        self.username = username

    def results(self):
        # Returns a list of all Result objects for this player.
        return [result for result in Result.all if result.player is self]

    def games_played(self):
        # Returns a list of all unique Game objects played by this player.
        games_list = [result.game for result in self.results()]
        # Use a dictionary to maintain insertion order and ensure uniqueness
        unique_games = list(dict.fromkeys(games_list))
        return unique_games

    def played_game(self, game):
        # Returns True if the player has played the game, False otherwise.
        return game in self.games_played()

    def num_times_played(self, game):
        # Returns the number of times the player has played the game.
        return len([result for result in self.results() if result.game is game])
    
    # Static method from commented-out test (TestPlayer.test_highest_score)
    @classmethod
    def highest_scored(cls, game):
        # Finds the player with the highest average score for a given game.
        # Collect all players for the game
        players_in_game = game.players()
        if not players_in_game:
            return None
        
        # Calculate average score for each player
        player_averages = {
            player: game.average_score(player)
            for player in players_in_game
        }

        # Find the player with the maximum average score
        return max(player_averages, key=player_averages.get)


    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username_value):
        # Validation checks for username (string, length 2 to 16)
        if (
            isinstance(username_value, str)
            and 2 <= len(username_value) <= 16
        ):
            self._username = username_value


class Result:
    all = [] # Class attribute to hold all Result instances

    def __init__(self, player, game, score):
        self._player = None
        self._game = None
        self._score = None
        
        self.player = player
        self.game = game
        self.score = score
        
        # Add the new instance to the class's all list
        Result.all.append(self)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score_value):
        # Validation checks for score (immutable integer, 1 <= score <= 5000)
        if (
            isinstance(score_value, int)
            and 1 <= score_value <= 5000
            and self._score is None # Enforce immutability
        ):
            self._score = score_value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player_value):
        # Validation check for player (type Player, immutable)
        if isinstance(player_value, Player) and self._player is None:
            self._player = player_value

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, game_value):
        # Validation check for game (type Game, immutable)
        if isinstance(game_value, Game) and self._game is None:
            self._game = game_value