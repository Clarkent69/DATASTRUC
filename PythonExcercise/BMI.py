# Japhet Melquisedec D. Gonzales
# CS-241

def calculate_bmi(weight, height, unit):
    if unit.lower() == "metric":
        return weight / (height ** 2)
    elif unit.lower() == "imperial":
        return (weight / (height ** 2)) * 703
    else:
        return None

def main():
    print("Select unit system:")
    print("1. Metric (kg, meters)")
    print("2. Imperial (lbs, inches)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        unit = "metric"
        weight = float(input("Enter your weight in kg: "))
        height = float(input("Enter your height in meters: "))
    elif choice == "2":
        unit = "imperial"
        weight = float(input("Enter your weight in pounds: "))
        height = float(input("Enter your height in inches: "))
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    bmi = calculate_bmi(weight, height, unit)

    if bmi is not None:
        print(f"\nYour BMI is: {bmi:.2f}")
        if bmi < 18.5:
            print("You are underweight.")
        elif 18.5 <= bmi < 24.9:
            print("You have a normal weight.")
        elif 25 <= bmi < 29.9:
            print("You are overweight.")
        else:
            print("You are morbidly obese.")
    else:
        print("Error in calculating BMI.")

if __name__ == "__main__":
    main()