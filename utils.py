import os
import re

# import pandas as pd

from const import SUPPORTED_FORMATS


def checkfile(path):
    """
		Checks if a file to add movie-rating already exist in the dir
		if it exists, create a new file with an incremental name

		Positional arguments
		path 			-- full path to a file
		
		returns 		-- file path
	"""
    pathd = os.path.expanduser(path)
    if not os.path.exists(path):
        return path

    root, ext = os.path.splitext(pathd)
    dir_ = os.path.dirname(root)
    fname = os.path.basename(root)
    target = fname + ext
    index = 1
    ls = set(os.listdir(dir_))

    while target in ls:
        target = "{}_{}{}".format(fname, index, ext)
        index += 1
    return os.path.join(dir_, target)


def proper_capitalization(string):
    return " ".join(word[0].upper() + word[1:] for word in string.split())


def is_supported(v_format):
    v_format = os.path.splitext(v_format)[1].strip().upper()
    return v_format in SUPPORTED_FORMATS["movies"]


def total_videos(directory):
    total = [m for m in os.listdir(directory) if is_supported(m)]

    return len(total)


def printf(string, color="reset"):
    r = (
        f"{SUPPORTED_FORMATS['colors'][color]}"
        f"{string}"
        f"{SUPPORTED_FORMATS['colors']['reset']}"
    )
    print(r)


def clean_title(movie_title, yr=False):
    """
		Clean movie title to make it a searchable name in rottentomatoes website

		Positional arguments
		movie_title		--	The movie title to be cleaned up

		Keyword arguments
		yr 				--	If set to true, it tncludes the year 
							movie was released

		returns 		--	movie title
							type(str)
	"""
    # find all word separating characters
    splitter = re.findall(r"[\.|_|\-|\s]", movie_title)
    splitter = set(splitter)  # Only select the unique characters
    stopwords = SUPPORTED_FORMATS["stopwords"]

    for split_sign in splitter:
        movie_title = "_".join(movie_title.split(split_sign))
    movie_title = movie_title.split("_")

    try:
        if movie_title[0].lower() in stopwords:
            movie_title.remove(movie_title[0])
        movie_title = [
            " ".join(movie_title[: movie_title.index(word)])
            for word in movie_title
            if word.lower() in stopwords
        ][0]
    except IndexError:
        movie_title = " ".join(movie_title)

    movie_title = re.sub(r"\s+", " ", movie_title)
    movie_title = movie_title.replace("[", "(")

    year = re.search(r"\(?(\d{4})\)?", movie_title)
    if year:
        movie_title = (
            movie_title[: movie_title.index(year.group(1))]
            + "("
            + movie_title[movie_title.index(year.group(1)[0]) :]
        )
    else:
        movie_title = movie_title

    movie_title = proper_capitalization(movie_title)

    if "(" in movie_title:  # Check to see if common pattern such as '(' exist in string
        start_delete = movie_title.index(
            "("
        )  # If it exist, it's additional data can be safely removed
        movie_title = movie_title[:start_delete].strip()

        if yr and year:
            return f"{movie_title} {year.group(1)}"
        else:
            return movie_title
    else:
        return movie_title


class FileWriter:
    def __init__(self, filename):
        self.filename = filename
        self.file_path = os.path.join(
            os.path.normpath(os.path.expanduser("~/Desktop")), filename
        )
        self.file_path2 = os.path.join(
            os.path.normpath(os.path.expanduser("~/Desktop")), "final_" + filename
        )

    def create(self):
        self.file_path = checkfile(self.file_path)
        with open(self.file_path, "w") as f:
            pass

    def append(self, data):
        with open(self.file_path, "a") as f:
            f.write(str(data))
            f.write("\n")

    def create_text_file(self, movie_list):
        df = pd.DataFrame(
            movie_list, columns=["movie_name", "movie_year", "movie_review"]
        )  # Create a pandas dataframe
        df.index = df.index + 1  # Set index to start counting from 1
        export_df = df.to_csv(
            self.file_path2, sep="\t", index=True, encoding="utf-8", header=True
        )  # Export file to text
