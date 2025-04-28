import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

def main():
    N = int(input("Enter number of inputs: "))
    X = np.random.randint(0, 2, size=(N, 1))
    Y = np.random.randint(0, 2, size=(1, 1))  # Expected output

    W1 = np.random.rand(4, N)
    b1 = np.random.rand(4, 1)
    W2 = np.random.rand(3, 4)
    b2 = np.random.rand(3, 1)
    W3 = np.random.rand(1, 3)
    b3 = np.random.rand(1, 1)

    learning_rate = 0.1

    for epoch in range(1000):
        # Forward pass
        Z1 = np.dot(W1, X) + b1
        A1 = sigmoid(Z1)

        Z2 = np.dot(W2, A1) + b2
        A2 = sigmoid(Z2)

        Z3 = np.dot(W3, A2) + b3
        A3 = sigmoid(Z3)

        # Backward pass
        dZ3 = A3 - Y
        dW3 = np.dot(dZ3, A2.T)
        db3 = dZ3

        dZ2 = np.dot(W3.T, dZ3) * sigmoid_derivative(Z2)
        dW2 = np.dot(dZ2, A1.T)
        db2 = dZ2

        dZ1 = np.dot(W2.T, dZ2) * sigmoid_derivative(Z1)
        dW1 = np.dot(dZ1, X.T)
        db1 = dZ1

        # Update weights
        W3 -= learning_rate * dW3
        b3 -= learning_rate * db3
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2
        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1

    print("Final Prediction:", A3)
    print("Final Weights and Biases:")
    print("W1:", W1)
    print("b1:", b1)
    print("W2:", W2)
    print("b2:", b2)
    print("W3:", W3)
    print("b3:", b3)

if __name__ == "__main__":
    main()
