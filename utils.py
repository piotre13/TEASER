__author__ = 'Pietro Rando Mazzarino'
__date__ = '2022/06/03'
__credits__ = ['Pietro Rando Mazzarino']
__email__ = 'pietro.randomazzarino@polito.it'

import yaml


def read_config(path):
    stream = open(path, 'r')
    dictionary = yaml.load(stream,Loader=yaml.FullLoader)
    return dictionary