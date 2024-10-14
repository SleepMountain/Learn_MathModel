import numpy as np


# 定义激活函数及其导数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# 定义神经网络类
class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        for i in range(1, len(layers)):
            w = np.random.randn(layers[i], layers[i-1])
            self.weights.append(w)

    def forward_propagation(self, inputs):
        activations = [inputs]
        for w in self.weights:
            output = sigmoid(np.dot(w, activations[-1]))
            activations.append(output)
        return activations

    def backward_propagation(self, activations, targets):
        delta = activations[-1] - targets
        gradients = [delta * sigmoid_derivative(activations[-1])]
        for i in range(len(self.layers)-2, 0, -1):
            delta = np.dot(self.weights[i].T, delta) * sigmoid_derivative(activations[i])
            gradients.insert(0, delta)
        return gradients

    def update_weights(self, gradients, learning_rate):
        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * np.dot(gradients[i], self.activations[i].T)

    def train(self, input_data, target_data, epochs, learning_rate):
        for _ in range(epochs):
            for inputs, targets in zip(input_data, target_data):
                activations = self.forward_propagation(inputs)
                gradients = self.backward_propagation(activations, targets)
                self.update_weights(gradients, learning_rate)

    def predict(self, inputs):
        activations = self.forward_propagation(inputs)
        return activations[-1]

# 使用示例
input_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
target_data = np.array([[0], [1], [1], [0]])

layers = [2, 4, 1]  # 输入层有两个神经元，隐藏层有四个神经元，输出层有一个神经元

nn = NeuralNetwork(layers)
nn.train(input_data, target_data, epochs=10000, learning_rate=0.1)  # 训练神经网络

# 验证预测结果
for inputs in input_data:
    prediction = nn.predict(inputs)
    print("输入:", inputs, "预测结果:", prediction)
