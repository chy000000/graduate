import os
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np
import pandas as pd
from pandas import DataFrame
#######################################################################
#五线谱
def find1(lum_img,lum_img1,b):
    b=np.array(b)
    #print(b)
    #####################################################
    #查找小节线位置
    i=0
    x=[[],[],[]]
    y=[]
    while i<len(b):
        #zero=np.zeros(b[i+4]-b[i]).tolist()
        for j in range(lum_img1.shape[0]):
            #print(lum_img1[j][b[i]:b[i+4]].sum())
            if(lum_img1[j][b[i]:b[i+4]].sum()==0):
                if(lum_img1[j][b[i]:b[i+4]+3].sum()!=0):
                    if(lum_img1[j][b[i]-4:b[i+4]].sum()!=0):
                        if(lum_img[b[i+4]-2][j-6:j].sum()!=0):
                            if(lum_img[b[i]-2][j:j+6].sum()!=0):
                                if(lum_img[b[i+4]+2][j-6:j].sum()!=0):
                                    if(lum_img[b[i]+2][j:j+6].sum()!=0):
                                        x[0].append(j)
                                        x[1].append(b[i])
                                        x[2].append(b[i+4])
            if(lum_img[b[i]][j]==0 and lum_img[b[i]][j-1]!=0):
                #k=len(x[0])-1
                #print(k)
                '''
                if(k>0):
                    if(x[0][k]<lum_img1.shape[0]-40):
                        x[0].append(lum_img1.shape[0]-5)
                        x[1].append(x[1][k-1])
                        x[2].append(x[2][k-1])
                '''
                x[0].append(j)
                x[1].append(b[i])
                x[2].append(b[i+4])
        i+=5
    #k=len(x[0])-1
    #print(k)
    '''
    if(k>0):
        if(lum_img1[lum_img1.shape[0]-5][x[1][k-1]]==0):
            if(x[0][k]<lum_img1.shape[0]-40):
                x[0].append(lum_img1.shape[0]-5)
                x[1].append(x[1][k-1])
                x[2].append(x[2][k-1])
    '''
    #print(x)
    for i in range(len(x[0])):
        if(i>1):
            if(abs(x[0][i]-x[0][i-1])<6):
                y.append(i)
                if(i>4):
                    if(abs(x[0][i]-x[0][i-4])<6):
                        if(abs(x[0][i]-x[0][i-3])<6):
                            if(abs(x[0][i]-x[0][i-2])<6):
                                    y.append(i-4)
    #y.append(len(x[0])-1)
    #print(y)
    l2 = list(set(y))
    l2.sort(key=y.index)
    #print(l2)
    
    x=np.array(x)
    x=np.delete(x,l2,axis=1)
    #print(x)
    f=[]
    t=[]
    for i in range(len(x[0])):
        t=[x[0][i],x[1][i],x[0][i],x[2][i]]
        f.append(t)
    #print(len(f))
    #print(f)
    #print(len(f))
    return f
#######################################################################
#节奏谱
def find2(lum_img,lum_img1,b):
    b=np.array(b)
    #####################################################
    #查找小节线位置
    x=[[],[],[]]
    y=[]
    for j in range(len(b)):
        for i in range(lum_img.shape[1]):
            if(lum_img1[i][b[j]-40:b[j]+40].sum()<4):
                if(lum_img1[i][b[j]-50:b[j]+50].sum()>9):
                    x[0].append(i)
                    x[1].append(b[j]-40)
                    x[2].append(b[j]+40)
            if(lum_img[b[j]][i]==0 and lum_img[b[j]][i-1]!=0):
                x[0].append(i)
                x[1].append(b[j]-40)
                x[2].append(b[j]+40)
    for i in range(len(x[0])):
        if(i!=len(x[0])-1):
            if(x[0][i]==x[0][i+1]-1):
                y.append(i)
        if(i>4):
            if(x[0][i]==x[0][i-5]+5):
                y.append(i)
    #y.append(len(x[0])-1)
    x=np.array(x)
    x=np.delete(x,y,axis=1)
    #print(x)
    f=[]
    t=[]
    for i in range(len(x[0])):
        t=[x[0][i],x[1][i],x[0][i],x[2][i]]
        f.append(t)
    #print(f)
    return f

##################################################################
#f=open("dir.txt","a")  
def find(file):            
    lena = mpimg.imread(file) # 读取和代码处于同一目录下的 lena.png
    # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
    lum_img = lena[:,:,0]
    #print(lum_img)
    lum_img=np.array(lum_img)
    lum_img[lum_img<100]=0
    lum_img[lum_img>=100]=1
    #print(lum_img.shape[0])
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
    ########################################################
    #判断节奏谱还是五线谱
    if(len(b)>4):
        if(b[1]-b[0]<30):
            x=find1(lum_img,lum_img1,b)
        else:
            x=find2(lum_img,lum_img1,b)
    else:
        x=find2(lum_img,lum_img1,b)
    c=[]
    for i in range(len(x)-1):
        if(abs(x[i+1][0]-x[i][0])<40):
            if(x[i+1][1]==x[i][1]):
                c.append(x[i+1])
    for i in c:
        x.remove(i)
    f=open(file[:-3]+'txt','w') 
    f.write(str(x)); 
    f.close()
    return x,z
    # f.writelines(os.path.join(root,file)+"\n")

#find('C:/Users/Administrator/Desktop/3.jpg')
'''
if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        imgpath = sys.argv[i]
find(imgpath)
print("success");
'''