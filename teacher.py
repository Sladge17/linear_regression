import sys
import numpy as np

def check_argv(argv):
	argv_len = len(argv)
	if not argv_len:
		return 'data.csv'
	if argv_len != 1:
		print("\033[31mNeed only one dataset\033[37m")
		exit()
	return argv[0]

def read_data(source):
	try:
		data = np.genfromtxt(source, dtype=np.uint32, delimiter=',')[1:]
	except:
		print("\033[31mDataset not exist\033[37m")
		exit()
	x = np.array(data[:, 0])
	y = np.array(data[:, 1])
	return (x, y)

def normalization(target, val_min, val_max):
	return (target - val_min) / (val_max - val_min)

def norm_x(x):
	x_minmax = np.array([np.min(x), np.max(x)])
	x = normalization(x, *x_minmax)
	return (x_minmax, x)

def set_hyperparameters(y):
	weight = np.array([np.random.rand(), np.max(y) / 2], np.float32)
	epochs = 100
	alpha = np.array([0.1, 0.01], np.float32)
	return (weight, epochs, alpha)

def learning_nn(weight, epochs, x, y, alpha):
	error = np.zeros(epochs, np.float32)
	selection = np.array([0, 1], np.float32)
	delta = np.zeros(2, np.float32)
	for epoch in range(epochs):
		error[epoch] = np.power(np.mean(np.stack((x,
													np.ones(x.size)),
												1) @ weight) - np.mean(y), 2)
		if error[epoch] < 100:
			return error
		for i in range(x.size):
			selection[0] = x[i]
			predict = selection @ weight 
			delta += (predict - y[i]) * selection
		weight -= delta * alpha
		delta[:] = 0
	return error

def create_weightsfile(x_minmax, weight):
	with open("weights", 'w') as file:
		for x in x_minmax:
			file.write(str(x) + '\n')
		for w in weight:
			file.write(str(w) + '\n')

def main(argv):
	source = check_argv(argv)
	x, y = read_data(source)
	x_minmax, x = norm_x(x)
	weight, epochs, alpha = set_hyperparameters(y)
	learning_nn(weight, epochs, x, y, alpha)
	create_weightsfile(x_minmax, weight)

if __name__ == "__main__":
	main(sys.argv[1:])