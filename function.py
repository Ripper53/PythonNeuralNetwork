import math

def meanSquaredLoss(input, target):
    return input - target

def sigmoid(x):
    if x < -709.0:
        return 0.0
    else:
        return 1.0 / (1.0 + math.exp(-x))

def sigmoidDerivative(x):
    return sigmoid(x) / (1.0 - sigmoid(x))

def relu(x):
    if x < 0.0:
        return 0.0
    else:
        return x

def reluDerivative(x):
    if x < 0.0:
        return 0.0
    else:
        return 1.0

def tanh(x):
    return math.tanh(x)

def tanhDerivative(x):
    return 1.0 - (tanh(x) * tanh(x))

def gaussian(x):
    return math.exp(-x ** 2)

def gaussianDerivative(x):
    return -2.0 * x * math.exp(-x ** 2)