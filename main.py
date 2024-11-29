from fpdf import FPDF
import random
import string
import os

# Function to place words in the grid
def place_words_in_grid(words, size, max_attempts=1000):
    grid = [['' for _ in range(size)] for _ in range(size)]
    directions = ['horizontal', 'vertical', 'diagonal',
                  'reverse_horizontal', 'reverse_vertical', 'reverse_diagonal']
    unplaced_words = []

    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < max_attempts:
            direction = random.choice(directions)
            word_length = len(word)
            if direction == 'horizontal':
                row = random.randint(0, size - 1)
                col = random.randint(0, size - word_length)
                if all(grid[row][col + i] in ('', c) for i, c in enumerate(word)):
                    for i, c in enumerate(word):
                        grid[row][col + i] = c
                    placed = True
            elif direction == 'vertical':
                row = random.randint(0, size - word_length)
                col = random.randint(0, size - 1)
                if all(grid[row + i][col] in ('', c) for i, c in enumerate(word)):
                    for i, c in enumerate(word):
                        grid[row + i][col] = c
                    placed = True
            elif direction == 'diagonal':
                row = random.randint(0, size - word_length)
                col = random.randint(0, size - word_length)
                if all(grid[row + i][col + i] in ('', c) for i, c in enumerate(word)):
                    for i, c in enumerate(word):
                        grid[row + i][col + i] = c
                    placed = True
            elif direction == 'reverse_horizontal':
                row = random.randint(0, size - 1)
                col = random.randint(word_length - 1, size - 1)
                if all(grid[row][col - i] in ('', c) for i, c in enumerate(word)):
                    for i, c in enumerate(word):
                        grid[row][col - i] = c
                    placed = True
            elif direction == 'reverse_vertical':
                row = random.randint(word_length - 1, size - 1)
                col = random.randint(0, size - 1)
                if all(grid[row - i][col] in ('', c) for i, c in enumerate(word)):
                    for i, c in enumerate(word):
                        grid[row - i][col] = c
                    placed = True
            elif direction == 'reverse_diagonal':
                row = random.randint(word_length - 1, size - 1)
                col = random.randint(word_length - 1, size - 1)
                if all(grid[row - i][col - i] in ('', c) for i, c in enumerate(word)):
                    for i, c in enumerate(word):
                        grid[row - i][col - i] = c
                    placed = True
            attempts += 1
        if not placed:
            unplaced_words.append(word)
    return grid, unplaced_words

# Function to fill empty grid cells with random letters
def fill_grid_with_random_letters(grid):
    letters = string.ascii_uppercase
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '':
                grid[row][col] = random.choice(letters)
    return grid

# Generate the word search grid
def generate_word_search(words, grid_size):
    while True:
        grid, unplaced_words = place_words_in_grid(words, grid_size)
        if not unplaced_words:
            return grid
        grid_size += 1

# Create PDF with improved formatting and a solution page
def create_pdf(grid, solution_grid, words, pdf_path):
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.set_margins(10, 10, 10)  # Reduce left, top, and right margins
    pdf.add_page()

    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Christmas Word Search", ln=1, align="C")

    # Add word bank with reduced font size
    pdf.set_font("Arial", size=8)  # Reduced font size for the word bank
    pdf.cell(0, 8, "Word Bank:", ln=1)

    # Dynamically adjust columns for word bank
    page_width = pdf.w - 20  # Adjusted width after reducing margins
    max_word_length = max(len(word) for word in words)
    columns = 8  # Set the desired number of columns here
    column_width = page_width / columns

    # Split words into rows based on the number of columns
    words_sorted = sorted(words)
    rows = [words_sorted[i:i + columns] for i in range(0, len(words_sorted), columns)]

    # Print each row of words in aligned columns
    for row in rows:
        for word in row:
            pdf.cell(column_width, 5, word, border=0, align='L')  # Use column width for consistent spacing
        pdf.ln(4)  # Slightly reduced row height
    pdf.ln(4)  # Add extra spacing after word bank

    # Add the word search grid
    pdf.set_font("Courier", size=10)  # Smaller font for a compact grid

    grid_size = len(grid)
    cell_width = (pdf.w - 20) / grid_size  # Utilize full page width
    cell_height = 4  # Shorter row height for compactness

    # Print the grid
    for row in grid:
        for cell in row:
            pdf.cell(cell_width, cell_height, cell, border=0, align='C')  # Center-align each cell
        pdf.ln(cell_height)  # Move to the next row
    pdf.ln(5)  # Add a small space below the grid

    # Add solution page
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Solution - Christmas Word Search", ln=1, align="C")

    pdf.set_font("Courier", size=6)  # Match font size with the grid
    for row in solution_grid:
        for cell in row:
            pdf.cell(cell_width, cell_height, cell, border=0, align='C')
        pdf.ln(cell_height)

    # Save the PDF
    try:
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        pdf.output(pdf_path)
        print(f"PDF successfully saved at: {pdf_path}")
    except Exception as e:
        print(f"An error occurred while saving the PDF: {e}")

def main():
    # List of words
    words = [
        "CHRISTMAS", "HOLIDAY", "SANTA", "REINDEER", "SNOWFLAKE", "ORNAMENT",
        "CAROL", "MISTLETOE", "PRESENT", "ELF", "CANDY", "JOLLY", "STOCKING",
        "GINGERBREAD", "SLEIGH", "NUTCRACKER", "BELLS", "FROSTY", "WREATH",
        "NOEL", "YULETIDE", "HOLLY", "TINSEL", "JOY", "LIGHTS", "PEACE",
        "FAMILY", "FRIENDS", "CELEBRATE", "WINTER"
    ]
    extra_words = ["SNOWMAN", "ICICLE", "COOKIES", "FESTIVE", "RUDOLPH",
                   "NORTHPOLE", "SLEDDING", "BLIZZARD", "FIREPLACE",
                   "SNOWBALL", "CHIMNEY"]
    all_words = words + extra_words

    # Initial grid size
    initial_grid_size = max(len(max(all_words, key=len)) + 5, len(all_words))
    grid = generate_word_search(all_words, initial_grid_size)

    # Copy grid for solution before random letter fill
    solution_grid = [row[:] for row in grid]
    grid = fill_grid_with_random_letters(grid)

    # Define PDF path
    output_dir = os.path.expanduser("WordSearchPuzzles")
    pdf_filename = "Christmas_Word_Search_Puzzle_Improved.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    # Create PDF
    create_pdf(grid, solution_grid, all_words, pdf_path)

if __name__ == "__main__":
    main()
