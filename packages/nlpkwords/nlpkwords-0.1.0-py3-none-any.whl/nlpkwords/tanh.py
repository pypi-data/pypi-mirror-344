import numpy as np

def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return 1 - np.tanh(x)**2

def main():
    N = int(input("Enter number of inputs: "))
    X = np.random.randint(0, 2, size=(N, 1))
    Y = np.random.randint(0, 2, size=(1, 1))  # Expected output

    # Small random initialization
    W1 = np.random.randn(4, N) * 0.01
    b1 = np.zeros((4, 1))
    W2 = np.random.randn(3, 4) * 0.01
    b2 = np.zeros((3, 1))
    W3 = np.random.randn(1, 3) * 0.01
    b3 = np.zeros((1, 1))

    learning_rate = 0.1

    for epoch in range(1000):
        # Forward pass
        Z1 = np.dot(W1, X) + b1
        A1 = tanh(Z1)

        Z2 = np.dot(W2, A1) + b2
        A2 = tanh(Z2)

        Z3 = np.dot(W3, A2) + b3
        A3 = tanh(Z3)

        # Loss (optional for monitoring)
        loss = np.mean((A3 - Y)**2)

        # Backward pass
        dZ3 = (A3 - Y) * tanh_derivative(Z3)
        dW3 = np.dot(dZ3, A2.T)
        db3 = dZ3

        dZ2 = np.dot(W3.T, dZ3) * tanh_derivative(Z2)
        dW2 = np.dot(dZ2, A1.T)
        db2 = dZ2

        dZ1 = np.dot(W2.T, dZ2) * tanh_derivative(Z1)
        dW1 = np.dot(dZ1, X.T)
        db1 = dZ1

        # Update weights
        W3 -= learning_rate * dW3
        b3 -= learning_rate * db3
        W2 -= learning_rate * dW2
        b2 -= learning_rate * db2
        W1 -= learning_rate * dW1
        b1 -= learning_rate * db1

        # (Optional) Print loss every 100 epochs
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.4f}")

    print("\nFinal Prediction:", A3)
    print("Final Weights and Biases:")
    print("W1:", W1)
    print("b1:", b1)
    print("W2:", W2)
    print("b2:", b2)
    print("W3:", W3)
    print("b3:", b3)

if __name__ == "__main__":
    main()
