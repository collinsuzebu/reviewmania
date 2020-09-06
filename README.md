# reviewmania
![Python](https://img.shields.io/badge/Python-v3.7.1-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

Reviewmania gives you the option to only watch movies based on rating from movie review websites. It generates a `movie_review.txt` file which contains all reviews from the specified directory to search.

## How to use

1. Clone repository: ```https://github.com/collinsuzebu/reviewmania.git```
2. Install dependencies:
```
cd reviewmania
pip install requirements.txt
```
3. Execute crawler from the command line: 
    - Regular execution: ```python3 reviewmania```
    - With a directory: ```python3 reviewmania -d /path/to/directory```
    - Get help on how to run the tool: ```python reviewmania --help```

## Limitations

- It only supports Python v3.6+.
- Support for Unix not provided.
- To avoid having timeouts on the request, you need a good internet connection to run the tool. It fails without re-trial neither does it continue from where it stopped.
- This tool was initially created to fetch review for less than 500 movies in one instance. Support for async IO would be added soon.

## License

This project is licensed under the terms of the MIT license.