# Gradescope Auto-Page Selection Chrome Extension

## Description

A Chrome extension that adds an automatic page selection functionality for Gradescope, an assignment submission website.

## Prerequisites

- Python 3.x
- Flask
- Selenium WebDriver
- Google Chrome
- Beautiful Soup 4

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/GradescopeAutoPageSelection.git
    ```

2. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```

3. Run the Flask server:
    ```
    python app.py
    ```

4. Load the Chrome extension into Google Chrome through the `chrome://extensions/` URL.

*Needs section explaining how to set up Cloud Vision
## Usage

Once a user uploads a PDF of the Problem Set on the assignment submission page and lands on the page-selection page they should,
1. Open the Chrome extension and enter your Gradescope email and password.
2. Click "Submit" to initiate the auto page-selection process.

Then our extension will perform:
- Automatic login to Gradescope with provided credentials
- Parse question numbers and corresponding image links
- Perform the page selection process

All the user is left to do is **hit submit!**


## Contributing

We would love to have the extension made publicly accessible; however, Gradescope does not provide a public API for their website.  In consideration of potential legal and compute restrictions that come with scrapping a website, as well as concerns with sending personal login information over the web, we could not publicly host and distribute our extension.

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE.md)
