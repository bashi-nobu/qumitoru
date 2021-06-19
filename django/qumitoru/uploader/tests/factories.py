from django.contrib.auth import get_user_model
from questionnaire.models import Questionare

from factory import LazyAttribute, Sequence, SubFactory
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

