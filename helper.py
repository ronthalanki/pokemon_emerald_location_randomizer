import glob
import re


def save_filename_template(playthrough_id):
    return f'out/playthrough{playthrough_id}.csv'


def get_new_playthrough_id():
    files = glob.glob('out/*.csv')
    indices = [int(re.match('out/playthrough(\d+).csv', f).group(1))
               for f in files]

    return max(indices) + 1
