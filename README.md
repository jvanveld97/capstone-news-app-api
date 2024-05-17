# News Hub Backend

This is the backend component of the News Hub project. It provides APIs for managing news articles and related data.

## Prerequisites

- Python 3.12
- Pipenv

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:

    ```sh
    cd your-repo
    ```

3. Install dependencies:

    ```sh
    pipenv install
    ```
# Django Server Setup Guide

This guide will help you set up and run your Django server using the debugger in Visual Studio Code.

## Prerequisites

- Visual Studio Code installed on your system.
- Python and Django installed.
- Virtual environment created for your Django project.

## Start the Debugger

1. **Open Visual Studio Code:** Open your project directory in Visual Studio Code.

2. **Ensure interpreter is set to the virtual environment:**
   - CMD + Shift + P and select Python: Select Interpreter
   - Select the interpreter that corresponds to your virtual environment in your terminal (e.g., `/.local/share/virtualenvs/jv-capstone-news-api-L1uKDuQa/bin/activate`).

3. **Start the debugger:**
   - Press `F5` or click on the green play button in the Debug view.

4. **Verify server is running:**
   - Open your terminal in VS code to verify that your Django server is running.

     (e.g., `Watching for file changes with StatReloader
      Performing system checks...
      
      System check identified no issues (0 silenced).
     
      May 17, 2024 - 16:42:54
     
      Django version 5.0.6, using settings 'newsproject.settings'
     
      Starting development server at http://127.0.0.1:8000/
     
      Quit the server with CONTROL-C.`).

By following these steps, you can start your Django server using the debugger in Visual Studio Code.
