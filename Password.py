#Japhet Melquisedec D. Gonzales
#CS - 241

def is_good_password(password):
    if len(password) < 8:
        return False
    
    has_uppercase = any(char.isupper()for char in password)
    has_lowercase = any(char.islower()for char in password)
    has_digit = any(char.isdigit()for char in password)
    
    return has_uppercase and has_lowercase and has_digit

def main():
    password = input ("Enter a Password to check if it's good!: ") 
    
    if is_good_password(password):
        print("That is a good password!")
    else:
        print(" That password is not good. It must be at least 8 characters long, must Atleast contain at least one uppercase letter, one lowercase letter, and one number" )

if __name__ == "__main__":
    main()
