import imageinput_xiaojiexian as im
import matplotlib.image as mpimg # mpimg 用于读取图片
import matplotlib.pyplot as plt # plt 用于显示图片
import numpy as np
#import time
from PIL import Image
import os
 
 
def blend_two_images(image1,image2):
    img1 = Image.open( image1)
    img1 = img1.convert('RGBA')
 
    img2 = Image.open( image2)
    img2 = img2.convert('RGBA')
    
    r, g, b, alpha = img2.split()
    alpha = alpha.point(lambda i: i>0 and 100)
 
    img = Image.composite(img2, img1, alpha)
 
    img.save('1'+'_new.png')
    os.remove(image1)
    os.remove(image2)
    return



file='C:/Users/Administrator/Desktop/13.jpg'

green=[0,255,0]
red=[255,0,0]
def Fault(file,standard,user,a):
    x,c=im.find(file)
    X=x
    x1=[]
    lena = mpimg.imread(file) # 读取和代码处于同一目录下的 lena.png
    lena.flags['WRITEABLE'] = True
    lena1=mpimg.imread(file) # 读取和代码处于同一目录下的 lena.png
    lena1.flags['WRITEABLE'] = True
    for i in range(len(X)):
        if(X[i][0]<X[0][0]+25):
            x1.append(i)
    X=np.array(X)
    X=np.delete(X,x1,axis=0)
    x1=[]
    for i in range(len(x)):
        if(i==len(x)-1):
            x1.append(i)
        elif(x[i+1][0]<x[0][0]+25):
            x1.append(i)
    x=np.array(x)
    x=np.delete(x,x1,axis=0)
    
    for i in range(len(x)):
        if(x[i][0]<=x[0][1]+10):
            x[i][0]+=int((x[0][3]-x[0][1])*(88/85))
            if(i==0):
                x[i][0]+=int((x[0][3]-x[0][1])*(80/85))
    print(len(x))
    width=abs(int((x[0][1]-x[0][3])/16))
    z=11

    '''
    file_object = open(file[:-3]+'txt')
    file_context = file_object.read()
    x=file_context.strip(',').split(',')
    '''
    
    for i in range(len(standard[0])):
        j=standard[0][i]
        end=X[j][0]
        lenth=int((end-x[j][0])/a)
        lena[x[j][1]+(z+standard[3][i])*width+int(-0.5*width) : x[j][1]+(z+standard[3][i])*width+int(0.5*width) , x[j][0]+int(standard[1][i]*lenth) : x[j][0]+int(standard[1][i]*lenth+standard[2][i]*lenth)]=green
    for i in range(len(user[0])):
        j=user[0][i]
        end=X[j][0]
        lenth=int((end-x[j][0])/a)
        lena1[x[j][1]+(z+user[3][i])*width+int(-0.5*width) : x[j][1]+(z+user[3][i])*width+int(0.5*width) , x[j][0]+int(user[1][i]*lenth) : x[j][0]+int(user[1][i]*lenth+user[2][i]*lenth)]=red
    mpimg.imsave(file[:-4]+'_new1'+file[-4:],lena)
    mpimg.imsave(file[:-4]+'_new2'+file[-4:],lena1)
    blend_two_images(file[:-4]+'_new1'+file[-4:],file[:-4]+'_new2'+file[-4:])
    return file[:-4]+'_new.png'



standard=[[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4],
       [0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.5,1],
       [-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8]]

standard=[[0,1,2,3,4],
       [0,1,2,3,4],
       [1,1,1,1,1],
       [-11,-10,-9,-8]]


user=[[0],[0],[2],[-11]]
Fault(file,standard,user,4)


img1='standard.jpg'
img2='user.jpg'
blend_two_images(img1,img2)