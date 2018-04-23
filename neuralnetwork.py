import random
import function as f

class Node(object):

    def __init__(self):
        self.value = 0.0

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

class Weight(object):

    def __init__(self, backNode, frontNode, minValue = -0.5, maxValue = 0.5):
        self.value = random.uniform(minValue, maxValue)
        self.delta = self.value
        self.backNode = backNode
        self.frontNode = frontNode

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def subtractValue(self, valueToSubtract):
        self.value -= valueToSubtract

    def getDelta(self):
        return self.delta

    def setDeltaToValue(self):
        self.delta = self.value

    def getBackNode(self):
        return self.backNode

    def getFrontNode(self):
        return self.frontNode

class FrontWeights(object):

    def __init__(self):
        self.frontWeights = []

    def getFrontWeights(self):
        return self.frontWeights

    def getFrontWeight(self, index):
        return self.frontWeights[index]

    def addFrontWeight(self, weight):
        self.frontWeights.append(weight)

class InputNode(Node, FrontWeights):

    def __init__(self):
        self.value = 0.0
        self.frontWeights = []

class BackWeights(object):

    def __init__(self):
        self.backWeights = []

    def getBackWeights(self):
        return self.backWeights

    def getBackWeight(self, index):
        return self.backWeights[index]

    def addBackWeight(self, weight):
        self.backWeights.append(weight)

class Neuron(Node, BackWeights):

    def __init__(self, activationFunction, activationFunctionDerivative, minBias = -0.5, maxBias = 0.5):
        self.activationFunction = activationFunction
        self.activationFunctionDerivative = activationFunctionDerivative
        self.value = 0.0
        self.trueValue = 0.0
        self.delta = 0.0
        self.bias = random.uniform(minBias, maxBias)
        self.backWeights = []

    def getTrueValue(self):
        return self.trueValue

    def getDelta(self):
        return self.delta
    
    def getBias(self):
        return self.bias

    def calculateValue(self):
        self.trueValue = 0.0
        for i in range(len(self.backWeights)):
            self.trueValue += (self.backWeights[i].getValue() * self.backWeights[i].getBackNode().getValue())
        self.trueValue += self.bias
        self.value = self.activationFunction(self.trueValue)

    def setDeltaToValue(self):
        self.delta = self.value

    def getBackWeightsValues(self):
        weightValues = []
        for i in range(len(self.backWeights)):
            weightValues.append(self.backWeights[i].getValue())
        return weightValues

class HiddenNeuron(Neuron, BackWeights, FrontWeights):

    def __init__(self, activationFunction, activationFunctionDerivative, minBias = -0.5, maxBias = 0.5):
        self.activationFunction = activationFunction
        self.activationFunctionDerivative = activationFunctionDerivative
        self.value = 0.0
        self.trueValue = 0.0
        self.delta = 0.0
        self.bias = random.uniform(minBias, maxBias)
        self.backWeights = []
        self.frontWeights = []

    def calculateDelta(self):
        self.delta = 0.0
        for i in range(len(self.frontWeights)):
            self.delta += (self.frontWeights[i].getDelta() * self.frontWeights[i].getFrontNode().getDelta())
        self.delta *= self.activationFunctionDerivative(self.trueValue)

    def learnWeightsAndBias(self, learningRate):
        self.calculateDelta()
        for i in range(len(self.backWeights)):
            self.backWeights[i].subtractValue(self.delta * self.backWeights[i].getBackNode().getValue() * learningRate)
        self.bias -= (self.delta * learningRate)

class OutputNeuron(Neuron):

    def calculateDelta(self, target, lossFunction):
        self.delta = lossFunction(self.value, target) * self.activationFunctionDerivative(self.trueValue)

    def learnWeightsAndBias(self, learningRate, target, lossFunction):
        self.calculateDelta(target, lossFunction)
        for i in range(len(self.backWeights)):
            self.backWeights[i].subtractValue(self.delta * self.backWeights[i].getBackNode().getValue() * learningRate)
        self.bias -= (self.delta * learningRate)

class Layer(object):

    def __init__(self, numberOfNodes):
        self.nodes = []
        for _ in range(numberOfNodes):
            self.nodes.append(Node())

    def getNodes(self):
        return self.nodes

    def getNode(self, index):
        return self.nodes[index]

    def getValues(self):
        values = []
        for i in range(len(self.nodes)):
            values.append(self.nodes[i].getValue())
        return values

class InputLayer(Layer):
    
    def __init__(self, numberOfNodes):
        self.nodes = []
        for _ in range(numberOfNodes):
            self.nodes.append(InputNode())
            
    def setInput(self, input):
        for i in range(len(self.nodes)):
            self.nodes[i].setValue(input[i])

class NeuronLayer(Layer):

    def __init__(self, numberOfNeurons, activationFunction, activationFunctionDerivative, minBias = -0.5, maxBias = 0.5):
        self.nodes = []
        for _ in range(numberOfNeurons):
            self.nodes.append(Neuron(activationFunction, activationFunctionDerivative, minBias, maxBias))

    def calculateValues(self):
        for i in range(len(self.nodes)):
            self.nodes[i].calculateValue()

    def addBackWeights(self, backLayer, minValue = -0.5, maxValue = 0.5):
        for i in range(len(self.nodes)):
            for j in range(len(backLayer.getNodes())):
                weight = Weight(backLayer.getNode(j), self.nodes[i], minValue, maxValue)
                self.nodes[i].addBackWeight(weight)
                backLayer.getNode(j).addFrontWeight(weight)
    '''
    def addConvBackWeights(self, backLayer, minValue = -0.5, maxValue = 0.5):
        numberOfNodes = len(self.nodes)
        numberOfBackNodes = len(backLayer.getNodes())
        diff = numberOfNodes - numberOfBackNodes
        if diff % 2 == 0:
            # Aligned
            for i in range(numberOfNodes):
                weight = Weight(backLayer.getNode(i), self.nodes[i], minValue, maxValue)
                self.nodes[i].addBackWeight(weight)
                backLayer.getNode(i).addFrontWeight(weight)
                j = i - 1
                if j >= 0:
                    topWeight = Weight(backLayer.getNode(j), self.nodes[i], minValue, maxValue)
                    self.nodes[i].addBackWeight(topWeight)
                    backLayer.getNode(j).addFrontWeight(topWeight)
                j = i + 1
                if j < numberOfBackNodes:
                    bottomWeight = Weight(backLayer.getNode(j), self.nodes[i], minValue, maxValue)
                    self.nodes[i].addBackWeight(bottomWeight)
                    backLayer.getNode(j).addFrontWeight(bottomWeight)
        else:
            # Not Aligned
            if numberOfNodes < numberOfBackNodes:
                for i in range(numberOfNodes):
                    weight = Weight(backLayer.getNode(i), self.nodes[i], minValue, maxValue)
                    self.nodes[i].addBackWeight(weight)
                    backLayer.getNode(i).addFrontWeight(weight)
                    j = i + 1
                    if j < numberOfBackNodes:
                        bottomWeight = Weight(backLayer.getNode(j), self.nodes[i], minValue, maxValue)
                        self.nodes[i].addBackWeight(bottomWeight)
                        backLayer.getNode(j).addFrontWeight(bottomWeight)
            else:
                for i in range(numberOfNodes):
                    if i < numberOfBackNodes:
                        weight = Weight(backLayer.getNode(i), self.nodes[i], minValue, maxValue)
                        self.nodes[i].addBackWeight(weight)
                        backLayer.getNode(i).addFrontWeight(weight)
                    j = i - 1
                    if j >= 0:
                        topWeight = Weight(backLayer.getNode(j), self.nodes[i], minValue, maxValue)
                        self.nodes[i].addBackWeight(topWeight)
                        backLayer.getNode(j).addFrontWeight(topWeight)
    '''
    def getBiases(self):
        biases = []
        for i in range(len(self.nodes)):
            biases.append(self.nodes[i].getBias())
        return biases

    def getValuesWithBiases(self):
        valueWithBias = []
        for i in range(len(self.nodes)):
            valueWithBias.append(self.nodes[i].getValue())
            valueWithBias.append(self.nodes[i].getBias())
        return valueWithBias

    def setDeltaToValue(self):
        for i in range(len(self.nodes)):
            self.nodes[i].setDeltaToValue()

class HiddenLayer(NeuronLayer):

    def __init__(self, numberOfNeurons, activationFunction, activationFunctionDerivative, minBias = -0.5, maxBias = 0.5):
        self.nodes = []
        for _ in range(numberOfNeurons):
            self.nodes.append(HiddenNeuron(activationFunction, activationFunctionDerivative, minBias, maxBias))

    def calculateDelta(self):
        for i in range(len(self.nodes)):
            self.nodes[i].calculateDelta()

    def learnWeightsAndBiases(self, learningRate):
        for i in range(len(self.nodes)):
            self.nodes[i].learnWeightsAndBias(learningRate)

class OutputLayer(NeuronLayer):

    def __init__(self, numberOfNeurons, activationFunction, activationFunctionDerivative, lossFunction, minBias = -0.5, maxBias = 0.5):
        self.lossFunction = lossFunction
        self.nodes = []
        for _ in range(numberOfNeurons):
            self.nodes.append(OutputNeuron(activationFunction, activationFunctionDerivative, minBias, maxBias))

    def calculateDelta(self, targets):
        for i in range(len(self.nodes)):
            self.nodes[i].calculateDelta(targets[i])

    def learnWeightsAndBiases(self, learningRate, target):
        for i in range(len(self.nodes)):
            self.nodes[i].learnWeightsAndBias(learningRate, target[i], self.lossFunction)

class NeuralNetwork(object):

    def __init__(self, layers, hiddenActivationFunction = f.tanh, hiddenActivationFunctionDerivative = f.tanhDerivative, outputActivationFunction = f.tanh, outputActivationFunctionDerivative = f.tanhDerivative, lossFunction = f.meanSquaredLoss, minBias = -0.5, maxBias = 0.5, minWeightValue = -0.5, maxWeightValue = 0.5):
        self.inputLayer = InputLayer(layers[0])
        self.hiddenLayers = []
        for i in range(1, len(layers) - 1):
            self.hiddenLayers.append(HiddenLayer(layers[i], hiddenActivationFunction, hiddenActivationFunctionDerivative, minBias, maxBias))
            if i > 1:
                self.hiddenLayers[i - 1].addBackWeights(self.hiddenLayers[i - 2])
            else:
                self.hiddenLayers[i - 1].addBackWeights(self.inputLayer)
        self.outputLayer = OutputLayer(layers[len(layers) - 1], outputActivationFunction, outputActivationFunctionDerivative, lossFunction, minBias, maxBias)
        self.outputLayer.addBackWeights(self.hiddenLayers[len(self.hiddenLayers) - 1], minWeightValue, maxWeightValue)

    def getOutput(self):
        output = []
        for i in range(len(self.outputLayer.getNodes())):
            output.append(self.outputLayer.getNode(i).getValue())
        return output

    def feedForward(self, input):
        self.inputLayer.setInput(input)
        for i in range(len(self.hiddenLayers)):
            self.hiddenLayers[i].calculateValues()
        self.outputLayer.calculateValues()
        return self.getOutput()

    def trainWithOutput(self, learningRate, target):
        self.outputLayer.learnWeightsAndBiases(learningRate, target)
        for i in range(len(self.hiddenLayers) - 1, -1, -1):
            self.hiddenLayers[i].learnWeightsAndBiases(learningRate)
        for i in range(len(self.hiddenLayers)):
            self.hiddenLayers[i].setDeltaToValue()
        self.outputLayer.setDeltaToValue()

    def train(self, learningRate, input, target):
        self.feedForward(input)
        self.trainWithOutput(learningRate, target)

    def trainFor(self, learningRate, inputs, targets):
        for i in range(len(inputs)):
            self.train(learningRate, inputs[i], targets[i])

    def print(self):
        print("I: " + str(self.inputLayer.getValues()))
        for i in range(len(self.hiddenLayers)):
            for j in range(len(self.hiddenLayers[i].getNodes())):
                print("W: " + str(self.hiddenLayers[i].getNode(j).getBackWeightsValues()))
            print("H: " + str(self.hiddenLayers[i].getValuesWithBiases()))
        for i in range(len(self.outputLayer.getNodes())):
            print("W: " + str(self.outputLayer.getNode(i).getBackWeightsValues()))
        print("O: " + str(self.outputLayer.getValuesWithBiases()))