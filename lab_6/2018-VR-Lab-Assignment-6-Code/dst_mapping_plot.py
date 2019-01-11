import pickle
import matplotlib.pyplot as plt

if __name__ == '__main__':
	with open('./dst_mapping.pkl','rb') as file:
		dsts = pickle.load(file=file)

	x = [pair[0] for pair in dsts]
	y = [pair[1] for pair in dsts]
	plt.plot(x, y)
	plt.axes().set_aspect(1.0)
	plt.title('go-go transfer function')
	plt.show()
