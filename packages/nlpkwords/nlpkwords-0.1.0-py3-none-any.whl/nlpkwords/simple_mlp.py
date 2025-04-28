import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def main():
    N = int(input("Enter number of inputs: "))
    
    # Random binary input X (reshaped to be a column vector)
    X = np.random.randint(0, 2, size=(N, 1))
    print("Input X:", X.T)  # Transpose to show as row vector
    
    # Random weight initialization
    W1 = np.random.rand(3, N)
    b1 = np.random.rand(3, 1)

    W2 = np.random.rand(2, 3)
    b2 = np.random.rand(2, 1)

    W3 = np.random.rand(1, 2)
    b3 = np.random.rand(1, 1)

    # Forward pass
    Z1 = sigmoid(np.dot(W1, X) + b1)  # 3x1
    Z2 = sigmoid(np.dot(W2, Z1) + b2)  # 2x1
    output = sigmoid(np.dot(W3, Z2) + b3)  # 1x1

    print("Final Output:", output)
    print("Final Weights and Biases:")
    print("W1:", W1)
    print("b1:", b1)
    print("W2:", W2)
    print("b2:", b2)
    print("W3:", W3)
    print("b3:", b3)

if __name__ == "__main__":
    main()
