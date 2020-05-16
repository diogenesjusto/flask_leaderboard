import pandas as pd 

from sklearn.metrics import f1_score
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error

class Scorer():
    def __init__(self, public_path = './master_key/public_key2.csv', 
                private_path = './master_key/private_key2.csv', metric = mean_squared_error):
        self.public_path = public_path
        self.private_path = private_path
        self.metric = metric

        self.df_public_key = pd.read_csv(self.public_path)
        self.df_private_key = pd.read_csv(self.private_path)
        
    def calculate_score(self, submission_path, submission_type = 'public'):
        df_submission = pd.read_csv(submission_path)

        if submission_type == 'private':
            df_key = self.df_private_key
        else: 
            df_key = self.df_public_key

        # if input length not same, return None
        if len(df_key) != len(df_submission):
            print(len(df_key), len(df_submission))
            return ("NOT SAME LENGTH", None)
        
        df_merged = df_key.merge(df_submission, how ='inner', 
                                left_on='data_id', right_on='data_id', # adjust `on` columns as params
                                suffixes=('_key', '_submission')) 
        # When submission and key have different index value
        if len(df_key) != len(df_merged):
            return ("NOT SAME INDEX", None)

        sub_true = df_merged['SUB-CATEGORIA']
        cat_true = df_merged['CATEGORIA']
        
        # data size is same, time to get score
        sub_key = df_merged['SUB-CATEGORIA_key']
        sub_submission = df_merged['SUB-CATEGORIA_submission']

        cat_key = df_merged['CATEGORIA_key']
        cat_submission = df_merged['CATEGORIA_submission']

        if sub_submission.isna().sum() > 0 or cat_submission.isna().sum() > 0:
            return ("SUBMISSION HAS NULL VALUE", None)

        encoder = preprocessing.LabelEncoder()
        
        sub_key = encoder.fit_transform(sub_key)
        cat_key = encoder.fit_transform(cat_key)
        sub_submission = encoder.fit_transform(sub_submission)
        cat_submission = encoder.fit_transform(cat_submission)
        
        f1_cat = f1_score(cat_key, cat_submission, average='micro')
        f1_sub = f1_score(sub_key, sub_submission, average='micro')
        final_score = (f1_score(cat_true, cat_pred, average='micro')+f1_score(sub_true, sub_pred, average='micro'))/2
        
        score = final_score
        return ("SUBMISSION SUCCESS", score)
