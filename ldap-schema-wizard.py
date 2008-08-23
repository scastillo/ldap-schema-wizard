"""
ldap-schema-wizzard.py - LDAP for human beings
See http://ldap-schema-wizard.googlecode.com for details

Sebastian Castillo Builes <castillobuiles@gmail.com>
"""

import ldap
import sys, getpass

from lsw_errors import InvalidOIDError, InvalidObjectClassKindError


VERSION = '0.1'

class Schema(object):
    """
    A LDAP Schema.

    Base class to export schemas to other formats
    """

    def __init__(self):
        self.attributes = []
        self.objectclasses = []
        self.representations = {}

    def to_xml(self, pretty=False):
        """
        to_xml(bool) -> str. Returns the Schema XML representation.

        If pretty then returns a more human redable XML with spaces
        """
        import xml.dom.minidom as minidom
        xml_impl = minidom.getDOMImplementation()
        doc = xml_impl.createDocument(None,'Schema', None)
        top = doc.documentElement
        top.setAttribute('ldap_schema_wizzard_version', VERSION)
        for oc in self.objectclasses:
            elem = doc.createElement('ObjectClass')
            elem.setAttribute('oid', oc.oid)
            for name in oc.names:
                _elem = doc.createElement('Name')
                _elem.appendChild(doc.createTextNode(name))
                elem.appendChild(_elem)
            elem.setAttribute('kind',('structural', 'abstract', 'auxiliar')[oc.kind])
            desc_elem = doc.createElement('Description')
            desc_elem.appendChild(doc.createTextNode(oc.desc))
            elem.appendChild(desc_elem)
            for may in oc.may:
                _elem = doc.createElement('May')
                _elem.appendChild(doc.createTextNode(may))
                elem.appendChild(_elem)
            for must in oc.must:
                _elem = doc.createElement('Must')
                _elem.appendChild(doc.createTextNode(must))
                elem.appendChild(_elem)
            for sup in oc.sup:
                _elem = doc.createElement('Sup')
                _elem.appendChild(doc.createTextNode(sup))
                elem.appendChild(_elem)
            elem.setAttribute('obsolete', str(oc.obsolete))
            top.appendChild(elem)
        return top.toprettyxml()


class ObjectClass(ldap.schema.ObjectClass):
    """
    LDAP ObjectClass object - Stores objectclass information

    =Initializer params=
    
    oid         - (str) Numeric OID
    kind        - (str) 'abstract', 'auxiliar' or 'structural'. Default: 'structural'
    desc        - (str) Short ObjectClass description
    may         - (tuple of str) Tuple of attributes that instances of this objectclass MAY implement
    must        - (tuple of str) Tuple of attributes that instances of this objectclass MUST implement
    names       - (tuple of str) Tuple of short names describing the ObjectClass
    is_obsolete - (bool). Specifies if the ObjectClass shoul not be used. Default: False
    sup         - (tuple of str) Tuple of OID's representing superior ObjectClasses
    """
    def __init__(self, oid, names, desc, kind='structural',  may=None,
                 must=None, is_obsolete=False, sup=None):

        ldap.schema.ObjectClass.__init__(self)
        self.set_oid(oid)
        self.set_default_attrs()
        self.set_names(names)
        self.set_kind(kind)
        self.set_desc(desc)
        self.set_may(may)
        self.set_must(must)
        self.set_obsolete(is_obsolete)
        self.set_sup(sup)

    #TODO: Catch all exceptions from _set_attrs
        
    def set_oid(self,oid):
        """
        set_oid(str) -> None

        eg: set_oid('0.9.2342.19200300.100.4.15')
        """
        if not self._is_valid_oid(oid):
            raise InvalidOIDError('OID Must be numeric values with dot separators')
        self.oid = oid
            
    def set_default_attrs(self):
        self._set_attrs(None, ldap.schema.ObjectClass.token_defaults)

    def set_names(self,names):
        """
        set_names(tuple) -> None

        eg: set_names(('friendlyCountry',))
        """
        if names is None:
            self.names = ()
        else:
            self.names = names
            

    def set_kind(self,kind):
        """
        Values acording to ldap.schema:
           structural = 0
           abstract   = 1
           auxiliary  = 2
        """
        if kind is 'structural':
            self.kind = 0
        elif kind is 'abstract':
            self.kind = 1
        elif kind is 'auxiliary':
            self.kind = 2
        else:
            raise InvalidObjectClassKindError(
                'ObjectClass kind must be in (structural, auxiliary, abstract) but was (%s)' % kind)

    def set_desc(self, desc):
        """sdfsfd"""
        self.desc = desc

    def set_may(self, may):
        """qwer"""
        if may is None:
            self.may = ()
        else:
            self.may = may

    def set_must(self, must):
        """qwert"""
        if must is None:
            self.must = ()
        else:
            self.must = must

    def set_obsolete(self, is_obsolete):
        """qwerty"""
        self.obsolete = is_obsolete

    def set_sup(self, sup):
        """qwertyu"""
        if sup is None:
            self.sup = ()
        else:
            self.sup = sup

        
    #
    # === Class Helpers ===
    #

    #TODO: Find the good way to look for uniqueness
    def _is_valid_oid(self,oid):
        """Validates OID syntax and that its unique"""
        # Verify that its only digits and dots
        return oid.replace('.','0').isdigit()



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


def main():

    try:
        schema = Schema()
        schema.objectclasses.append(ObjectClass('1.2.', ('test',) ,'Test Object Class 1', kind='abstrac'))
        schema.objectclasses.append(ObjectClass(oid='1.2.3.1', desc='RFC 0000: Specification for NASA dogs', names=('inetOrgPublicDog', 'dog')))

        schema.objectclasses[0].may=('may1', 'may2', 'may3')
        schema.objectclasses[1].set_obsolete(True)

        xml_file = open('schema_test.xml', 'w')
        xml_file.write(schema.to_xml())
        xml_file.close()

    
        for i in schema.objectclasses:
            print i
    except InvalidOIDError, err:
        print "Error creating schema: %s" % err.message
    except InvalidObjectClassKindError, err:
        print "Error creating ObjecClass: %s" % err.message
        
    sys.exit()
    
    print 'Server name or ip address: ',
    SERVER = str(sys.stdin.readline())
    print 'Port to connect: ',
    PORT = int(sys.stdin.readline())
    URL = 'ldap://localhost'
    DN = getpass.getuser()
    PASSWD = getpass.getpass('Password: ')

    connection = ldap.initialize(URL) 

    try:
        connection.simple_bind_s(DN,PASSWD)
    except ldap.LDAPError, error:
        print error
    finally:
        connection.unbind()

if __name__ == '__main__':
    main()
