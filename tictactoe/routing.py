from django.urls import path
from . import consumers

urlpatterns=[
    path("ws/tictactoe/",consumers.TicTacToeConsumer.as_asgi()),
]