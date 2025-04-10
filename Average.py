#Japhet Melquisedec D. Gonzales
#CS - 241

def main():
    total = 0
    count = 0

    first_value = float(input("Enter the first value (enter 0 to stop): "))

    if first_value == 0:
        print("Error: You must enter at least one value before the sentinel.")
        return

    total += first_value
    count += 1

    while True:
        next_value = float(input("Enter the next value (enter 0 to stop): "))
        if next_value == 0:
            break
        total += next_value
        count += 1

    average = total / count
    print(f"The average of the entered values is: {average:.2f}")

if __name__ == "__main__":
    main()