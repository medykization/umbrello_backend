from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import generics
from boards.serializers import BoardSerializer, ListSerializer, AddListSerializer, AddCardSerializer, CardSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from boards.models import Board, List, Card
from django.db.models import Max
from django.contrib.auth.models import User
import json


class BoardView(generics.RetrieveAPIView):
    # checks if user is authenticated to view the model objects
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, user):
        return Board.objects.filter(owner_id=user)  # return all model objects

    def get(self, request, *args, **kwargs):  # GET request handler for the model
        user = request.user
        queryset = self.get_queryset(user)
        serializer = BoardSerializer(queryset, user=user, many=True)
        return Response(serializer.data)


class BoardAdd(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args):
        user = request.user
        body = request.data
        input = {"name": body['name']}
        serializer = BoardSerializer(data=input, user=user)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardNameUpdate(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = request.user
        body = request.data
        id = body['id']
        name = body['name']
        if name == "":
            return Response("You enter blank name")
        try:
            board = Board.objects.get(owner_id = user, id = id)
            if board.name == name:
                return Response("You enter the same name")
            board.name = name
            board.save()
            return Response("Board name updated")
        except Board.DoesNotExist:
            return Response("Board doesn't exist")
        

class ListView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, id):
        board = Board.objects.get(id = id)
        return List.objects.filter(board_id=board)  # return all model objects

    def post(self, request, *args, **kwargs):  # GET request handler for the model
        body = request.data
        id = body['id']
        queryset = self.get_queryset(id)
        serializer = ListSerializer(queryset, many=True)
        return Response(serializer.data)

class ListNameUpdate(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        name = body['name']
        if name == "":
            return Response("You enter blank name")
        try:
            li = List.objects.get(id = id)
            if li.name == name:
                return Response("You enter the same name")
            li.name = name
            li.save()
            return Response("List name updated")
        except Board.DoesNotExist:
            return Response("List doesn't exist")

class ListAdd(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, user, board_id):
        board = Board.objects.get(owner_id = user, id = board_id)
        last_list = List.objects.filter(board_id = board).order_by('order').last()
        if last_list is None:
            return board, 1
        return board, last_list.order + 1

    def post(self, request, *args):
        user = request.user
        body = request.data
        input = {"name": body['name']}
        try:
            board, order = self.get_queryset(user,body['id'])
        except Board.DoesNotExist:
            return Response("Board doesn't exist")
        serializer = AddListSerializer(data=input, board=board, order = order)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response("List added",status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListArchive(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        try:
            li = List.objects.get(id = id)
            cards = Card.objects.filter(list_id = li)
            for card in cards:
                card.archived = not card.archived
                card.save()
            li.archived = not li.archived
            li.save()
            if li.archived == True:
                return Response("Card archived")
            else:
                return Response("Card unarchived")
        except List.DoesNotExist:
            return Response("List doesn't exist")

class ListDelete(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        try:
            List.objects.get(id = id, archived = True).delete()
            return Response("List deleted")
        except List.DoesNotExist:
            return Response("List doesn't exist")

class ListChangeOrder(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        nr = body['nr']
        try:
            li = List.objects.get(id = id)
            if nr == li.order:
                return Response("You enter the same value")

            last_nr = List.objects.filter(board_id = li.board_id).order_by('order').last()

            if nr > last_nr or nr < 1:
                return Response("The entered number is incorrect")

            #lists = List.object.filter(order__gte=)
            return Response("List name updated")
        except Board.DoesNotExist:
            return Response("List doesn't exist")

class CardView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, id):
        li = List.objects.get(id = id)
        return Card.objects.filter(list_id=li)  # return all model objects

    def post(self, request, *args, **kwargs):  # GET request handler for the model
        body = request.data
        id = body['id']
        queryset = self.get_queryset(id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

class CardAdd(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, user, list_id):
        li = List.objects.get(id = list_id)
        last_card = Card.objects.filter(list_id = li).order_by('order').last()
        if last_card is None:
            return li, 1
        return li, last_card.order + 1

    def post(self, request, *args):
        user = request.user
        body = request.data
        input = {"name": body['name'], "description": body['description'], "term": body['term']}
        try:
            li, order = self.get_queryset(user,body['id'])
            if li.archived == True:
                return Response("List is archived")
        except List.DoesNotExist:
            return Response("List doesn't exist")
        serializer = AddCardSerializer(data=input, list=li, order = order)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response("Card added",status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardValuesUpdate(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        name = body['name']
        description = body['description']
        term = body['term']
        if name == "" and description == "" and term == "":
            return Response("You enter blank values")
        try:
            card = Card.objects.get(id = id)
            if name != "" and card.name != name:
                card.name = name
            if name != "" and card.description != description:
                card.description = description
            if term != "":
                card.term = term
            card.save()
            return Response("Card values updated")
        except Board.DoesNotExist:
            return Response("Card doesn't exist")

class CardArchive(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        try:
            card = Card.objects.get(id = id)
            card.archived = not card.archived
            card.save()
            if card.archived == True:
                return Response("Card archived")
            else:
                return Response("Card unarchived")
        except Card.DoesNotExist:
            return Response("Card doesn't exist")

class CardDelete(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        body = request.data
        id = body['id']
        try:
            Card.objects.get(id = id, archived = True).delete()
            return Response("Card deleted")
        except List.DoesNotExist:
            return Response("Card doesn't exist")