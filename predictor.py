import sys
import os

def read_weights():
	x_minmax = [0] * 2
	weight = [0] * 2
	while True:
		try:
			with open("weights") as file:
				for i, string in enumerate(file):
					if i < 2:
						x_minmax[i] = int(string)
						continue
					weight[i - 2] = float(string)
			return (x_minmax, weight)
		except:
			try:
				os.system("python teacher.py")
			except:
				print("\033[31mNot exist file teacher.py\033[37m")
				exit()

def normalization(target, val_min, val_max):
	return (target - val_min) / (val_max - val_min)

def prediction(target, x_minmax, weight):
	target = normalization(target, *x_minmax)
	prediction = int(round(target * weight[0] + weight[1], 0))
	return prediction

def check_argv(argv):
	if not len(argv):
		return 0
	for i in range(len(argv)):
		try:
			argv[i] = int(argv[i])
		except:
			print("\033[31mIncorrect input\033[37m")
			exit()
		if argv[i] < 0:
			print("\033[31mIncorrect input\033[37m")
			exit()
	return 1

def run_multiprediction():
	x_minmax, weight = read_weights()
	while True:
		argv = input("Target mileage (km)(q -> quit): ")
		if argv == 'q':
			exit()
		try:
			argv = int(argv)
		except:
			print("\033[31mIncorrect input, try again\033[37m")
			continue
		if argv < 0:
			print("\033[31mIncorrect input, try again\033[37m")
			continue
		predict = max(prediction(int(argv), x_minmax, weight), 0)
		print(f"\033[32mMileage {argv}km, cost {predict}\033[37m")

def run_singleprediction(argv):
	x_minmax, weight = read_weights()
	for i in argv:
		predict = max(prediction(i, x_minmax, weight), 0)
		print(f"\033[32mMileage {i}km, cost {predict}\033[37m")

def main(argv):
	if not check_argv(argv):
		run_multiprediction()
	run_singleprediction(argv)

if __name__ == "__main__":
	main(sys.argv[1:])