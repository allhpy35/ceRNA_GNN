import numpy as np, sys, os, random, pdb, json, uuid, time, argparse
from pprint import pprint
import logging, logging.config
from collections import defaultdict as ddict
from ordered_set import OrderedSet

# PyTorch related imports
import torch
from torch.nn import functional as F
from torch.nn.init import xavier_normal_
from torch.utils.data import DataLoader
from torch.nn import Parameter
#from torch_scatter import scatter_add

np.set_printoptions(precision=4)

def set_gpu(gpus):
	"""
	Sets the GPU to be used for the run

	Parameters
	----------
	gpus:           List of GPUs to be used for the run
	
	Returns
	-------
		
	"""
	os.environ["CUDA_DEVICE_ORDER"]    = "PCI_BUS_ID"
	os.environ["CUDA_VISIBLE_DEVICES"] = gpus

def get_logger(name, log_dir, config_dir):
	"""
	Creates a logger object

	Parameters
	----------
	name:           Name of the logger file
	log_dir:        Directory where logger file needs to be stored
	config_dir:     Directory from where log_config.json needs to be read
	
	Returns
	-------
	A logger object which writes to both file and stdout
		
	"""
	config_dict = json.load(open( config_dir + 'log_config.json'))
	config_dict['handlers']['file_handler']['filename'] = log_dir + name.replace('/', '-')
	logging.config.dictConfig(config_dict)
	logger = logging.getLogger(name)

	std_out_format = '%(asctime)s - [%(levelname)s] - %(message)s'
	consoleHandler = logging.StreamHandler(sys.stdout)
	consoleHandler.setFormatter(logging.Formatter(std_out_format))
	logger.addHandler(consoleHandler)

	return logger

def get_combined_results(left_results, right_results):
	results = {}
	count   = float(left_results['count'])

	results['left_mr']	= round(left_results ['mr'] /count, 5)
	results['left_mrr']	= round(left_results ['mrr']/count, 5)
	results['right_mr']	= round(right_results['mr'] /count, 5)
	results['right_mrr']	= round(right_results['mrr']/count, 5)
	results['mr']		= round((left_results['mr']  + right_results['mr']) /(2*count), 5)
	results['mrr']		= round((left_results['mrr'] + right_results['mrr'])/(2*count), 5)

	for k in range(10):
		results['left_hits@{}'.format(k+1)]	= round(left_results ['hits@{}'.format(k+1)]/count, 5)
		results['right_hits@{}'.format(k+1)]	= round(right_results['hits@{}'.format(k+1)]/count, 5)
		results['hits@{}'.format(k+1)]		= round((left_results['hits@{}'.format(k+1)] + right_results['hits@{}'.format(k+1)])/(2*count), 5)
	return results

def get_param(shape):
	param = Parameter(torch.Tensor(*shape)); 	
	xavier_normal_(param.data)
	return param

def com_mult(a, b):
	r1, i1 = a.real, a.imag  # a 텐서의 실수부, 허수부
	r2, i2 = b.real, b.imag  # b 텐서의 실수부, 허수부

	# 복소수 곱셈 공식: (r1 + i1*j) * (r2 + i2*j) = (r1*r2 - i1*i2) + (r1*i2 + i1*r2)*j
	real_part = r1 * r2 - i1 * i2
	imag_part = r1 * i2 + i1 * r2

	# 실수부와 허수부를 합쳐 복소수 텐서로 반환
	return torch.complex(real_part, imag_part)

	# r1, i1 = a[..., 0], a[..., 1]
	# r2, i2 = b[..., 0], b[..., 1]
	# return torch.stack([r1 * r2 - i1 * i2, r1 * i2 + i1 * r2], dim = -1)

def conj(a):
	#a[..., 1] = -a[..., 1]
	real_part = a.real
	imag_part = a.imag

	# 허수 부분의 부호를 반대로 바꾸어 켤레 복소수 생성
	conj_a = torch.complex(real_part, -imag_part)
	return torch.conj(a)

def cconv(a, b):
	print(torch.__version__)
	#return torch.fft.irfft(com_mult(torch.fft.rfft(a, 1), torch.fft.rfft(b, 1)), 1, signal_sizes=(a.shape[-1],))
	return torch.fft.irfft(com_mult(torch.fft.rfft(a, 1), torch.fft.rfft(b, 1)), n=a.shape[-1], dim=1)

	#return torch.fft.irfft(com_mult(torch.fft.rfft(a, 1), torch.fft.rfft(b, 1)), n=a.shape[-1])

def ccorr(a, b):
	#return torch.fft.irfft(com_mult(conj(torch.fft.rfft(a, 1)), torch.fft.rfft(b, 1)), 1, signal_sizes=(a.shape[-1],))
	return torch.fft.irfft(com_mult(conj(torch.fft.rfft(a, 1)), torch.fft.rfft(b, 1)), n=a.shape[-1], dim=1)

	#return torch.fft.irfft(com_mult(conj(torch.fft.rfft(a, 1)), torch.fft.rfft(b, 1)),n=a.shape[-1])
