import torchvision.models as models
from torchvision import models, transforms
from torch.autograd import Variable
import torch.nn as nn
import numpy as np
from PIL import Image
import requests
from io import BytesIO

class Classifier:
    def __init__(self, model=models.vgg16(pretrained=True)):
        self.model = model
        # input size 224 x 224
        self.trans = transforms.Compose([
            transforms.Scale(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # from http://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
])
        self.imagenet_classes = eval(requests.get('https://gist.githubusercontent.com/yrevar/942d3a0ac09ec9e5eb3a/' \
            'raw/596b27d23537e5a1b5751d2b0481ef172f58b539/imagenet1000_clsid_to_human.txt').content)
    
    def data_loader(self, X):
        #import pdb; pdb.set_trace()
        # Load image URLs, create Image, put in list with label
        image_url, class_name = X
        #class_name = X[1]
        #image_url = X[0]
        
        #response = requests.get(image_url)
        #im = Image.open(BytesIO(response.content))
        im = Image.open(image_url)
        return im, class_name
        """
        for class_name, image_url
        #for class_name, image_url in X:
        #    response = requests.get(image_url)
        #    im = Image.open(BytesIO(response.content))
        #    yield im, class_name
        """
        
    def evaluate(self, X):
        image, label = self.data_loader(X)
        tens = Variable(self.trans(image))
        tens = tens.view(1, 3, 224, 224)
        preds = nn.LogSoftmax()(self.model(tens)).data.cpu().numpy()
        res = np.argmax(preds)
        print('true (likely) label:', label)
        print('predicted', self.imagenet_classes[res], '\n')
        return self.imagenet_classes[res]
    
    def batch_evaluate(self, X):
        # TODO load several images and infer with batch_size=X
        return

# my_classifier = Classifier(model=models.vgg16(pretrained=True))
# my_classifier.evaluate(['https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=3200&q=80', 'banana'])
# my_classifier.evaluate(['https://images.unsplash.com/flagged/photo-1551120036-96014e3026de?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80', 'pear'])

# images = [('dog', 'https://images.unsplash.com/photo-1534361960057-19889db9621e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=3150&q=80'),
#         ('pomeranian', 'https://c.photoshelter.com/img-get/I0000q_DdkyvP6Xo/s/900/900/Pomeranian-Dog-with-Ball.jpg'),
#         ('car', 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2250&q=80')]