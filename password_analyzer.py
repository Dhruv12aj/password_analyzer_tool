import re
import os

def password_meter_score(password):
    length = len(password)
    upper_case = len(re.findall(r'[A-Z]', password))
    lower_case = len(re.findall(r'[a-z]', password))
    numbers = len(re.findall(r'[0-9]', password))
    symbols = len(re.findall(r'[^a-zA-Z0-9_]', password))
    middle_num_sym = len(re.findall(r'(?<=.)[0-9\W](?=.)', password))

    # checks
    sequential_letters = 0
    sequential_numbers = 0
    sequential_symbols = 0

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    numbers_seq = "0123456789"
    symbols_seq = ")!@#$%^&*()"

    lower_pass = password.lower()

    for i in range(len(alphabet) - 2):
        seq = alphabet[i:i+3]
        if seq in lower_pass or seq[::-1] in lower_pass:
            sequential_letters += 1

    for i in range(len(numbers_seq) - 2):
        seq = numbers_seq[i:i+3]
        if seq in lower_pass or seq[::-1] in lower_pass:
            sequential_numbers += 1

    for i in range(len(symbols_seq) - 2):
        seq = symbols_seq[i:i+3]
        if seq in password or seq[::-1] in password:
            sequential_symbols += 1

    # Additions
    score = 0
    score += length * 4
    if upper_case:
        score += (length - upper_case) * 2
    if lower_case:
        score += (length - lower_case) * 2
    if numbers:
        score += numbers * 4
    if symbols:
        score += symbols * 6
    score += middle_num_sym * 2

    requirements = 0
    if length >= 8: requirements += 1
    if upper_case > 0: requirements += 1
    if lower_case > 0: requirements += 1
    if numbers > 0: requirements += 1
    if symbols > 0: requirements += 1
    if requirements >= 4:
        score += requirements * 2

  
    if upper_case + lower_case == length:  # only letters
        score -= length
    if numbers == length:  # only numbers
        score -= length
    # repeat chars penalty
    repeat_chars = {}
    for char in password.lower():
        repeat_chars[char] = repeat_chars.get(char, 0) + 1
    if any(v > 1 for v in repeat_chars.values()):
        repeat_penalty = sum(v for v in repeat_chars.values()) - len(repeat_chars)
        score -= int(repeat_penalty * (len(password) / (len(set(password)) or 1)))
    # Consecutive
    score -= (len(re.findall(r'[A-Z]{2,}', password)) - 1) * 2
    score -= (len(re.findall(r'[a-z]{2,}', password)) - 1) * 2
    score -= (len(re.findall(r'[0-9]{2,}', password)) - 1) * 2
    # Sequential
    score -= sequential_letters * 3
    score -= sequential_numbers * 3
    score -= sequential_symbols * 3

    # Normalize
    score = max(0, min(score, 100))
    return score

def strength_label(score):
    if score >= 90:
        return "Very Strong"
    elif score >= 80:
        return "Strong"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Moderate"
    else:
        return "Weak"

def analyze_password(password):
    score = password_meter_score(password)
    print(f"Password: {password}\nScore: {score}%\nStrength: {strength_label(score)}\n{'-'*40}")

def main():
    while True:  # keeps looping until user exits
        print("\n=== Password Analyzer Tool ===")
        print("1) Analyze password")
        print("2) Analyze password file")
        print("3) Exit")

        choice = input("Enter choice: ").strip()
        if choice == "1":
            pwd = input("Enter password: ").strip()
            analyze_password(pwd)
        elif choice == "2":
            file_path = input("Enter file path: ").strip()
            if file_path.startswith("file://"):
                file_path = file_path[7:]
            if not os.path.exists(file_path):
                print("❌ File not found.")
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    pwd = line.strip()
                    if pwd:
                        analyze_password(pwd)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
