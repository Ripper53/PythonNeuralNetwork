from tictactoe import TicTacToe
from neuralnetwork import NeuralNetwork
import random
import function as f

class TicTacToeAI(object):

    def __init__(self, hiddenLayers, hiddenActivationFunction = f.relu, hiddenActivationFunctionDerivative = f.reluDerivative, outputActivationFunction = f.gaussian, outputActivationFunctionDerivative = f.gaussianDerivative):
        layers = [9]
        for i in range(len(hiddenLayers)):
            layers.append(hiddenLayers[i])
        layers.append(9)
        self.NN = NeuralNetwork(layers, hiddenActivationFunction, hiddenActivationFunctionDerivative, outputActivationFunction, outputActivationFunctionDerivative)
        self.totalGamesTrained = 0

    def print(self):
        self.NN.print()

    def getTotalGamesTrained(self):
        return self.totalGamesTrained

    def startGame(self, trainingGame = False, learningRate = 0.1, decay = 0.99):
        cross = 1
        circle = -1
        playerMoves = []
        playerBoard = []
        neuralMoves = []
        neuralBoard = []
        mark = circle
        game = TicTacToe()
        entry = ""
        while entry != "exit" and game.finished() == False:
            if entry == "print":
                self.print()
            else:
                game.print()
                if mark == cross:
                    mark = circle
                    board = game.getBoard(mark)
                    coord = self.action(board)
                    x = coord[0][0]
                    y = coord[0][1]
                    #print(coord)
                    print("x: " + str(x) + ", y: " + str(y))
                    while game.addMark(mark, x, y) == False:
                        if trainingGame == False:
                            break
                        out = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
                        value = self.coordinatesToIndex(x, y)
                        out[value] = 0.0
                        self.NN.trainWithOutput(learningRate, out)
                        coord = self.action(board)
                        x = coord[0][0]
                        y = coord[0][1]
                    if trainingGame:
                        value = self.coordinatesToIndex(x, y)
                        neuralMoves.append(value)
                        neuralBoard.append(board)
                else:
                    mark = cross
                    entry = input()
                    if entry != "exit":
                        split = entry.split(',')
                        x = int(split[0])
                        y = int(split[1])
                        if game.addMark(mark, x, y) and trainingGame:
                            board = game.getBoard(mark)
                            value = self.coordinatesToIndex(x, y)
                            playerMoves.append(value)
                            playerBoard.append(board)
            print()
        if game.finished() == True:
            game.print()
            winner = game.getWinner()
            print("Winner: " + str(winner))
            if trainingGame:
                neuralMoves.reverse()
                neuralBoard.reverse()
                if winner == cross:
                    for i in range(len(neuralMoves)):
                        target = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
                        target[neuralMoves[i]] = 0.0
                        self.NN.train(learningRate * (decay ** i), neuralBoard[i], target)
                    for i in range(len(playerMoves)):
                        target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                        target[playerMoves[i]] = 1.0
                        self.NN.train(learningRate * (decay ** i), playerBoard[i], target)
                elif winner == circle:
                    for i in range(len(neuralMoves)):
                        target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                        target[neuralMoves[i]] = 1.0
                        self.NN.train(learningRate * (decay ** i), neuralBoard[i], target)
                    for i in range(len(playerMoves)):
                        target = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
                        target[playerMoves[i]] = 0.0
                        self.NN.train(learningRate * (decay ** i), playerBoard[i], target)
                #else:
                #    for i in range(len(neuralMoves)):
                #        target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                #        target[neuralMoves[i]] = 1.0
                #        self.NN.train(learningRate * (decay ** i), neuralBoard[i], target)
                #    for i in range(len(playerMoves)):
                #        target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                #        target[playerMoves[i]] = 1.0
                #        self.NN.train(learningRate * (decay ** i), playerBoard[i], target)
    
    def trainFor(self, learningRate, decay, exploreRate, episodes):
        cross = 1
        circle = -1
        gameNum = 0
        for _ in range(episodes):
            self.totalGamesTrained += 1
            gameNum += 1
            print("Number " + str(gameNum))
            game = TicTacToe()
            crossMoves = []
            crossBoard = []
            circleMoves = []
            circleBoard = []
            mark = circle
            while game.finished() == False:
                #game.print()
                if mark == cross:
                    mark = circle
                else:
                    mark = cross
                x = None
                y = None
                board = game.getBoard(mark)
                if random.random() >= exploreRate:
                    coord = self.action(board)
                    x = coord[0][0]
                    y = coord[0][1]
                    while game.addMark(mark, x, y) == False:
                        #game.print()
                        out = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
                        value = self.coordinatesToIndex(x, y)
                        out[value] = 0.0
                        self.NN.trainWithOutput(learningRate, out)
                        coord = self.action(board)
                        x = coord[0][0]
                        y = coord[0][1]
                else:
                    pos = [[0,0],[1,0],[2,0],[0,1],[1,1],[2,1],[0,2],[1,2],[2,2]]
                    picked = random.choice(pos)
                    x = picked[0]
                    y = picked[1]
                    #print("Explored!")
                    while game.addMark(mark, x, y) == False:
                        pos.remove(picked)
                        picked = random.choice(pos)
                        x = picked[0]
                        y = picked[1]
                value = self.coordinatesToIndex(x, y)
                if mark == cross:
                    crossMoves.append(value)
                    crossBoard.append(board)
                else:
                    circleMoves.append(value)
                    circleBoard.append(board)
            #game.print()
            crossMoves.reverse()
            crossBoard.reverse()
            circleMoves.reverse()
            circleBoard.reverse()
            if game.getWinner() == cross:
                for i in range(len(crossMoves)):
                    target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                    target[crossMoves[i]] = 1.0
                    self.NN.train(learningRate * (decay ** i), crossBoard[i], target)
                for i in range(len(circleMoves)):
                    target = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
                    target[circleMoves[i]] = 0.0
                    self.NN.train(learningRate * (decay ** i), circleBoard[i], target)
            elif game.getWinner == circle:
                for i in range(len(circleMoves)):
                    target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                    target[circleMoves[i]] = 1.0
                    self.NN.train(learningRate * (decay ** i), circleBoard[i], target)
                for i in range(len(crossMoves)):
                    target = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
                    target[crossMoves[i]] = 0.0
                    self.NN.train(learningRate * (decay ** i), crossBoard[i], target)
            #else:
            #    for i in range(len(crossMoves)):
            #        target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            #        target[crossMoves[i]] = 1.0
            #        self.NN.train(learningRate * (decay ** i), crossBoard[i], target)
            #    for i in range(len(circleMoves)):
            #        target = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            #        target[circleMoves[i]] = 1.0
            #        self.NN.train(learningRate * (decay ** i), circleBoard[i], target)

    def action(self, input):
        output = self.NN.feedForward(input)
        highestIndex = 0
        highestValue = output[0]
        for i in range(1, len(output)):
            if highestValue < output[i]:
                highestIndex = i
                highestValue = output[i]
        return self.indexToCoordinates(highestIndex), output, highestIndex

    def indexToCoordinates(self, index):
        if index == 0:
            return 0, 0
        elif index == 1:
            return 1, 0
        elif index == 2:
            return 2, 0
        elif index == 3:
            return 0, 1
        elif index == 4:
            return 1, 1
        elif index == 5:
            return 2, 1
        elif index == 6:
            return 0, 2
        elif index == 7:
            return 1, 2
        else:
            return 2, 2

    def coordinatesToIndex(self, x, y):
        if x == 0 and y == 0:
            return 0
        elif x == 1 and y == 0:
            return 1
        elif x == 2 and y == 0:
            return 2
        elif x == 0 and y == 1:
            return 3
        elif x == 1 and y == 1:
            return 4
        elif x == 2 and y == 1:
            return 5
        elif x == 0 and y == 2:
            return 6
        elif x == 1 and y == 2:
            return 7
        else:
            return 8