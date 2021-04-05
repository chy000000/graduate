import os
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
from PIL import Image
import numpy as np
import pandas as pd
from pandas import DataFrame

def find(file):            
    lena = mpimg.imread(file)
    # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
    lum_img = lena[:,:,0]
    #print(lum_img)
    lum_img=np.array(lum_img)
    lum_img[lum_img<150]=0
    lum_img[lum_img>=150]=1
    #print(lum_img.shape[1])
    w=lum_img.shape[1]
    h=lum_img.shape[0]
    #output = DataFrame(lum_img)
    #output.to_csv("test.csv")
    lena.shape #(512, 512, 3)
    lum_img.shape #(512, 512, 3)
    lum_img1=np.transpose(lum_img)
    ###################################################
    #按列找到第一个有黑的位置
    loc=np.array(np.where(lum_img==np.min(lum_img)))
    loc=np.array(loc)
    loc=loc.T[loc.T[:,1].argsort()].T
    for i in range(len(loc[1])):
        if(lum_img[loc[0][i]][loc[1][i]:loc[1][i]+200].sum()<10):
            m=loc[1][i]
            break
    a=lum_img1[m+30]
    i=len(loc[1])-1
    for j in range(len(loc[1])):
        i-=1
        if(lum_img[loc[0][i]][loc[1][i]-200:loc[1][i]].sum()<10):
            z=loc[1][i]
            break
    #print(m)
    #loc,a=work(lum_img1)#按列找到第一个有黑的位置
    ###########################################################
    #识别谱的位置
    a=np.transpose(a)   
    b=np.array(np.where(a==0))
    b=b.tolist()
    b=b[0]
    d=[]
    c=[]
    for i in range(len(b)):
        if(lum_img[b[i]][m+20:m+200].sum()>10):
            c.append(b[i])
    c=list(set(c))
    for i in c:
        b.remove(i)
    b=list(set(b).difference(set(c)))
    b.sort()
    c=[]
    for i in range(len(b)-1):
        if(b[i]==b[i+1]-1):
            c.append(b[i])
        c=list(set(c))
    for i in c:
        b.remove(i)
    b=list(set(b).difference(set(c)))
    b.sort()
    c=[]
    for i in range(len(b)-1):
        if(i!=1 and i!=len(b)-2):
            if(abs((b[i]-b[i-1])-(b[i-1]-b[i-2]))>10 and abs((b[i]-b[i+1])-(b[i+1]-b[i+2]))>10):
                c.append(b[i])
    c=list(set(c))
    for i in c:
        b.remove(i)
    split=[]
    split.append(0)
    if(len(b)>5):
        if(b[1]-b[0]<30):
            i=6
            while(i<=len(b)):
                loc=b[i]
                while(1):
                    if(lum_img[loc][0:w].sum()>=w-5):
                        split.append(loc)
                        break
                    loc=loc-1
                i=i+5
    split.append(h)
    print(split)
    filelist=[]
    for i in range(len(split)-1):
        lena1 = lena[split[i]:split[i+1], 0:w]
        img1 = Image.fromarray(lena1)
        f = file[:-4] + '_' + str(i + 1) + '.jpg'
        filelist.append(f)
        img1.save(f)
    return filelist,split,h,w
    
def image_compose(filename,image_names,h,w):
    IMAGE_ROW=len(image_names)
    to_image = Image.new('RGB', (w, h)) #创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    high = 0
    for y in range(IMAGE_ROW):
        from_image = Image.open(image_names[y])
        img = np.array(from_image)
        img = img[:, :, 0]
        high1 = img.shape[0]
        to_image.paste(from_image, (0, high))
        high += high1
    #to_image=to_image.resize((w, h),Image.ANTIALIAS)
    to_image.show()
    return to_image.save('new\\'+filename[5:-4]+'_new.jpg') # 保存新图


#filename='test\\12.jpg'
#filelist,s,h,w = find(filename)
#image_compose(filename,filelist,h,w)