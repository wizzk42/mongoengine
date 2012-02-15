#!/usr/bin/env python
# -*- coding: utf8 -*-

__all__ = [ 'DocumentGenericFieldsMixin' ]

import datetime

class DocumentGenericFieldsMixin(object):
    """
        Generic Fields Extension for mongoengine.BaseDocument
        Provide some functionality to manage typed fields 
        mapped as attributes
    """
    
    @classmethod
    def _from_son( cls, son ):
        obj = super(DocumentGenericFieldsMixin, cls)._from_son( son )

        data = dict((str(key), value) for key, value in son.items())

        for generic_field_name, generic_field_value in data.items():
            print generic_field_name, generic_field_value
            if generic_field_name not in cls._fields and generic_field_name != '_id':
                if generic_field_value is not None:
                    generic_field_type = cls._autodetect_field_type_for_value( generic_field_value )
                    if generic_field_type:
                        generic_field = cls._create_generic_field( cls._autodetect_field_type_for_value( generic_field_value ), generic_field_name )
                        cls._fields[generic_field_name] = generic_field
                setattr(obj, generic_field_name, generic_field_value)    
        return obj

    @classmethod
    def _autodetect_field_type_for_value( self, value ):
        """
            Try to determine the proper field type for a data value
        """
        if isinstance( value, dict ):
            from fields import DictField
            return DictField
        elif isinstance( value, list ):
            from fields import ListField
            return ListField
        elif isinstance( value, int ):
            from fields import IntField
            return IntField
        elif isinstance( value, float ):
            from fields import FloatField
            return FloatField
        elif isinstance( value, bool ):
            from fields import BooleanField
            return BooleanField
        elif isinstance( value, datetime.datetime ):
            from fields import DateTimeField
            return DateTimeField
        elif isinstance( value, basestring ):
            from fields import StringField
            return StringField

    @classmethod
    def _create_generic_field( self, field_class, field_name, **kwargs ):
        """ 
            Create a new generic field class
        """
        if isinstance( field_class, type ):
            try:
                return field_class( db_field=field_name, **kwargs )
            except:
                pass
        return None

    def __setattr__( self, attr_name, attr_value ):
        """
            Setup a new field for the current object
        """
        if attr_name is not None:
            if not attr_name.startswith('_') and attr_name not in type(self)._fields:
                field_class = type(self)._autodetect_field_type_for_value( attr_value )
                field = type(self)._create_generic_field( field_class, attr_name )
                self._fields.update({ attr_name: field })
                setattr( self, attr_name, attr_value )
            else:
                object.__setattr__( self, attr_name, attr_value )

