# Function to print the pyramid pattern
def print_pyramid(rows):
    for i in range(1, rows + 1):
        # Print leading spaces
        print(' ' * (rows - i), end='')
        
        # Print stars
        print('*' * (2 * i - 1))

# Input for the number of rows in the pyramid
rows = 8
print_pyramid(rows)

