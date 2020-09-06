import os
import sys
from argparse import ArgumentParser

import reviewmania



def _validate_input_args(args):
	if not os.path.isdir(args.directory):
		err_msg = ('A valid directory is required')
		
		print(f'{argparser.prog}: error: {err_msg}', file=sys.stderr)
		sys.exit()


argparser = ArgumentParser(
    prog='reviewmania',
    description='Get movie reviews from rotten tomatoes '
    			'for all movies in a directory')


argparser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 1.0')


argparser.add_argument('-d', '--directory',
    required=True,
    dest='directory',
    default=None,
    help='Specify the directory to perform the '
         'operation. It default to current directory')

args = argparser.parse_args()
_validate_input_args(args)
reviewmania.main(args)