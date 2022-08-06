# apply-custom-style-to-images
our model can apply any style to any image there is, it uses a pre-trained model(vgg16) layers but unlike any deeplearning model in our model we are training the input to be like the original photo.<br/>
that being said as weights it's hard to get the optimal value, so the input will have most important feature because we are using pre-trained model with blur on other trivial details.<br/>
we gonna do kinda the same things for the style by getting all the expected output of all the cnn's and as you know as we dive deeper will get more feature by doing that the input will try to be like the original photo with trivial details included.<br/>
finally we merge them together to get our image with our custom style as important details will still there but it will have style like style we want.
# how to run it
there is two ways to use it:<br/>
1-colab<br/>
2-locally<br/>
if you're using colab just upload the ipynb file and run it<br/>
locally:<br/>
1-you have to install python 3<br/>
2-the recommended libraries<br/>
3-install ide and open the .py file or .ipynb<br/>
4-run it

# the recommended libraries:
1-tensorflow<br/>
2-keras<br/>
3-numpy<br/>
4-scipy<br/>
5-matplotlib

# reference:
https://paperswithcode.com/paper/a-neural-algorithm-of-artistic-style
