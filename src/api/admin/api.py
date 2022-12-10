import csv
from io import StringIO
from flask import request, make_response 
from flask_restx import Resource, Namespace, fields
from src.models import User, UserFeedback, UserUnknownQuestions
from src.api.admin.crud import (
    verify_user
)

admin_namespace = Namespace('admin')

new_user = admin_namespace.model(
    "Admin opertaion on new user",
    {
        "uid": fields.String(),
    },
)

user_model = admin_namespace.model(
    "Show all new users",
    {
        "uid": fields.String(),
        "userName": fields.String(),
        "role": fields.String(),
        "isVerified": fields.Boolean(),
        "userImg": fields.String(),
        "userImg_mimetype": fields.String(),
        "userAudioLocation": fields.String(),
        "registeredDate": fields.DateTime(),
    },
)

user_questions = admin_namespace.model(
    "show all unknown questions",
    {
        "uid" : fields.String(),
        "unknown_question": fields.String(),
        "question_time": fields.DateTime(),
    }
)

feedback_users = admin_namespace.model(
    "show all feedbacks of users",
    {
        "uid" : fields.String(),
        "rating": fields.Integer,
        "comment": fields.String(),
        "feedback_time": fields.DateTime(),
    }
)

class New_Users(Resource):
    @admin_namespace.marshal_with(user_model, as_list=True)
    @admin_namespace.doc(params={'Authorization': {"type": "Bearer", "in": "header"}})
    def get(self):
        """new user list"""
        all_new_users = User.query.filter_by(isVerified=False).all()
        return all_new_users, 200
    
    @admin_namespace.expect(new_user)
    def put(self):
        """Verify user"""
        resp = {}
        payload = request.get_json()
        uid = payload.get("uid")
        user = User.query.filter_by(uid=uid).first()
        if not user:
            resp["message"]= "User doesn't exist"
            return resp, 400
        verify_user(uid, verify=True)   
        resp['uid'] = uid
        resp['message'] = 'User verified successfully!' 
        return resp, 201

class FeedbackUsers(Resource):
    @admin_namespace.marshal_with(feedback_users,as_list=True)
    def get(self):
        """All feedbacks and comments"""
        return UserFeedback.query.all(), 200

class UnknownUserQuestions(Resource):
    @admin_namespace.marshal_with(user_questions,as_list=True)
    def get(self):
        """show all questions"""
        return UserUnknownQuestions.query.all(), 200

class FeedbackUser(Resource):
    @admin_namespace.marshal_with(feedback_users,as_list=True)
    def get(self,uid):
        """All feedbacks and comments of single user"""
        return UserFeedback.query.filter_by(uid=uid).all(), 200

class UnknownUserQuestion(Resource):
    @admin_namespace.marshal_with(user_questions,as_list=True)
    def get(self,uid):
        """show all questions"""
        return UserUnknownQuestions.query.filter_by(uid=uid).all(), 200


class ExportQuestions(Resource):
    def get(self):
        """click for download the Question table in csv"""
        questions = UserUnknownQuestions.query.order_by(UserUnknownQuestions.question_time).all()
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['ID', 'UID', 'QUESTIONS', 'DATE'])
        cw.writerows([(i.id, i.uid, i.unknown_question, i.question_time) for i in questions])
        # print([(i.id, i.uid, i.unknown_question, i.question_time) for i in questions])
        # print(si.getvalue())
        response = make_response(si.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=questions.csv'
        response.headers['Content-type'] = 'text/csv'
        return response


admin_namespace.add_resource(New_Users, "/new_users")
admin_namespace.add_resource(FeedbackUsers,"/users_feedback")
admin_namespace.add_resource(FeedbackUser,"/users_feedback/<uid>")
admin_namespace.add_resource(UnknownUserQuestions,"/unknown_questions")
admin_namespace.add_resource(UnknownUserQuestion,"/unknown_questions/<uid>")
admin_namespace.add_resource(ExportQuestions,"/export_unknown_questions")