import face_recognition
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