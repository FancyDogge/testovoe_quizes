from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ArrowType
from sqlalchemy import desc

import requests
import os

#переменные среды, заданные в docker-compose
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
database = os.environ['POSTGRES_DB']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False, unique=True)
    answer = db.Column(db.String, nullable=False)
    date_created = db.Column(ArrowType, nullable=False)

    def __init__(self, question: str, answer: str, date_created: ArrowType):
        self.question = question
        self.answer = answer
        self.date_created = date_created
    
    #кастомное св-во для сериализации объектов этого класса
    @property
    def serialized(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'date_created': self.date_created.for_json(),
        }

#создает таблицу Quiz 
db.create_all()


def quiz_API_call_and_quiz_obj_save(questions_num: int):
    #call к API с викторинами
    try:
        quiz_api_response = requests.get(f'https://jservice.io/api/random?count={questions_num}')
    except:
        return {'message': 'quiz API call error'}
    quiz_list = quiz_api_response.json()
    #достаю последний сохраненный вопрос из дб
    question_to_return = Quiz.query.order_by(desc(Quiz.id)).first()

    #чек, вернул ли запрос к API с викторинами хотя бы 1 вопрос
    if len(quiz_list) > 0:
        for index, quiz in enumerate(quiz_list):
            #чек на наличие в дб такого же объекта
            if bool(Quiz.query.filter_by(question=quiz['question']).first()):
                #если такой обхект уже есть, то ф-ция вызывает сама себя, в качестве аргумента - недополученное кол-во вопросов
                return quiz_API_call_and_quiz_obj_save(len(quiz_list) - index)       
            else:
                new_quiz = Quiz(
                question = quiz['question'],
                answer = quiz['answer'],
                date_created = quiz['created_at'],
                )
                #сохраняем объект в дб
                db.session.add(new_quiz)
                db.session.commit()
        #чек, есть ли в дб хотя бы 1 сохраненный ранее вопрос
        if question_to_return:
            return question_to_return.serialized
        else:
            return {}
    return {'message': 'You\'ve requested 0 quizes'}


#Один единственный эндпоинт, который слушает post запросы
@app.route('/get_quiz', methods=['POST'])
def post_test():
    if request.method == 'POST':
        try:
            questions_num = request.get_json(force=True)['questions_num']
        except:
            return {'message': 'questions_num was not provided'}
        
        return quiz_API_call_and_quiz_obj_save(questions_num)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)