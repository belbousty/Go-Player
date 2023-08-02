# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
import math
from playerInterface import *

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):
        return "Ayume"

    def is_out_of_edges(self, coord):
        length = self._board._BOARDSIZE
        if (coord % length != length-1 and 
                coord % length != 0 and 
                coord >= length and 
                coord < length**2 -length):
            return True
        return False
    
    def _get_neighbors(self, coord):
        size = self._board._BOARDSIZE
        if (self.is_out_of_edges(coord)):
            return [coord - 1, coord + 1, coord - size, coord +size]
        elif (coord < size):
            if (coord == 0):
                return [coord+1, coord + size]
            if (coord == size - 1):
                return  [coord -1, coord + size]
            else :
                return [coord+1, coord -1, coord + size]
        elif (coord > (size-1)**2): 
            if (coord == size**2 -1):
                return [coord - 1, coord -size]
            if (coord == (size-1)**2 + 1) :
                return [coord + 1, coord -size]
            else: 
                return [coord + 1, coord - 1, coord - size]
        elif (coord % size ==0): 
            return [coord+1, coord - size, coord + size]
        else: 
            return [coord - 1, coord + size, coord -size]

    def get_coordinates(self, coord):
        size = self._board._BOARDSIZE
        return [coord//size, coord%size]
    
    def reverse_cordinates(self, i, j): 
        size = self._board._BOARDSIZE
        return  size*i+j

    def get_liberties(self, i, j):
            count = 0
            coord = self.reverse_cordinates(i, j)
            neighbors = self._get_neighbors(coord)
            for i in range(0, len(neighbors)):
                if (self._board.__getitem__(neighbors[i]) == self._board._EMPTY):
                    count += 1
            return count

    def get_empty_advantages(self, i, j):
        opponent_color = self._board.flip(self._mycolor)
        count = 0
        coord = self.reverse_cordinates(i, j)
        neighbors = self._get_neighbors(coord)
        for i in range(0, len(neighbors)):
                if (self._board.__getitem__(neighbors[i]) == opponent_color):
                    count += 1
        return count
        
    def get_captured_stones(self, color):
        if (color == self._board._BLACK):
            return self._board._capturedWHITE
        else :
            return self._board._capturedBLACK


    def generate_weight(self, coord):
        opponent_color = self._board.flip(self._mycolor)
        center = self.get_coordinates(coord)
        size = self._board._BOARDSIZE
        half_size = (size - 1) // 2
        matrix = [[0] * size for _ in range(size)]

        for i in range(size):
            for j in range(size):
                distance = max(abs(center[0] - i), abs(center[1] - j))
                value = 3**(2*self.get_captured_stones(self._mycolor)+1) # My captured stones
                #value += 2 **(max(half_size - distance, 0))
                value += 3**(self.evaluate_connectivity(coord, self._mycolor) +1) # My connectivty 
                if (self._board.__getitem__(self.reverse_cordinates(i,j)) == self._mycolor):
                    value += 3**(self.get_liberties(i,j)*2) # liberties of stone
                if (self._board.__getitem__(self.reverse_cordinates(i,j)) == opponent_color):
                    value += 3**((4-self.get_liberties(i,j) + 1)*2) # liberties of oppnent stone
                value += 2**(self.get_empty_advantages(i, j) + 1)
    
                matrix[i][j] = value
        weights = [element for sublist in matrix for element in sublist]
        return weights
    
    def evaluate_connectivity(self, coord, color ,storage=[]):
        if self._board.__getitem__(coord) == color: 
            size = self._board._BOARDSIZE
            neighbors = self._get_neighbors(coord)
            for i in range(0,len(neighbors)):
                if (self._board.__getitem__(neighbors[i]) == color and (neighbors[i] not in storage)):
                    storage.append(neighbors[i])
                    return 1 + self.evaluate_connectivity(neighbors[i],color,storage)
        return 0

        
    def evaluate_board(self):
        stones_number = 0
        score = 0
        size = self._board._BOARDSIZE
        weights = self.generate_weight(size//2*(size+1))
        for coord in range(0, self._board.__len__()):
            if (self._board.__getitem__(coord) == self._mycolor):
                stones_number += 1
        if stones_number > 2: 
            opponent_color = self._board.flip(self._mycolor)
            connectivity = 0 
            for coord in range(1, self._board.__len__()):
                if (self._board.__getitem__(coord) == self._mycolor):
                    my_connect = self.evaluate_connectivity(coord, self._mycolor) 
                    if (my_connect > connectivity):
                        connectivity = my_connect
                        weights = self.generate_weight(coord)
            for coord in range(0, self._board.__len__()):
                if (self._board.__getitem__(coord) == self._mycolor):
                    score += weights[coord]
            return score
        else :
            if (stones_number == 1):
                weights = self.generate_weight(20)
            elif (stones_number == 2):
                weights = self.generate_weight(24)
            else : 
                weights = self.generate_weight(33)
            for coord in range(0, self._board.__len__()):
                if (self._board.__getitem__(coord) == self._mycolor):
                    score += weights[coord]
            return score



    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self._board.is_game_over():
            return self.evaluate_board(), None
        
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self._board.legal_moves():
                self._board.push(move)
                eval, _ = self.alpha_beta(depth-1, alpha, beta, False)
                self._board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self._board.legal_moves():
                self._board.push(move)
                eval, _ = self.alpha_beta(depth-1, alpha, beta, True)
                self._board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

        
    def stonesNb(self):
        stones_number = 0
        for coord in range(0, self._board.__len__()):
            if (self._board.__getitem__(coord) == self._mycolor):
                stones_number += 1
        return stones_number
    

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS"
        
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = True
        if (self.stonesNb() >= 25) :
            best_eval, move = self.alpha_beta(4, alpha, beta, maximizing_player)
        elif (self.stonesNb() >= 10) :
            best_eval, move = self.alpha_beta(3, alpha, beta, maximizing_player)
        else :
            best_eval, move = self.alpha_beta(2, alpha, beta, maximizing_player)
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



