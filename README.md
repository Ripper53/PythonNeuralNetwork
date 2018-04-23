# PythonNeuralNetwork
Created a neural network from scratch to learn the basics of it.

The neuralnetwork.py file contains the neural network.
I split the neural network into many parts using classes since I didn't want to deal with matrix multiplications.
The speed of training was not taken into account for in the algorithm. I made it to just work,
so I don't know if using arrays or numpy matrix would have made the training much faster.

When creating a NeuralNetwork object, the first parameter is a list of ints where each int is the number of nodes in that layer.
The number of layers is the length of that list, the first int is the number of inputs and last int is the number of outputs.
There must be at least three ints in the list and all ints must have a value greater than 0.

The function.py file contains important functions for the neural network to use.
Such as activation functions and functions to calculate loss.
Add more activation or loss functions here and pass them in the parameters of the class NeuralNetwork to use them.

The min and max in the parameters of the NeuralNetwork class are the random range the values can take.

The training algorithm uses backpropogation to learn, the neural network is fully connected.
