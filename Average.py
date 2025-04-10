#Japhet Melquisedec D. Gonzales
#CS - 241

def is_good_password(password):
    """
    Checks if a password is good based on the defined criteria.

    Args:
        password: The password string to check.

    Returns:
        True if the password is good, False otherwise.
    """
    if len(password) < 8:
        return False
    has_upper = False
    has_lower = False
    has_digit = False
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
    return has_upper and has_lower and has_digit

def main():
    password = input("Please enter your password: ")
    if is_good_password(password):
        print("The password is good.")
    else:
        print("The password is not good.")

if __name__ == "__main__":
    main()