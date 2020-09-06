'''
	This program sorts all movies in a directory based on review from
	RottenTomato.

	### Author	--- Collins Uzebu
	### Created --- Dec 3, 2019
'''


import re, os
import enzyme # for handling meta data in "mkv" video files
import requests
import concurrent.futures
from pathlib import Path

from const import SUPPORTED_FORMATS
from utils import (
					checkfile, FileWriter, clean_title,
					proper_capitalization, total_videos,
					is_supported, printf
				)




def get_tfpdl_title(movie_name, movie_path):
	"""
		Gets title of movie, if movie is gotten from torrent
		params: 
				full name of movie -- movie.mkv
				full path to movie -- C:/movie.mkv
		return: 
				title of movie --> Type (str)
	"""
	information = movie_name
	if 'tfpdl' in movie_name and os.path.splitext(movie_name)[1] == '.mkv':
		with open(movie_path, 'rb') as f:
			mkv = enzyme.MKV(f)
		information = mkv.info.title
		information = information.split('-')[1]
	return information.strip()





def search_movie(movie_title):
	'''
		This function fetches data from rotten tomatoes website
		It returns the search result from the first page

		params: movie_title to be searched
				year - year of movie. If True searches the movie with year.
		return: List of tuples --> [(movie title, year, rating),]
	'''
	mov_title = movie_title[:-5] if movie_title[-4:].isdigit() else movie_title
	search_url = 'https://www.rottentomatoes.com/napi/search/?limit=9&query=' + re.sub(' ', '%20', mov_title)
	resp = requests.get(search_url)
	resp = resp.json()
	# resp = {"actors":[],"critics":[],"franchises":[],"movies":[{"name":"Green Book","year":2018,"url":"/m/green_book","image":"https://resizing.flixster.com/zIIzoN8sunZj1FGpSu6KX_ZuGzA=/fit-in/80x80/v1.bTsxMjgyMzMzODtqOzE4MzczOzEyMDA7MzE1ODs1MDAw","meterClass":"certified_fresh","meterScore":78,"castItems":[{"name":"Viggo Mortensen","url":"/celebrity/viggo_mortensen"},{"name":"Mahershala Ali","url":"/celebrity/mahershala_ali"},{"name":"Linda Cardellini","url":"/celebrity/linda_cardellini"}],"subline":"Viggo Mortensen, Mahershala Ali, Linda Cardellini, "},{"name":"The Green Book: Guide to Freedom","year":2019,"url":"/m/the_green_book_guide_to_freedom","image":"https://resizing.flixster.com/JGegwrMVJ-lxY01iA_j6oMqHApk=/fit-in/80x80/v1.bTsxMzAxOTA2MztqOzE4Mzc1OzEyMDA7MjI1MDszMDAw","meterClass":"N/A","meterScore":'null',"castItems":[],"subline":'null'}],"tvSeries":[],"actorCount":0,"criticCount":0,"franchiseCount":0,"movieCount":2,"tvCount":0}
	resp = resp['movies']
	accum = []
	for movie in resp:
		name = movie['name']
		year = movie['year']
		score = movie['meterScore']
		tup = (name, year, score)
		if movie_title[-4:].isdigit() and int(movie_title[-4:]) == tup[1]:
			return [(name, year, score)]
		if mov_title.lower() == tup[0].lower() or len(tup[0]) <= len(mov_title)+4:
			accum.append((name, year, score))
	return accum


def main(args):
	movie_directory = args.directory
	total = total_videos(movie_directory)
	
	printf(f"There are '{total}' movie(s) in this directory", "cyan")

	fw = FileWriter('movie_review.txt')
	fw.create() #create a text file
	
	cleaned_title_list = []
	
	try:
		for movie in os.listdir(movie_directory):
			if is_supported(movie):
				mv_path = os.path.join(movie_directory, movie)
				tfpdl_data = get_tfpdl_title(movie, mv_path)
				cleaned_title = clean_title(os.path.splitext(tfpdl_data)[0], yr=True)

				cleaned_title_list.append(cleaned_title)

		with concurrent.futures.ProcessPoolExecutor() as executor:
			searched = executor.map(search_movie, cleaned_title_list)
			record_movie = [fw.append(mov) for mov_lst in searched for mov in mov_lst]
			printf('[+] Review search completed...', "green")

	except KeyError:
		printf('[-] There was a problem with fetching data due to poor internet connection...', "red")

	except requests.exceptions.ConnectionError:
		printf('[-] There was a problem with your internet connection...', "red")