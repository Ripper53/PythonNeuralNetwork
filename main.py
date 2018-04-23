from neuralnetwork import NeuralNetwork
from tictactoeAI import TicTacToeAI
#import function as f
import pickle

#AI = TicTacToeAI([9, 9, 9, 9, 9, 9])

# Loading
fileName = "tttAI.pickle"
pickle_in = open(fileName, "rb")
AI = pickle.load(pickle_in)
pickle_in.close()

print("Training...")
AI.trainFor(0.00001, 0.9, 0.01, 1000)
print("Training Completed!")

# Saving
pickle_out = open(fileName, "wb")
pickle.dump(AI, pickle_out)
pickle_out.close()

while True:
    AI.startGame(True, 0.00001, 0.9)
    print("Enter exit to close program, enter anything else to start another game...")
    if input() == "exit":
        break
    print("Next Game!")

# Saving
pickle_out = open(fileName, "wb")
pickle.dump(AI, pickle_out)
pickle_out.close()

#AI.print()