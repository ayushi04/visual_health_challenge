import generate_image as gm
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import validSyntax as vd

#THIS CLASS IS USED TO CREATE CUSTOM HEIDI MATRIX. IT TAKES SORTED DATASET AND STRING OF 
#CONDITIONS TO CREATE CUSTOM HEIDI MATRIX.
class generateCustomMatrix:
    bits=[] #ALL THE CONDITIONS AS STRING IN LIST 
    bitslen=0 #NUMBER OF CONDITIONS IN LIST

    def appendToBitList(self,bitop): #ADDING LIST OF CONDITIONS TO "bits" LIST
        for i in bitop:
            alllist=i.split('\n')
            for j in alllist:
                self.bits.append(j) 
                self.bitslen=self.bitslen+1

    def resetBitList(self): #RESETTING THE BITLIST AND MAKING "bitslen"=0
        self.bits=[]
        self.bitslen=0

    def getBitList(self): #PRINTING THE BITLIST
        return str(self.bits)

    def getKNNmatrix(self,sorted_data,row,col,b1,knn=10): #CREATES KNN MATRIX
        b1=b1[b1.find("(")+1:b1.find(")")]
        b1=b1.split(",")
        for i in range(len(b1)):
            if(b1[i] in list(sorted_data.columns)):
                b1[i]=sorted_data.columns.get_loc(b1[i])
            else:
                b1[i]=int(b1[i])
        subspace=sorted_data.iloc[:,b1]    
        np_subspace=subspace.values
        nbrs=NearestNeighbors(n_neighbors=knn,algorithm='ball_tree').fit(np_subspace)
        temp=nbrs.kneighbors_graph(np_subspace).toarray()
        temp=temp.astype(np.uint64)
        return temp

    #MAIN METHOD FOR CREATING CUSTOME HEIDI MATRIX. IT PARSES ALL THE STRINGS IN "bits" LIST
    #AND CREATES CUSTOM BIT MATRIX   
    global gl
    def generateCustomHeidiMatrix(self,sorted_data,row,col,knn=10):
        global gl
        matrix=np.zeros(shape=(row,row),dtype=np.uint64)
        factor=1
        count=0
        bit_subspace={} #key : bit_number and value is the subspace that bit refers to.
        for b1 in self.bits:
            #OPTION1 : KNN(X)
            if("KNN" in b1):
                print('b1',b1)
                temp=self.getKNNmatrix(sorted_data,row,col,b1,knn)
                matrix=matrix + temp*factor
                factor=factor*2
                bit_subspace[count]=b1
                count=count+1
            elif(vd.validateSyntax(b1)):
                import re
                ml=re.findall('[0-9.]+|.',b1)
                print('lll',len(ml))
                if(len(ml)==3):
                    x=sorted_data.iloc[:,int(ml[0])].values
                    y=sorted_data.iloc[:,int(ml[2])].values
                    temp=[[eval(str(x[i])+ml[1]+str(y[j])) for i in range(len(x))] for j in range(len(y))]
                    temp=np.array(temp,dtype=np.uint8)
                    matrix=matrix + temp*factor
                    factor=factor*2
                    bit_subspace[count]=b1
                    count=count+1
                    gl=temp
                    #print('valid')
                elif(len(ml)==5):
                    x=sorted_data.iloc[:,int(ml[0])].values
                    y=sorted_data.iloc[:,int(ml[2])].values
                    z=sorted_data.iloc[:,int(ml[4])].values
                    if(ml[1] in ['+','-','*','/','%','//','**']):
                        temp=[[eval(str(x[i])+ml[1]+str(y[i])+ml[3]+str(z[j])) for i in range(len(x))] for j in range(len(y))]
                    elif(ml[3] in ['+','-','*','/','%','//','**']):
                        temp=[[eval(str(x[i])+ml[1]+str(y[j])+ml[3]+str(z[j])) for i in range(len(x))] for j in range(len(y))]
                    else:
                        print('invalid bit vector input')
                        return    
                    temp=np.array(temp,dtype=np.uint8)
                    matrix=matrix + temp*factor
                    factor=factor*2
                    bit_subspace[count]=b1
                    count=count+1
                    gl=temp
                    #print('valid')
                else:
                    print('invalid bit vector input')
                    return                
            elif("" == b1):
                factor=factor*2
                count=count+1
            else:
                print('invalid bit vector input')
                return
        return matrix,bit_subspace


if __name__=='__main__':
    fpath='./static/default/blobs_3d_5c_1000/blobs_3d_5c_1000.csv'
    feature_vector,classLabel_numeric,class_label_dict,fv_dict, row, col=gm.readDataset(fpath,"yes")
    feature_vector.loc[:,'classLabel']=classLabel_numeric    
    feature_vector.loc[:,'classLabel_orig']=classLabel_numeric
    c= generateCustomMatrix()
    c.appendToBitList(['KNN(1)'])
    c.appendToBitList(['KNN(2)'])
    c.appendToBitList(['1>1'])
    c.appendToBitList(['1+2>1'])
    print(c.getBitList())
    matrix,bs=c.generateCustomHeidiMatrix(feature_vector,row,col)
    print(matrix)