import os

def generate_color_bar_graph(percentage):
    # Define color codes for Windows command line
    color_codes = {
        "red": "4",
        "green": "2",
        "yellow": "6",
        "blue": "1",
        "magenta": "5",
        "cyan": "3",
        "white": "7"
    }

    # Calculate number of characters for the bar graph
    num_chars = int(percentage / 2)

    # Generate the colored bar graph
    bar_graph = ""
    for color in color_codes.values():
        bar_graph += f"\033[4{color}m{'█' * num_chars}\033[0m"

    # Print the bar graph
    os.system("cls")  # Clear screen (Windows command)
    print(bar_graph)
    print(f"Percentage: {percentage}%")

# Test the function
percentage = float(input("Enter percentage: "))
generate_color_bar_graph(percentage)
