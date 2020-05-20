import pandas as pd 

from sklearn.metrics import f1_score
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error

class Scorer():
    def __init__(self, public_path = './s3/master_key/public_key.csv', 
                private_path = './s3/master_key/private_key.csv', metric = mean_squared_error):
        self.public_path = public_path
        self.private_path = private_path
        self.metric = metric

        col_names = ["DESCRIÇÃO-PARCEIRO","SUB-CATEGORIA","CATEGORIA"]
        self.df_public_key = pd.read_csv(self.public_path, names=col_names)
        self.df_private_key = pd.read_csv(self.private_path)
        
    def calculate_score(self, submission_path, submission_type = 'public'):
        col_names = ["data_id","DESCRIÇÃO-PARCEIRO","SUB-CATEGORIA","CATEGORIA"]
        df_submission = pd.read_csv(submission_path, names=col_names)

        if submission_type == 'private':
            df_key = self.df_private_key
        else: 
            df_key = self.df_public_key

        # if input length not same, return None
        if len(df_key) != len(df_submission):
            print(len(df_key), len(df_submission))
            return ("NOT SAME LENGTH", None)
        
        #df_merged = df_key.merge(df_submission, how ='inner', 
        #                        left_on='data_id', right_on='data_id', # adjust `on` columns as params
        #                        suffixes=('_key', '_submission')) 
        # When submission and key have different index value
        #if len(df_key) != len(df_merged):
        #    return ("NOT SAME INDEX", None)
  
        # data size is same, time to get score
        #sub_key = df_merged['SUB-CATEGORIA_key']
        #sub_submission = df_merged['SUB-CATEGORIA_submission']
        #cat_key = df_merged['CATEGORIA_key']
        #cat_submission = df_merged['CATEGORIA_submission']

        sub_key = df_key['SUB-CATEGORIA']
        sub_submission = df_submission['SUB-CATEGORIA']
        cat_key = df_key['CATEGORIA']
        cat_submission = df_submission['CATEGORIA']

        #if sub_submission.isna().sum() > 0 or cat_submission.isna().sum() > 0:
        #    return ("SUBMISSION HAS NULL VALUE", None)

        encoder = preprocessing.LabelEncoder()
        
        sub_key = encoder.fit_transform(sub_key.astype(str))
        cat_key = encoder.fit_transform(cat_key.astype(str))
        sub_submission = encoder.fit_transform(sub_submission.astype(str))
        cat_submission = encoder.fit_transform(cat_submission.astype(str))
        
        f1_cat = f1_score(cat_key, cat_submission, average='micro')
        f1_sub = f1_score(sub_key, sub_submission, average='micro')
        final_score = ((f1_cat*0.5)+(f1_sub*0.5))/(f1_cat+f1_sub)
        
        score = final_score
        return ("SUBMISSION SUCCESS", score)
