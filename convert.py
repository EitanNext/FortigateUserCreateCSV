import csv
import random
import string

# Function to generate a random password
def generate_password():
    chars = string.ascii_letters + string.digits + '!@#$%&'
    while True:
        # Generate a random 12-character string
        password = ''.join(random.choice(chars) for i in range(12))
        # Check if the password contains at least one upper case letter, one lower case letter, one number, and one symbol
        if (any(c.isupper() for c in password)
            and any(c.islower() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in '!@#$%&' for c in password)):
            break
    return password

# Open the CSV file and read the data
with open('names.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    # Open the output file for writing usernames and passwords
    with open('usernames_passwords.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Skip the header row in the CSV file
        next(reader)
        # Loop over each row in the CSV file and generate a username and password
        for row in reader:
            full_name = row[0]
            # Extract the first name and last name initials from the full name
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name_initial = name_parts[-1][0]
            # Create the username using the first name and last name initial
            username = f"{first_name.capitalize()}{last_name_initial.capitalize()}"
            # Generate a password for the user
            password = generate_password()
            # Write the username, password, and full name to the output file
            writer.writerow([full_name, username, password])
    with open('cli_commands.txt', 'w') as outfile:
        # Write the initial configuration line
        outfile.write('config user local\n')
        # Loop over each row in the CSV file and generate CLI commands
        csvfile.seek(0)  # Return to the beginning of the CSV file
        next(reader)  # Skip the header row
        for row in reader:
            full_name = row[0]
            # Split the full name into first and last name
            first_name, last_name = full_name.split()
            # Generate the username
            username = f'{first_name.capitalize()}{last_name.capitalize()}'
            # Generate the password
            password = generate_password()
            # Write the CLI commands for creating the user to the output file
            outfile.write(f'edit "{username}"\n')
            outfile.write(f'set passwd {password}\n')
            outfile.write('next\n')
        # Write the final end line
        outfile.write('end\n')
