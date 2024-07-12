# SiteHealthChecker
# Overview
This project contains a Python script designed to asynchronously fetch URLs from a given list, utilizing aiohttp for HTTP requests and handling potential errors such as unauthorized access, not found errors, server errors, and connection timeouts. The script supports basic authentication and retries the request up to three times in case of failures.

# Prerequisites
Before running the script, ensure you have Python 3.7+ installed along with the following Python packages:

```bash
pip install aiohttp
pip install numpy
pip install tqdm
pip install pandas
```


# Prepare the URL Paths File
Create a JSON file (user-data/url_paths.json) containing the URL paths you want to fetch. For example:

```json
[
    "/path1/",
    "/path2/",
    "/path3/"
]
```

# Configure the Script
Edit the script to set the base_url, user, and password variables:

```python
if __name__ == "__main__":
    file_path = './user-data/url_paths.json'
    base_url = 'https://www.example.com' # Add your base URL
    user = '' # Add your username
    password = '' # Add your password
    asyncio.run(main(file_path, base_url, user, password))
```

# Run the Script
Run the script using the following command:

```bash
python3 async_web_response.py
```

# Output
The script will print messages indicating the status of the failed URLs fetch attempts, including any errors encountered (e.g., unauthorized access, not found, server error, or timeout).


# Code Explanation
Functions

load_urls(file_path): Loads URL paths from a specified JSON file.

fetch(session, url, user, password): Asynchronously fetches a URL with basic authentication, handling retries and printing status messages for various HTTP response codes and errors.

get_tasks(session, urls, base_url, user, password): Creates a list of asynchronous tasks for each URL path, combining the base URL with each path.

main(file_path, base_url, user, password): Loads URLs, creates a session with a connection pool, and gathers the asynchronous tasks for execution.
