import re
import time
import math
import hashlib
import random
import string
import requests
import streamlit as st

# Function to check password strength
def check_password_strength(password):
    score = 0

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        st.error("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        st.error("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        st.error("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        st.error("❌ Include at least one special character (!@#$%^&*).")

    # Final strength evaluation
    if score == 4:
        st.success("✅ Strong Password!")
    elif score == 3:
        st.warning("⚠️ Moderate Password - Consider adding more security features.")
    else:
        st.error("❌ Weak Password - Improve it using the suggestions above.")

    return score

# Function to calculate password entropy
def calculate_entropy(password):
    unique_chars = set(password)
    entropy = len(password) * math.log2(len(unique_chars))
    return entropy

# Function to check password entropy and give feedback
def check_password_entropy(password):
    entropy = calculate_entropy(password)
    if entropy >= 50:  # Adjust this threshold
        st.success("✅ Strong Password (High entropy)")
    else:
        st.error("❌ Weak Password (Low entropy)")

# Function to check if password contains the username
def check_password_similarity(password, username):
    if username.lower() in password.lower():
        st.error("❌ Your password should not contain your username.")
    else:
        st.success("✅ Password does not match username.")

# Function to check if the password is common
def check_common_passwords(password):
    common_passwords = ['password123', '123456', 'qwerty', 'letmein', 'admin']
    if password in common_passwords:
        st.error("❌ Your password is too common. Choose a more secure one.")
    else:
        st.success("✅ Your password is not on the common password list.")

# Function to check password age
def password_age_check(last_updated_timestamp):
    current_timestamp = time.time()
    password_age = current_timestamp - last_updated_timestamp
    age_in_days = password_age / (60 * 60 * 24)
    
    if age_in_days > 180:  # Password older than 6 months
        st.warning("⚠️ Your password is more than 6 months old. Consider updating it.")
    else:
        st.success("✅ Your password is up to date.")

# Function to check password breach (using the "Have I Been Pwned" API)
def check_password_breach(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # Get the first 5 characters of the hashed password (API requirement)
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # The API response is a plain text with hashed suffixes
        hashes = response.text.splitlines()
        
        # Check if the suffix of our password's hash exists in the list of pwned passwords
        for hash in hashes:
            hash_suffix = hash.split(':')[0]  # Get only the hash prefix part
            if hash_suffix == suffix:
                st.error("❌ Your password has been involved in a data breach. Change it!")
                return
        
        st.success("✅ Your password has not been breached.")
    
    else:
        st.error("❌ Error checking password breach status.")

# Function to generate a strong password
def generate_strong_password(length=12):
    # Define possible characters
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    
    return password

# Streamlit function for password strength visualization
def password_strength_visual(password):
    score = check_password_strength(password)
    if score == 4:
        st.success("✅ Strong Password!")
        st.progress(100)
    elif score == 3:
        st.warning("⚠️ Moderate Password")
        st.progress(60)
    else:
        st.error("❌ Weak Password")
        st.progress(20)

# Main Streamlit Program
def main():
    st.title("Password Strength Meter")
    
    option = st.selectbox("Choose an option:", ["Check password strength", "Generate a strong password"])
    
    if option == "Check password strength":
        password = st.text_input("Enter your password:")
        
        # Add your username here (replace with actual username from user input if needed)
        username = "ziaukhan"
        
        if password:
            # Check the password strength
            check_password_strength(password)
        
            # Check the password entropy
            check_password_entropy(password)
        
            # Check if password contains the username
            check_password_similarity(password, username)
        
            # Check if the password is common
            check_common_passwords(password)
        
            # Check password age (You can replace the timestamp with actual data)
            last_updated = time.time() - (100 * 60 * 60 * 24)  # Example: 100 days ago
            password_age_check(last_updated)
        
            # Check if password is part of a breach (API check)
            check_password_breach(password)
        
            # Visual representation using Streamlit (optional)
            password_strength_visual(password)
        
    elif option == "Generate a strong password":
        password = generate_strong_password()
        st.write(f"Your generated strong password is: **{password}**")
        st.success("✅ Strong Password Generated Successfully!")

# Run the Streamlit app
if __name__ == "__main__":
    main()