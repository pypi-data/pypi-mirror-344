def nim_game():
    print("Welcome to the Nim Game!")

    stones = int(input("Enter the initial number of stones: "))
    player = input("Enter your name: ")

    current_player = player  # You start first

    while stones > 0:
        print(f"\nCurrent stones: {stones}")

        if current_player == player:
            try:
                move = int(input(f"{player}, remove 1, 2, or 3 stones: "))
                if move not in [1, 2, 3] or move > stones:
                    print("Invalid move! Try again.")
                    continue
            except ValueError:
                print("Please enter a valid number.")
                continue
        else:
            # Smart move: leave multiple of 4
            if stones % 4 == 0:
                move = 1  # no perfect move, just pick 1
            else:
                move = stones % 4
            print(f"Computer removes {move} stones.")

        stones -= move

        if stones == 0:
            if current_player == player:
                print(f"\n{player} wins!")
            else:
                print("\nComputer wins!")
            break

        # Switch turn
        current_player = "Computer" if current_player == player else player

if __name__ == "__main__":
    nim_game()
