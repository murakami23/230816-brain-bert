import os
import configparser
import numpy as np
from scipy import signal
from BrainBertFunc import get_stft, downsampling, plot_stft

conf = configparser.ConfigParser()
conf.read('./conf.ini')

original_sf = 9600  # 9600
re_sf = 2048  # 2048

work_dir = os.getcwd()
js_dir = "js13"
npy_path = "js13-exp-1-1001-8-mf-150-mb350-ECoG-t1.npy"

input_path = f'{work_dir}/{js_dir}/{npy_path}'

# Load the input data
input_data = np.load(input_path)
downsampled_data = downsampling(input_data)
plot_stft(downsampled_data, 10)