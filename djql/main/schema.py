import graphene
from .models import *
from graphene_django import DjangoObjectType,DjangoListField

class BookListType(DjangoObjectType):
    class Meta:
        model = BookList
        field="__all__"


class Query(graphene.ObjectType):
    books = graphene.List(BookListType, id=graphene.Int())

    def resolve_books(self, info, id=None):
        if id:
            return BookList.objects.filter(id=id)
        return BookList.objects.all()



class AddNewBook(graphene.Mutation):
    singleBook = graphene.Field(BookListType)

    class Arguments:
        title = graphene.String(required=True)

    def mutate(self, info, title):
        book = BookList(title=title)
        book.save()
        return AddNewBook(singleBook=book)


class UpdateNewBook(graphene.Mutation):
    singleBook = graphene.Field(BookListType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)

    def mutate(self, info, id, title):
        book = BookList.objects.get(id=id)
        book.title = title
        book.save()
        return UpdateNewBook(singleBook=book)

class DeleteSingleBook(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        book = BookList.objects.get(id=id)
        book.delete()
        return DeleteSingleBook(message=f"Book Id:{id} is deleted successfully" )


class Mutation(graphene.ObjectType):
    add_new_book = AddNewBook.Field()
    update_new_book = UpdateNewBook.Field()
    delete_single_book = DeleteSingleBook.Field()