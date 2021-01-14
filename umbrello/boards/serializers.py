from boards.models import Board, List, Card,  Log
from django.contrib.auth.models import User, Group
from rest_framework.serializers import ModelSerializer, ValidationError


class BoardSerializer(ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','name',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        user = validated_data['user']
        board = Board(owner_id=user, name=validated_data['name'])

        last_log = Log.objects.filter(board_id = board).order_by('order').last()
        if last_log is None:
            log_order = 1
        else:
            log_order = last_log.order + 1
        log = Log(board_id = board, username = validated_data['user'].username, description = 'created the board',order = log_order)

        board.save()

        group = Group.objects.create(name=str(board.id))
        group.save()
        user.groups.add(group)
        board.members_id = group
        
        board.save()
        log.save()

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

        last_log = Log.objects.filter(board_id = board).order_by('order').last()
        if last_log is None:
            log_order = 1
        else:
            log_order = last_log.order + 1
        log = Log(board_id = board, username = board.owner_id.username, description = 'created the list',order = log_order)
        log.save()

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
        
        new_card = Card(list_id=list_id, name=validated_data['name'], description   = validated_data['description'], term = validated_data['term'], order = order)
        new_card.save()

        last_log = Log.objects.filter(board_id = list_id.board_id).order_by('order').last()
        if last_log is None:
            log_order = 1
        else:
            log_order = last_log.order + 1
        log = Log(board_id = list_id.board_id, username = list_id.board_id.owner_id.username, description = 'created the card',order = log_order)
        log.save()

class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ['id','name','description','order','archived','term', 'members_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = ['username','description','order','term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)