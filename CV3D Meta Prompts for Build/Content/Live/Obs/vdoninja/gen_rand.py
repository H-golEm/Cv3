import random
import string

def generate_random_string(length=25):
    characters = string.ascii_letters + string.digits  # Combines letters and digits
    return ''.join(random.choice(characters) for _ in range(length))

# Generate the string
random_string = generate_random_string()
print(random_string)
