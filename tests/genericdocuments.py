import unittest

from mongoengine import *
from mongoengine.connection import _get_db

class FirstGenericDocumentTest(unittest.TestCase):

    def setUp(self):
        connect(db='mongoenginetest')
        self.db = _get_db()

        class Person(DocumentGenericFieldsMixin, Document):
            name = StringField()
            age = IntField()
        self.Person = Person

    def test_create_generic_document( self ):
        test_person = self.Person(name='Test')
        test_person.ssn = '1234567890'
        self.assertTrue(test_person._fields.has_key('ssn'))
        self.assertTrue(hasattr(test_person, 'ssn'))
        self.assertEqual(test_person.ssn, '1234567890')
        test_person.save()
        test_person.reload()
        self.assertTrue(test_person._fields.has_key('ssn'))
        self.assertTrue(hasattr(test_person, 'ssn'))
    
    def test_save_generic_document( self ):
        test_person = self.Person(name = 'TestSave' )
        test_person.save()
        
        collection = self.db[self.Person._meta['collection']]
        person_obj = collection.find_one({'name': 'TestSave'})
        self.assertTrue(person_obj is not None)
        self.assertEqual(test_person.id, person_obj['_id'])
        self.assertEqual(test_person.name, person_obj['name'])
        self.assertEqual(test_person.age, person_obj['age'])
        
        

if __name__ == '__main__':
    unittest.main()
