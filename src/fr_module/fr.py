from src.models import UserImage, User
import face_recognition
import numpy as np
import cv2 
import json
import os

class FR:
    face_encoding_filename = "data/face_data/fr_face_encodings.json"

    def resize_image(self,path):
        img = cv2.imread(path)
        (h,w) = img.shape[:2]
        width = 500
        ratio = width / float(w)
        height = int(ratio * h)
        
        return cv2.resize(img, (width,height))
        
    def register_face(self, image_file_path, user_id, name):
        # image file to encodings generations
        # face entry
        # image = cv2.imread(image_file_path)
        # print(image_file_path)
        image = self.resize_image(path=image_file_path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        face_bounderies = face_recognition.face_locations(image)
        
        if len(face_bounderies)!=1:
            return -99
        
        try:
            face_encoding = face_recognition.face_encodings(image,face_bounderies)[0]

        except IndexError:
            face_encoding = []
            return -1

        #creating empty json file that will hold all the face encodings
        ## if the json file does not exist then create a new file
        if os.path.exists(FR.face_encoding_filename)==False:

            json_object=json.dumps({"face_encodings": []}, indent = 4)
            with open (FR.face_encoding_filename,"w") as f:
                f.write(json_object)

        #registering a new user (with face encoding, user_id and name) 
        # to existing json file
        with open(FR.face_encoding_filename,"r+") as file:
            file_data = json.load(file)
            new_data = {}
            new_data["id"] = user_id
            new_data["name"]=name
            new_data ["encoding"] = face_encoding.tolist()

            file_data["face_encodings"].append(new_data)
            file.seek(0)

            json.dump(file_data,file, indent=4)

        return face_encoding.tolist()

    def recognize_face(self, image_file_path):
        image = self.resize_image(path=image_file_path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        face_bounderies = face_recognition.face_locations(image)
        
        if len(face_bounderies)!=1:
            return -99
        
        try:
            current_encoding = face_recognition.face_encodings(image,face_bounderies)[0]

        except IndexError:
            current_encoding = []
            return -1
        
        # checking the current user's encoding with the existing encodings from json file
        ## adding all the existing users encoding list to this list
        """
        existing_encodings_list = []
        #
        if os.path.exists(FR.face_encoding_filename)==False:
            return "fr_face_encodings.json file missing"
        else: 
            with open(FR.face_encoding_filename,"r") as file:
                file_data=json.load(file)
                for face in file_data["face_encodings"]:
                    existing_encodings_list.append(face["encoding"])
        """
        all_encodings = UserImage.query.with_entities(UserImage.userImg_encoded_value).all()
        ## a list of rows will come
        ## each rows are string
        ## so we have to unpack them to list
        existing_encodings_list = [json.loads(all_encodings[i][0]) for i in range(len(all_encodings))]

        # matches = face_recognition.compare_faces(existing_encodings_list, current_encoding) 

        # calculating distances from current users encoding values to the existing users encoding values
        # minimum means similar face
        distances= face_recognition.face_distance(existing_encodings_list, current_encoding)
        """
        if min(distances)<0.5:
            match_idx= np.argmin(distances) ## array index
            # print(matches, match_idx)
            person_id = file_data["face_encodings"][match_idx]["id"]
            person_name = file_data["face_encodings"][match_idx]["name"]
            print(f"person name: {person_name}")
            print(f"person id: {person_id}")
            return person_id
        else:
            #you can add your error code according to your usage
            return "Unknown User"
        """
        if min(distances)<0.5:
            match_idx= np.argmin(distances) ## array index
            person = UserImage.query.filter_by(userImg_endoed_value=all_encodings[match_idx][0]).first()
            if person != None:
                person_uid = person.uid
                person_name = User.query.filter_by(uid=person_uid).first().userName
                print("person_name: {}".format(person_name))
                return person_uid
            return "Unknown operation"
        else:
            return "Unknown User"