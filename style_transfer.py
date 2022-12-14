# -*- coding: utf-8 -*-
"""style_transfer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qh3aSM_dVURWkWPvJx0zYDFSD_GPsIn-
"""

import keras.backend as k
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import scipy
import tensorflow as tf

tf.compat.v1.disable_eager_execution()
img=keras.preprocessing.image.load_img("/content/ele.jpg")
x=keras.preprocessing.image.img_to_array(img)
x=x.reshape(1,x.shape[0],x.shape[1],x.shape[2])
batch_size=x.shape
shape=x.shape[1:]
x=keras.applications.vgg16.preprocess_input(x)

vgg=keras.applications.vgg16.VGG16(include_top=False,input_shape=shape)

new_model=keras.models.Sequential()
for layer in vgg.layers:
  if layer.name.endswith("pool"):
    new_model.add(keras.layers.AveragePooling2D())
  else:
    new_model.add(layer)

new_model.summary()

def cut_off_model(count):
  model=keras.models.Sequential()
  output=None
  conv_layer_counter=0
  for layer in new_model.layers:
    if layer.name.endswith("conv1") or layer.name.endswith("conv2")  or layer.name.endswith("conv3"):
      conv_layer_counter+=1
    model.add(layer)    
    if conv_layer_counter==count:
      output=layer
      break
    
  return model,output

c_model,output=cut_off_model(7)


target=k.variable(c_model.predict(x))
loss=k.mean(k.square(target-output.output))

grad=k.gradients(loss,new_model.input)

loss_and_grad=k.function(inputs=[new_model.input],outputs=[loss]+grad)

fake_input=np.random.randn(np.product(batch_size))

def unprocess(img):
  img[...,0]=img[...,0]+103.939
  img[...,1]=img[...,1]+116.779
  img[...,2]=img[...,2]+126.68
  img=img[...,::-1]
  return img

def scale(x):
  x=x-x.min()
  x=x/x.max()
  return x

def wrapper(x_vec):
  l,g=loss_and_grad([x_vec.reshape(*batch_size)])
  return l.astype(np.float64),g.flatten().astype(np.float64)

losses=[]
for _ in range(10):
  
  fake_input,l,_=scipy.optimize.fmin_l_bfgs_b(wrapper,fake_input,maxfun=50)#just an optimizer like adam
  fake_input=np.clip(fake_input,-127,127)
  
  print(l)
  losses.append(l)

x1=fake_input.reshape(*batch_size)

x1=unprocess(x1)
g=scale(x1[0])

plt.imshow(g)

def autocorrelation(x):
  x=k.batch_flatten(k.permute_dimensions(x,(2,0,1)))
  g=k.dot(x,k.transpose(x))/x.get_shape().num_elements()
  return g

# vgg=keras.applications.vgg16.VGG16(include_top=False,input_shape=shape)
content_model=keras.Model(new_model.input,output.output)

img=keras.preprocessing.image.load_img("/content/ele.jpg")
x=keras.preprocessing.image.img_to_array(img)
x=x.reshape(1,x.shape[0],x.shape[1],x.shape[2])
batch_size=x.shape
shape=x.shape[1:]
x=keras.applications.vgg16.preprocess_input(x)
target2=content_model.predict(x)

loss=k.mean(k.square(k.variable(target2)-content_model.output))

img=keras.preprocessing.image.load_img("/content/style.jpg",target_size=(shape[0],shape[1]))
x=keras.preprocessing.image.img_to_array(img)
x=x.reshape(1,x.shape[0],x.shape[1],x.shape[2])
batch_size=x.shape
shape=x.shape[1:]
x=keras.applications.vgg16.preprocess_input(x)

style_output=[layer.get_output_at(1) for layer in new_model.layers if layer.name.endswith("conv1")]

len(style_output)

style_model=keras.Model(new_model.input,style_output)

target_style=[k.variable(y) for y in style_model.predict(x)  ]

weights=[1,2,3,4,5]

for i in range(len(target_style)):
  loss+=weights[i]*k.mean(k.square(autocorrelation(target_style[i][0])-autocorrelation(style_model.output[i][0])))

grad=k.gradients(loss,new_model.input)

loss_and_grad=k.function(inputs=[new_model.input],outputs=[loss]+grad)

def wrapper(x_vec):

  l,g=loss_and_grad([x_vec.reshape(*batch_size)])
  
  return l.astype(np.float64),g.flatten().astype(np.float64)

x=np.random.randn(np.product(batch_size))

for _ in range(10):
  
  x,l,_=scipy.optimize.fmin_l_bfgs_b(wrapper,x,maxfun=10)#just an optimizer like adam
  x=np.clip(x,-127,127)
 
  print(l)
  losses.append(l)

x1=x.reshape(*batch_size)

x1=unprocess(x1)
g=scale(x1[0])
plt.imshow(g)

jj=g*255
jj=jj.astype(np.uint8)
plt.imshow(jj)

from PIL import Image
im = Image.fromarray(jj)
im.save("your_file.jpeg")

