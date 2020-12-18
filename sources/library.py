# -*- coding: utf-8 -*-
"""
EmpID    - 214931
Email    - Akshada.Pawar@kpit.com
Location - Pune
Batch    - July, 2020
Date     - 12/12/2020
File Description -  Program to implement Library Management System. This program can do
                    following functions:
                        1) Add a book to the library
                        2) Display all available books
                        3) Borrow a book from library
                        4) Return books to the library
                        5) Display all students with books
"""

import sys
from datetime import datetime, timedelta
from collections import defaultdict  # Used to store collection of data and handle exceptions

""" Without using try-except block we can handled exceptions in Python with the help of
 defaultdict in the collection module."""


class StudentException(Exception): pass


class NoStudent(StudentException): pass


class NoBook(StudentException): pass


# This only contains the title name

class Status_Of_Book:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return self.title

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return self.title == other


# This keep the record of students who have yet to return books

class Checking:
    loan_period = 10
    fine_per_day = 2

    def __init__(self):
        self.due_dates = {}

    def check_in(self, name):
        due_date = datetime.now() + timedelta(days=self.loan_period)
        self.due_dates[name] = due_date

    def check_out(self, name):
        current_date = datetime.now()
        if current_date > self.due_dates[name]:
            delta = current_date - self.due_dates[name]
            overdue_fine = self.fine_per_day * delta.days
            print("Fine Amount: ", overdue_fine)


# Library class contains a set of books

class Library:
    record = Checking()

    def __init__(self):
        self.books = []

    def add_book(self, new_book):  # Adding new book to the library
        self.books.append(new_book)
        return self.books

    def display_books(self):  # Display all available books
        if self.books:
            print("\nThe books we have made available in our library are:\n")
            for book in self.books:
                print(book)
            return(self.books)
        else:
            print("\nSorry, we have no books available in the library at the moment\n")
            return False

    def lend_book(self, requested_book):  # Request for a book
        if requested_book in self.books:
            print(f'''\n You have now borrowed, \"{requested_book}\" book''')
            self.books.remove(requested_book)
            return True

        else:
            print(f'''\n Sorry, \"{requested_book}\" is not there in our library at the moment''')
            return False


# Student class contains container for all students

class Student:
    def __init__(self):
        self.books = defaultdict(list)

    """def get_student(self, name):
        if name not in self.books:
            return "Not Found"

        return self.books[name]"""

    def borrow_book(self, name, book, library):
        if library.lend_book(book):
            self.books[name].append(book)
            return True
        return False

    def return_book(self, name, book, library):
        if book not in self.books[name]:
            raise NoBook(f'''\n\"{name}\" doesn't seem to have borrowed "{book}"''')
            return False
        else:
            library.add_book(book)
            self.books[name].remove(book)
            return True

    def students_with_books(self):  # Display all record in the library
        for name, books in self.books.items():
            if books:
                yield name, books


def borrow_book(library, book_tracking):
    name = input("\nPlease Enter Your Name: ")
    book = Status_Of_Book(input("\nEnter Book Name You Want To Borrow: "))

    if book_tracking.borrow_book(name, book, library):
        library.record.check_in(name)


def return_book(library, book_tracking):
    name = input("\nPlease Enter Your Name: ")
    returned_book = Status_Of_Book(input("\nEnter Book Name You Want To Return: "))

    if book_tracking.return_book(name, returned_book, library):
        library.record.check_out(name)

library = Library()
book_tracking = Student()

if __name__ == '__main__':

    while True:

        # Main Menu

        print("#################### WELCOME STUDENT ####################")
        choice = int(input("#################### LIBRARY MANAGEMENT SYSTEM #################### \n\n \
                           1) Add Book \n \
                           2) Display all Books \n \
                           3) Borrow a Book \n \
                           4) Return a Book \n \
                           5) Lending Record \n \n"))

        if choice == 1:
            library.add_book(Status_Of_Book(input("\nPlease, Enter Book Name You Want to Add in the Library: ")))

        elif choice == 2:
            library.display_books()

        elif choice == 3:
            borrow_book(library, book_tracking)

        elif choice == 4:
            return_book(library, book_tracking)

        elif choice == 5:
            students = tuple(book_tracking.students_with_books())
            if students:
                for name, book in students:
                    print(f"{name}: {book}")
            else:
                print("\nNo students have borrowed books at the moment")

        else:
            print("\nSomething gone wrong! Please check again.")

        user_input = int(
            input("\nWant something more?\n \
                   1) To continue.\n \
                   2) To exit.\n"))

        if user_input == 1:
            continue

        else:
            sys.exit()