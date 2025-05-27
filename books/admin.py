from django.contrib import admin
from books.models import Book, Author, BookAuthor, BookReview


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'id')
    search_fields = ('title', 'isbn')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'id')
    search_fields = ('first_name', 'last_name', 'email')


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', 'id')
    search_fields = ('book', 'author')


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'comment','stars_given', 'id')
    search_fields = ('user', 'book', 'comment')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)

