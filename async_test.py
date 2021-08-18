import time
from tqdm import tqdm

def foo():
	for i in range(100_000):
		print(i)
		yield 
		time.sleep(0.5)



if __name__ == "__main__":
	a = foo()
	print(type(a), next(a), next(a))
	for i in tqdm(range(1000)):
		time.sleep(.01)