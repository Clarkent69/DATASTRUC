#Japhet Melqusiedec D. Gonzales
#CS-241

def main():
    unique_words = []
    check = set()
    
    print("Enter words (press Enter on a blank line to finish):")
    while True:
        #the strip function purpose is to remove any spaces to the input of the user so it wont be registered as a new word when it isnt
        user_input = input().strip() 
        if user_input == "": #this simply checks if the user enters a blank input
            break
        if user_input not in check:
            unique_words.append(user_input)
            check.add(user_input)
    
    print("\nUnique words in original order:")
    print("\n".join(unique_words))

if __name__ == "__main__":
    main()