from boards.models import Board, List, Card
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ValidationError


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','name',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        board = Board(
            owner_id=validated_data['user'], name=validated_data['name'])
        board.save()

    def validate(self, data):
        user = self.user
        #if not Board.objects.filter(owner_id=user).filter(name=data.get("name")).exists():
        data['user'] = user
        return data

class ListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ['id','name','order','archived']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AddListSerializer(ModelSerializer):
    class Meta:
        model = List
        fields = ['id','name',]

    def __init__(self, *args, **kwargs):
        self.board = kwargs.pop('board')
        self.order = kwargs.pop('order')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        board = self.board
        order = self.order
        
        new_list = List(board_id=board, name=validated_data['name'], order = order)
        new_list.save()

class AddCardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['name','description','term']

    def __init__(self, *args, **kwargs):
        self.list = kwargs.pop('list')
        self.order = kwargs.pop('order')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        list_id = self.list
        order = self.order
        
        new_card = Card(list_id=list_id, name=validated_data['name'], description = validated_data['description'], term = validated_data['term'], order = order)
        new_card.save()

class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['id','name','description','order','archived','term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)