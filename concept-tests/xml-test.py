#!/usr/bin/python
import xml

import ldap.schema

from StringIO import StringIO

class Schema:
    """ The schema generated and to be exported"""
    def __init__(self):
        self.attributes = []
        self.objectclasses = []
        self.representations = {}

class ObjectClass():
    """werty"""
    def __init__(self, oid, abstract=None, auxiliary=None, desc=(None,), may=(),
                 must=(), name=(), obsolete=None, structural=None, sup=()):

        ldap.schema.ObjectClass.__init__(self)
        self.oid = oid
        self._set_attrs(None,
                        {'ABSTRACT': abstract,
                         'AUXILIARY': auxiliary,
                         'DESC': desc,
                         'MAY': may,
                         'MUST': must,
                         'NAME': name,
                         'OBSOLETE': obsolete,
                         'STRUCTURAL': structural,
                         'SUP': sup})
    
class AttributeType(ldap.schema.AttributeType):
    """Ertyui"""
    def __init__(self, oid, names=(), desc=(None,), obsolete=None,
                 sup=(), equality=(None,), ordering=(None,), substr=(None,),
                 syntax=(None,), single_value=None, collective=None,
                 no_user_mod=None, usage=('userApplications',)):

        ldap.schema.AttributeType.__init__(self)
        self.oid = oid
        # May cause problems with some syntaxes
        self._set_attrs(None,
                        {'COLLECTIVE': collective,
                         'DESC': desc,
                         'EQUALITY': equality,
                         'NAME': names,
                         'NO-USER-MODIFICATION': no_user_mod,
                         'OBSOLETE': obsolete,
                         'ORDERING': ordering,
                         'SINGLE-VALUE': single_value,
                         'SUBSTR': substr,
                         'SUP': sup,
                         'SYNTAX': syntax,
                         'USAGE': usage})
        
# test
class Library:
    """ A library, with books in stands """
    def __init__(self, stands=[]):
        self.stands = stands

    def __str__(self):
        string = "+Library:\n"
        for s in self.stands:
            string += str(s)
        return string + '\n'
            
    def add_stand(stand):
        self.stands.append(stand)

class Stand:
    """ A stand with books for a library """
    def __init__(self, books=[]):
        self.books = books

    def __str__(self):
        string = "++Stand:\n"
        for b in self.books:
            string += str(b)
        return string + '\n'
    
class Book:
    """ A book, you can put it in a stand for example... like in libraries"""
    def __init__(self, title="", author="", labels=set()):
        self.title = title
        self.author = author
        self.labels = labels

    def __str__(self):
        return '+++Book: ' + self.title + " by " + self.author + '\n' 

    def set_title(title):
        self.title = title

    def set_author(author):
        self.author = author

    def add_label(label):
        this.labels.add(label)

    def remove_label(label):
        this.labels.remove(label)

    def to_representation(self, representation='json'):
        """Get a representation of this schema
        to_json()->string"""
        out = StringIO()
        #json_out = 
        
    def store(self, representation='json'):
        """Stores a representation of this schema in a persistent way"""
        pass




def main():

    b1 = Book("Chasing dinosaurs", "Philip Ronson", set(["history", "animals"]))
    b2 = Book("a book", "an author", set())
    s1 = Stand([b1,b2])
    s2 = Stand([b1,b2])
    l = Library([s1,s2])

    print l

if __name__ == '__main__':
    main()
