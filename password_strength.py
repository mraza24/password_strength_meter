import re
import random
import string

# Function to generate a strong password
def generate_password():
    # Define the character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*"

    # Combine all characters
    all_characters = lowercase + uppercase + digits + special_characters

    # Randomly pick one character from each category to ensure strength
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_characters)
    ]

    # Fill the rest of the password length (8 characters) randomly
    password += random.choices(all_characters, k=4)

    # Shuffle the password to make it more random
    random.shuffle(password)

    # Convert the list to a string and return the password
    return ''.join(password)

def check_password_strength(password):
    score = 0
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        print("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        print("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        print("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        print("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score == 4:
        print("✅ Strong Password!")
    elif score == 3:
        print("⚠️ Moderate Password - Consider adding more security features.")
    else:
        print("❌ Weak Password - Improve it using the suggestions above.")

# Main function
def main():
    print("Password Strength Meter")
    print("1. Check password strength")
    print("2. Generate a strong password")
    
    choice = input("Choose an option (1/2): ")

    if choice == '1':
        password = input("Enter your password: ")
        check_password_strength(password)
    elif choice == '2':
        print("\nGenerated strong password: ", generate_password())
    else:
        print("Invalid option. Please choose 1 or 2.")

# Run the program
if __name__ == "__main__":
    main()