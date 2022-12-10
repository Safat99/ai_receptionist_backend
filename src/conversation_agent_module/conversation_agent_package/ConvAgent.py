import os
import json

# import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ConvAgent:
    conversation_database_dir="src/conversation_agent_module/conversation_database"
    qa_file_name= "UIU_qa_store.json"

    def __init__(self,transformer_model_name) -> None:
        self.model = SentenceTransformer(transformer_model_name)

    def conversation(self, question):
        """
        replies according to the question

        :question: user's question in string format
        
        :return: returns a dictionary having the question and 
                corresponding asnwers in the key-value pair setting
        """

        # creating dictionary: data -- for saving related information
        # related to the conversation between user v/s agent
        data={}
        data["success"] = False
        data["unknown"] = False
        data["question"]=""
        data["answer"]=""
        data["message"] = ""

        #creating question-answer json file path
        qa_data_path = os.path.join(ConvAgent.conversation_database_dir,
                                    ConvAgent.qa_file_name)

        #generating encoding of user's current question
        current_question_encoding = [self.model.encode(question)]

        
        try:
            # ----------extracting the encodings of all the questions ------
            database_question_encodings =[]
            # if the question-answer json file does not exist
            # then it returns the empty data dictionary or you can send any error
            # codes if you want
            if os.path.exists(qa_data_path) == False:
                data["message"] = "no data path found"
                return data
            else:
                with open(qa_data_path,"r") as file:
                    file_data = json.load(file)
                    for qa in file_data["qa_encodings"]:
                        database_question_encodings.append(qa["encoding"])
            #----------extraction done-------------------
            

            #------checking similarity between : user qustion vs database question------
            # an
            score= cosine_similarity(current_question_encoding,database_question_encodings)
            score =score[0]
            
            print("question similarity: ",max(score))
            if max(score)>0.5:
                print(f"similarity score: {max(score)}")
                match_idx= np.argmax(score)
                answer = file_data["qa_encodings"][match_idx]["answer"]
                question = file_data["qa_encodings"][match_idx]["question"]
                data["answer"] = answer
                data["question"] = question
                data["message"] = "threshold score passed, known_question"
            else:
                data["unknown"]=True
                data["message"] = "threshold value failed, irrelavant question"

            data["success"]=True

        except Exception as e:
            print(f"Something went wrong while getting agent response: {e}")
            #returns the empty data variable
            #which contains all the status of conversational agent
            data["message"] = "exception occured"
            return data   
        

        
        return data

        

