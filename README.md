# Game Directory Project

## Assumptions:

- The `data` directory contains numerous files and subdirectories.
- Our focus is solely on the games within this directory.
- Each game is stored in a directory with the word "game" in its name.
- Every game directory contains a single `.go` file that requires compilation before execution.

## Project Steps/Requirements:

1. **Identify Game Directories:**
   - Traverse the `/data` directory and locate all directories containing the word "game."

2. **Create a New /games Directory:**
   - Establish a new directory named `/games` to store the modified game files.

3. **Copy and Rename Game Directories:**
   - Duplicate the game directories into the `/games` directory.
   - Remove the "game" suffix from each directory name.

4. **Generate a .json File:**
   - Create a `.json` file containing information about the games, such as names and details.

5. **Compile Game Code:**
   - Compile the `.go` file within each game directory to prepare them for execution.

6. **Run Game Code:**
   - Execute the compiled code for each game to ensure proper functionality.

## Getting Started:

1. Clone this repository to your local machine.
2. Navigate to the root directory of the project.

```bash
git clone <repository_url>
cd <repository_directory>
