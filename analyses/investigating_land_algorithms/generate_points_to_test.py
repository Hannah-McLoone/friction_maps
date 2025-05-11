import csv
import random


def generate_random_number_pairs(a, b, c, d, filename="test_points_of_amazon_land.csv"):
    numbers = [(random.randint(int(a), int(b)), random.randint(int(c), int(d))) for _ in range(5000)]
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Number 1", "Number 2"])  # Header
        for number1, number2 in numbers:
            writer.writerow([number1, number2])
    
    print(f"Successfully written 5000 random number pairs to {filename}")

# Example usage
a, b = -70, -50# Range for first number
c, d = -10, 0  # Range for second number
#generate_random_number_pairs(a //0.008333333333333333333, b//0.008333333333333333333, c //0.008333333333333333333, d//0.008333333333333333333)

