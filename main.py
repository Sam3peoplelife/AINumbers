import numpy as np
import random
import mnist_loader
from tkinter import *
import PIL
from PIL import ImageTk, Image, ImageDraw
import cv2

class Network(object):
        def __init__(self, sizes):
            self.num_layers = len(sizes)
            self.sizes = sizes
            self.biases = [np.random.randn(y,1) for y in sizes[1:]]
            self.weights = [np.random.randn(y,x) for x,y in zip(sizes[:-1], sizes[1:])]
        def feedforward(self, a):
            for b,w in zip(self.biases, self.weights):
                a = sigmoid(np.dot(w,a)+b)
            return a
        def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
            if test_data: n_test = len(test_data)
            n = len(training_data)
            for j in range(epochs):
                random.shuffle(training_data)
                mini_batches = [training_data[k:k+mini_batch_size] for k in range(0,n,mini_batch_size)]
                for mini_batch in mini_batches:
                    self.update_mini_batch(mini_batch, eta)
                if test_data:
                    print("Epoch {0} : {1} / {2}".format(j,self.evaluate(test_data), n_test))
                else:
                    print("Epoch {0} complete".format(j))
        def update_mini_batch(self, mini_batch, eta):
            nabla_b = [np.zeros(b.shape) for b in self.biases]
            nabla_w = [np.zeros(w.shape) for w in self.weights]
            for x,y in mini_batch:
                delta_nabla_b, delta_nabla_w = self.backprop(x,y)
                nabla_b = [nb + dnb for nb,dnb in zip(nabla_b, delta_nabla_b)]
                nabla_w = [nw + dnw for nw,dnw in zip(nabla_w, delta_nabla_w)]
            self.weights = [w-(eta/len(mini_batch))*nw for w,nw in zip(self.weights, nabla_w)]
            self.biases = [b-(eta/len(mini_batch))*nb for b,nb in zip(self.biases, nabla_b)]
        def backprop(self, x, y):
            nabla_b = [np.zeros(b.shape) for b in self.biases]
            nabla_w = [np.zeros(w.shape) for w in self.weights]
            activation = x
            activations = [x]
            zs = []
            for b, w in zip(self.biases, self.weights):
                z = np.dot(w, activation)+b
                zs.append(z)
                activation = sigmoid(z)
                activations.append(activation)
            delta = self.cost_derivative(activations[-1], y) * \
                    sigmoid_prime(zs[-1])
            nabla_b[-1] = delta
            nabla_w[-1] = np.dot(delta, activations[-2].transpose())
            for l in range(2, self.num_layers):
                z = zs[-l]
                sp = sigmoid_prime(z)
                delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
                nabla_b[-l] = delta
                nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
            return(nabla_b, nabla_w)

        def evaluate(self, test_data):
            test_results = [(np.argmax(self.feedforward(x)),y) for (x,y) in test_data]
            return sum(int(x == y) for (x,y) in test_results)


        def cost_derivative(self, output_activations, y):
            return(output_activations - y)


def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))


training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
net = Network([784, 50, 50, 50, 10])
net.SGD(training_data, 30, 10, 4.0, test_data=test_data)


width = 28
height = 28
white = (255,255,255)
filename = "image.jpg"
def save():

    img_path = "image.jpg"
    img = cv2.imread(img_path, 0)
    img_reverted = cv2.bitwise_not(img)
    new_img = img_reverted / 255
    new_img_new = [item for sublist in new_img for item in sublist]
    img_net = np.array(new_img_new)
    final = img_net.reshape(784, 1)
    arrayx = np.argmax(net.feedforward(final))
    print(arrayx)


def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1,y1,x2,y2, fill='dimgray', width = 1)
    draw.line([x1,y1,x2,y2], fill='black', width=1)

root = Tk()
cv = Canvas(root, width=width, height=height,bg='white')
cv.pack()
image1=PIL.Image.new("RGB", (width,height), white)
draw = ImageDraw.Draw(image1)
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)
button = Button(text="show", command = save)
button.pack()
root.mainloop()









