#the class that is managing the game
class Game:
    def __init__(self, id):
        # player 1 didn't move yet
        self.p1Went = False
        # player 2 didn't move yet
        self.p2Went = False
        self.ready = False
        # current game id
        self.id = id
        self.moves = [None, None]
        # wins= [player1, player2] how many wins each player has
        self.wins = [0, 0]
        # how many ties there are
        self.ties = 0

    # get the players move
    def get_player_move(self, p):
        return self.moves[p]

        # player 0= player1
        # player 1= player2
        # updates the moves lidt with the players move
    def play(self, player, move):
        self.moves[player] = move
        # if the player equals 0- player 1 made a move and therefore p1Went is updated to true
        if player == 0:
            self.p1Went = True
        else:
            # if the player equals 1- player 2 made a move and therefore p2Went is updated to true
            self.p2Went = True

    # checking if the two players are connected to the game
    def connected(self):
        return self.ready

    # checking if both of the players made a move
    def bothWent(self):
        return self.p1Went and self.p2Went

    # checking who won (player1 or player2)
    def winner(self):
        # checking 9 possible cases because there are 3 moves each player can do 3 times
        # checking the first word of the players move ('W'-Water, 'F'- Fire, 'S'-sponge)
        # checking the first players first letter of his move
        p1 = self.moves[0].upper()[0]
        # checking the second players first letter of his move
        p2 = self.moves[1].upper()[0]

        # if there is no winner- a tie
        winner = -1
        # in this case Water beats Fire and therefore p1 wins
        if p1 == "W" and p2 == "F":
            winner = 0
        # in this case Water beats Fire and therefore p2 wins
        elif p1 == "F" and p2 == "W":
            winner = 1
        # in this case Sponge beats Water and therefore p1 wins
        elif p1 == "S" and p2 == "W":
            winner = 0
        # in this case Sponge beats Water and therefore p2 wins
        elif p1 == "W" and p2 == "S":
            winner = 1
        # in this case Fire beats Sponge and therefore p1 wins
        elif p1 == "F" and p2 == "S":
            winner = 0
        # in this case Fire beats Sponge and therefore p2 wins
        elif p1 == "S" and p2 == "F":
            winner = 1

        return winner

    # updating the players moves to False
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False