import maya.cmds as cmds
import random
from Snippets import FailExit


class activationType():
    none = 0
    sigmoid = 1
    tanH = 2

    def __init__(self, Type):
        self.value = Type


class node():
    activation = activationType(activationType.none)

    def __init__(self, activation=activationType(activationType.sigmoid)):
        self.connections = random.random()
        self.activationType = activation


class layer():
    nodes = []
    output = []

    def __init__(self, size):
        self.nodes = []
        for i in range(0, size):
            self.nodes.append(node())


class NeuralNetwork():
    layers = []
    weights = []

    def __init__(self, layout, weights):
        for l in layout:
            self.layers.append(layer(l))
        expectedWeightCount = 0
        for i in range(1, len(layout)):
            expectedWeightCount += (layout[i - 1] + 1) * layout[i]
        if len(weights) == expectedWeightCount:
            self.weights = weights
        else:
            if len(weights) != 0:
                FailExit("Weights not compatible with network layout")
            for w in range(0, expectedWeightCount):
                self.weights.append(-0.5 + random.random())

    def GetHypothesis(data):
        for d in range(0, len(data)):
            layers[0].nodes[d].output = d
        for l in range(1, layers):
            FeedForward(layers[-1], layers[l], l)
        output = []
        for o in layers(-1).nodes:
            output.append(o.output)
        return output


def DoNNTest():
    net = NeuralNetwork([2, 3, 2], [])
    for w in net.weights:
        print w
