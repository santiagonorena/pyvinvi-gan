import torch
from torch.autograd import Variable
import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms
import torchvision.datasets as dset

class Vgg19(torch.nn.Module):
    def __init__(self, requires_grad=False):
        super(Vgg19, self).__init__()
        vgg_pretrained_features = models.vgg19(pretrained=True).features
        self.slice1 = torch.nn.Sequential()
        self.slice2 = torch.nn.Sequential()
        self.slice3 = torch.nn.Sequential()
        self.slice4 = torch.nn.Sequential()
        self.slice5 = torch.nn.Sequential()
        for x in range(2):
            self.slice1.add_module(str(x), vgg_pretrained_features[x])
        for x in range(2, 7):
            self.slice2.add_module(str(x), vgg_pretrained_features[x])
        for x in range(7, 12):
            self.slice3.add_module(str(x), vgg_pretrained_features[x])
        for x in range(12, 21):
            self.slice4.add_module(str(x), vgg_pretrained_features[x])
        for x in range(21, 30):
            self.slice5.add_module(str(x), vgg_pretrained_features[x])
        if not requires_grad:
            for param in self.parameters():
                param.requires_grad = False

    def forward(self, X):
        
        h_relu1 = self.slice1(X)
        h_relu2 = self.slice2(h_relu1)        
        h_relu3 = self.slice3(h_relu2)        
        h_relu4 = self.slice4(h_relu3)        
        h_relu5 = self.slice5(h_relu4)                
        out = [h_relu1, h_relu2, h_relu3, h_relu4, h_relu5]
        return out
    
    
    
class VGGLoss(nn.Module):
    def __init__(self, gpu_ids=0):
        super(VGGLoss, self).__init__()        
        self.vgg = Vgg19()
        self.criterion = nn.L1Loss()
        self.weights = [1.0/32, 1.0/16, 1.0/8, 1.0/4, 1.0]        

    def forward(self, x, y):              
        x_vgg, y_vgg = self.vgg(x), self.vgg(y)

        loss = 0
        for i in range(len(x_vgg)):
            loss += self.weights[i] * self.criterion(x_vgg[i], y_vgg[i].detach())        
        return loss




#------------------Example------------------------------------
# if __name__ == '__main__':
#     dataset = dset.MNIST(root='C:/Users/motur/LRGAN/datasets/mnist', download=False,
#                                transform=transforms.Compose([
#                                    transforms.Resize(128),
#                                    transforms.ToTensor(),
#                                ]))
#     dataloader = torch.utils.data.DataLoader(dataset, batch_size=4,
#                                              shuffle=True)
#     data_iter = iter(dataloader)
    
#     criterionVGG = VGGLoss()
#     criterionVGG = criterionVGG.cuda()
    
#     for i in range(20):
#         images, labels = data_iter.next()
#         img1 = Variable(images[0].expand(1,3,128,128).cuda())
#         img2 = Variable(images[1].expand(1,3,128,128).cuda())
#         y1 = labels[0]
#         y2 = labels[1]
#         loss_G_VGG = criterionVGG(img1, img2)
        
#         print(str(y1) + ' , ' + str(y2))
#         print(loss_G_VGG.data)
#         break
  