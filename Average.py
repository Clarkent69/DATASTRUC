#Japhet Melquisedec D. Gonzales
#CS - 241

def main():
    total = 0 
    count = 0
    
    first_value = float(input("Please Enter your First value (Enter 0 to stop): "))
    
    if first_value == 0:
        print("Error: You must enter at least one value.")
        return
    
    total += first_value
    count += 1
    
    while True:
        next_value = float(input("Please Enter the next value (enter 0 to stop): "))
        if next_value == 0:
            break
        total += next_value
        count += 1
        
        average = total / count
    print(f"The average of the entered values is: {average:.1f}")

if __name__ == "__main__":
    main()