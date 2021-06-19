from django.contrib.auth import get_user_model
from questionnaire.models import Category, Questionare, QuestionareQuestion, Question
from factory import LazyAttribute, Sequence, SubFactory, Iterator
from factory.django import DjangoModelFactory

UserModel = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    username = Sequence(lambda n: f'user{n}')
    email = LazyAttribute(lambda o: f'{o.username}@example.com')
    password = 'testpassword'
    is_active = True

class QuestionareFactory(DjangoModelFactory):
    class Meta:
        model = Questionare

    name = Sequence(lambda n: f'questionnare_{n}')
    is_active = True
    user = SubFactory(UserFactory)

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    contents = Sequence(lambda n: f'category_{n}')
    user = SubFactory(UserFactory)

class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    contents = Sequence(lambda n: f'question_{n}')
    scale_patarn = 5
    category = SubFactory(CategoryFactory)

class QuestionareQuestionFactory(DjangoModelFactory):
    class Meta:
        model = QuestionareQuestion

    questionare = SubFactory(QuestionareFactory)
    question = SubFactory(QuestionFactory)

class MakeQuestionDataFactory():
    def makeData(self):
        q = QuestionareFactory()
        categories = CategoryFactory.create_batch(7, user=q.user)
        questions = QuestionFactory.create_batch(7, category=Iterator(categories))
        QuestionareQuestionFactory.create_batch(7, questionare=q, question=Iterator(questions))
        return q
