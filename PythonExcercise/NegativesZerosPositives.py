def main():
    negative_numbers = []
    zero_numbers = []
    positive_numbers = []

    print("Enter integers one by one. Press Enter on a blank line to finish.\n")

    while True:
        user_input = input("Enter an integer (or a blank line to finish): ").strip()
        
        if user_input == "":
            break

        try:
            number = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid integer or a blank line.")
            continue

        if number < 0:
            negative_numbers.append(number)
        elif number == 0:
            zero_numbers.append(number)
        else:
            positive_numbers.append(number)

    print("\nNegative numbers:")
    for num in negative_numbers:
        print(num)

    print("\nZeros:")
    for num in zero_numbers:
        print(num)

    print("\nPositive numbers:")
    for num in positive_numbers:
        print(num)

if __name__ == "__main__":
    main()
