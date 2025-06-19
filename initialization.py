# This file checks if the required packages are installed, if APIs are working, etc.
from eink_display import show_message, clear_display


def check_packages():
    """
    Checks if the required packages are installed. Part 1 of the initialization process.
    :return:
    """
    try:
        import PIL

        print("All required packages are installed.")
    except ImportError as e:
        print(f"Missing package: {e.name}. Please install it using pip.")

        # Show on the E-Ink display if possible
        try:
            from eink_display import show_message
            show_message("fatal", f"Missing package: {e.name}. Please install it using pip.")
        except ImportError:
            print("E-Ink display not available to show the message.")

def full_initialization():
    """
    Runs the full initialization process, including package checks and API checks.
    :return:
    """
    clear_display() # clear display before showing the message
    show_message("info", "Initializing...")
    check_packages() # make sure all required packages are installed

    # Add more initialization steps as needed
    show_message("info", "Initialization complete. All systems go!")
