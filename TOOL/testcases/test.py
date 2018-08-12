import pandas as pd

from mod_matrix import generateCustomMatrix as gcm

if __name__=='__main__':
    path='../static/uploads/V2_ICU_INPUT_PATIENT_1.csv'
    data=pd.read_csv(path)
    c= gcm.generateCustomMatrix()
    #c.appendToBitList(['KNN(1)'])
    #c.appendToBitList(['KNN(2)'])
    c.appendToBitList(['1>1'])
    #c.appendToBitList(['1+2>1'])
    matrix,bs=c.generateCustomHeidiMatrix(data)
    print(matrix)