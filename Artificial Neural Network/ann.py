from random import random
from math import exp
from matplotlib import pyplot


def identical(x):
    return x


def der_identical(_x):
    return 1


def ReLU(x):
    return max(0, x)


def der_ReLU(x):
    if x > 0:
        return 1
    else:
        return 0


def threshold(x):
    if x > 0.2:
        return 1
    return 0


def der_threshold(x):
    # is just to have some function when we train the network
    return 1


def sigmoid(x):
    return (1.0 / (1.0 + exp(-x)))


def der_sigmoid(x):
    return x * (1.0 - x)


class Neuron:
    def __init__(self, no_inputs, activation_function):
        self.no_inputs = no_inputs
        self.activation_function = activation_function
        self.weights = [random() for _ in range(self.no_inputs)]
        self.output = 0

    def set_weights(self, new_weights):
        self.weights = new_weights

    def fire_neuron(self, inputs):
        u = sum([x * y for x, y in zip(inputs, self.weights)])
        self.output = self.activation_function(u)
        return self.output

    def __str__(self):
        return str(self.weights)


class Layer:
    def __init__(self, no_inputs, activation_function, no_neurons):
        self.no_neurons = no_neurons
        self.neurons = [Neuron(no_inputs, activation_function) for _ in
                        range(self.no_neurons)]

    def forward(self, inputs):
        for x in self.neurons:
            x.fire_neuron(inputs)
        return [x.output for x in self.neurons]

    def __str__(self):
        s = ''
        for i in range(self.no_neurons):
            s += ' n ' + str(i) + ' ' + str(self.neurons[i]) + '\n'
        return s


class FirstLayer(Layer):
    def __init__(self, no_neurons, bias=False):
        if bias:
            no_neurons = no_neurons + 1
        Layer.__init__(self, 1, identical, no_neurons)
        for x in self.neurons:
            x.set_weights([1])

    def forward(self, inputs):
        for i in range(len(self.neurons)):
            self.neurons[i].fire_neuron([inputs[i]])
        return [x.output for x in self.neurons]
        # return inputs


class Network:
    def __init__(self, structure, activation_function, derivative, bias=False):
        self.activation_function = activation_function
        self.derivative = derivative
        self.bias = bias
        self.structure = structure[:]
        self.no_layers = len(self.structure)
        self.layers = [FirstLayer(self.structure[0], bias)]
        for i in range(1, len(self.structure)):
            self.layers = self.layers + [Layer(self.structure[i - 1], activation_function, self.structure[i])]

    def feed_forward(self, inputs):
        self.signal = inputs[:]
        if self.bias:
            self.signal.append(1)
        for l in self.layers:
            self.signal = l.forward(self.signal)
        return self.signal

    def back_propagate(self, loss, learn_rate):
        err = loss[:]
        delta = []
        current_layer = self.no_layers - 1
        new_config = Network(self.structure, self.activation_function, self.derivative, self.bias)
        # last layer
        for i in range(self.structure[-1]):
            delta.append(err[i] * self.derivative(self.layers[-1].neurons[i].output))
            for r in range(self.structure[current_layer - 1]):
                new_config.layers[-1].neurons[i].weights[r] = self.layers[-1].neurons[i].weights[r] + learn_rate * \
                                                              delta[i] * self.layers[current_layer - 1].neurons[
                                                                  r].output
        # propagate the errors layer by layer
        for current_layer in range(self.no_layers - 2, 0, -1):

            current_delta = []
            for i in range(self.structure[current_layer]):
                current_delta.append(self.derivative(self.layers[current_layer].neurons[i].output) * sum(
                    [self.layers[current_layer + 1].neurons[j].weights[i] * delta[j] for j in
                     range(self.structure[current_layer + 1])]))

            delta = current_delta[:]
            for i in range(self.structure[current_layer]):
                for r in range(self.structure[current_layer - 1]):
                    new_config.layers[current_layer].neurons[i].weights[r] = self.layers[current_layer].neurons[
                    i].weights[r] + learn_rate * delta[i] * self.layers[current_layer - 1].neurons[r].output
        self.layers = new_config.layers

    def compute_loss(self, u, t):
        loss = []
        out = self.feed_forward(u)
        for i in range(len(t)):
            loss.append(t[i] - out[i])
        return loss[:]

    def __str__(self):
        s = ''
        for i in range(self.no_layers):
            s += ' l ' + str(i) + ' :' + str(self.layers[i])
        return s


def normalise_data(data):
    mini = data[0][0]
    maxi = data[0][0]
    for entry in data:
        for i in range(6):
            if entry[i] > maxi:
                maxi = entry[i]
            if entry[i] < mini:
                mini = entry[i]

    for i in range(len(data)):
        for j in range(6):
            data[i][j] = (data[i][j] - mini) / (maxi - mini)

    return data


def read_data(filename):
    with open(filename, "r") as f:
        u = []
        t = []
        lines = f.readlines()
        for line in lines:
            line = line.split(',')
            pelvic_incidence = float(line[0])
            pelvic_tilt = float(line[1])
            lumbar_lordosis_angle = float(line[2])
            sacral_slope = float(line[3])
            pelvic_radius = float(line[4])
            degree_spondylolisthesis = float(line[5])
            u.append([pelvic_incidence, pelvic_tilt, lumbar_lordosis_angle, sacral_slope, pelvic_radius,
                      degree_spondylolisthesis])
            if line[6].strip('\n') == 'Hernia':
                t.append([1, 0, 0])
            elif line[6].strip('\n') == 'Normal':
                t.append([0, 0, 1])
            else:
                t.append([0, 1, 0])
    f.close()
    return u, t


def test_vertebra():
    [u, t] = read_data('training_data.txt')
    u = normalise_data(u)

    errors = []
    iterations = []

    nn = Network([6, 7, 7, 3], sigmoid, der_sigmoid)
    for i in range(500):
        iterations.append(i)
        e = []
        for j in range(len(u)):
            e.append(sum(nn.compute_loss(u[j], t[j])))
            nn.back_propagate(nn.compute_loss(u[j], t[j]), 0.01)
        errors.append(sum([x ** 2 for x in e]))

    [u, t] = read_data('data.txt')
    u = normalise_data(u)

    for j in range(len(u)):
        print(u[j], t[j], nn.feed_forward(u[j]))

    pyplot.plot(iterations, errors, label='loss value vs iteration')
    pyplot.xlabel('Iterations')
    pyplot.ylabel('loss function')
    pyplot.legend()
    pyplot.show()


test_vertebra()
