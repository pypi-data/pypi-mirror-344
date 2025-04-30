# DMT AutoGui

AutoGui is a Python library that simplifies automating graphical user interfaces (GUIs) using `pyautogui`, `pyperclip`, and other related libraries. It provides a higher-level interface for common GUI automation tasks, such as finding and clicking images, typing text, taking screenshots, and interacting with system processes.  It also includes robust error handling and logging capabilities.

## Features

* **Image Recognition:**  Locate images on the screen with configurable confidence levels and timeouts.
* **Mouse Control:** Click on images or specific coordinates. Get the current mouse position.
* **Keyboard Control:** Press keys and write text.
* **Screen Operations:** Get screen size and take screenshots, optionally specifying a region.
* **System Interaction:** Open and close programs.
* **Error Handling:**  Uses `Model_Error` objects for consistent error reporting.
* **Logging:** Integrated logging with customizable levels.
* **Path Handling:**  Handles both relative and absolute file paths for images.

## Logging

AutoGui uses Python's built-in `logging` module. You can provide your own logger instance or let AutoGui create one. This allows for flexible logging configuration.

## Error Handling

All methods that can potentially fail return either a `Model_AutoGuiResponse` (on success) or a `Model_Error` (on failure). This makes it easy to check for errors and handle them appropriately.

## File Paths

The `GUIController` automatically determines the directory of the calling script and uses it as the base path for finding image files. This simplifies the use of relative paths. You can also provide absolute paths.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.