import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

from src.speech_recognition_module.ExtractFeature import ExtractFeature
import pickle
from sklearn.mixture import GaussianMixture

class Spk_r:

    model_path_dir = "data/all_speaker_models"
    def register_speaker(self,audio_path, user_id):
        
        feature_extractor = ExtractFeature()
        try:
            stacked_feature = feature_extractor.extract_features(audio_path) #first training audio's feature
            
            speaker_models_dir="data/all_speaker_models"
            model_name = str(user_id)+".gmm"

            speaker_model_path = os.path.join(speaker_models_dir,model_name)#directory in which model is to saved
                
            # name of model represent's whose voice model
            gmm = GaussianMixture(n_components=16, covariance_type='diag', max_iter=500, n_init=3, verbose=1)
            gmm.fit(stacked_feature) #generating the GMM model of the stacked features

            os.makedirs(os.path.dirname(speaker_model_path), exist_ok=True)
            pickle.dump(gmm, open(speaker_model_path, 'wb'))
        
        except Exception as e:
            
            print("######################### Exception ####################")
            print(f"something went wrong while getting agent response: {e}.")
            print("###########################################")
            return -1
        return speaker_model_path

    def recognize_speaker(self,audio_path):
        '''
        @:param audio_path : Path to the audio which needs to be predicted
        @:return: Returns the user_id of the speaker
    '''
        #if there is no speaker models directory
        #raise error
        if os.path.isdir(Spk_r.model_path_dir) == False:
            #add error code according to your use
            return -1, -100
        
        # to extract necessary features from the audio 
        feature_extractor = ExtractFeature()
        
        
        # extract existing users (speakers) models from speaker_models directory / database
        # list of gmm_files available

        gmm_files = [os.path.join(Spk_r.model_path_dir, fname) for fname in
                os.listdir(Spk_r.model_path_dir) if fname.endswith('.gmm')]


        
        # user ids of all the users in the database
        # user_ids = [int(fname.split("/")[-1].split(".gmm")[0]) for fname in gmm_files]
        user_names = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]

        #list of existing models
        existing_speaker_models   = [pickle.load(open(gmm_file,'rb')) for gmm_file in gmm_files] # rb stands for  reading the binary file
        
        #if this triggers, it means that there are no user models in the database
        if len(existing_speaker_models) == 0:
            return -1, -100


        # speaker recognition part

        # features of the file to be predicted
        feature = feature_extractor.extract_features(audio_path)

        score_of_individual_comparision = np.zeros(len(existing_speaker_models))
        for i in range(len(existing_speaker_models)):
            gmm = existing_speaker_models[i]  # checking with each model one by one
            scores = np.array(gmm.score(feature))
            score_of_individual_comparision[i] = scores.sum()

        winner = np.argmax(score_of_individual_comparision)

        #detected
        # detected_user_id = user_ids[winner]
        detected_user_name = user_names[winner]

        
        # return detected_user_id, score_of_individual_comparision.max()
        return detected_user_name, score_of_individual_comparision.max()

        # print(gmm_files)
        # print(user_ids)
        # return 0