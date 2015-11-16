import logging
import operator
import re

from .._errors import *


_LOG = logging.getLogger(__name__)


class ResourceManager(object):
    """
    Base class for ResourceManagers.

    ResourceManagers provide CRUD-L services for a specific type of asset.

    Inheritance was chosen over composition for Managers to facilitate tailored argumentation
    for a
    """
    _resource_type = None
    _resource_collection = {}
    _resource_update_handlers = {}

    @classmethod
    def _create_resource(cls, name, *args, **kwargs):
        resource_type_name = cls._resource_type.__name__

        if name in cls._resource_collection:
            msg = 'Creation Failed: {0} "{1}" already exists.'.format(resource_type_name, name)
            _LOG.error(msg)
            raise ResourceAlreadyExistsError(msg)
        else:
            _LOG.debug('Creation Started: New {0}'.format(resource_type_name))

        try:
            resource = cls._resource_type(name, *args, **kwargs)
        except ValueError as e:
            msg = 'Creation Failed: {0}'.format(e)
            _LOG.error(msg)
            raise ResourceCreationError(msg)
        else:
            cls._resource_collection[name] = resource

        _LOG.debug('Creation Complete: {0} "{1}"'.format(resource_type_name, name))
        return resource

    @classmethod
    def _get_resource(cls, resource_name):
        resource_type_name = cls._resource_type.__name__

        try:
            result = cls._resource_collection[resource_name]
        except KeyError:
            msg = 'Retrieval Failed: {0} "{1}" not found.'.format(resource_type_name, resource_name)
            _LOG.error(msg)
            raise ResourceNotFoundError(msg)
        else:
            _LOG.debug('Retrieval Complete: {0} "{1}"'.format(resource_type_name, resource_name))

        return result

    @classmethod
    def _update_resource(cls, resource_name, **update_values):
        resource_type_name = cls._resource_type.__name__

        try:
            resource = cls._resource_collection[resource_name]
        except KeyError:
            msg = 'Update Failed: {0} "{1}" not found.'.format(resource_type_name, resource_name)
            _LOG.error(msg)
            raise ResourceNotFoundError(msg)

        _LOG.debug('Update Started: {0} "{1}"'.format(resource_type_name, resource_name))

        orig_values = {}
        try:
            for property_name, new_value in update_values.iteritems():
                try:
                    orig_value = getattr(resource, property_name)
                    orig_values[property_name] = orig_value
                except AttributeError:
                    msg = 'Update Failed: {0} "{1}.{2}" not found.'.format(resource_type_name, resource_name,
                                                                           property_name)
                    _LOG.error(msg)
                    raise ResourceAttributeNotFoundError(msg)

                setattr(resource, property_name, new_value)

                msg = 'Updated {0} "{0}.{1}": "{2}"'.format(resource_type_name, resource_name, property_name, new_value)
                _LOG.debug(msg)
        except Exception as e:
            for property_name, orig_value in orig_values.iteritems():
                setattr(resource, property_name, orig_value)
                msg = 'Reverted {0} "{0}.{1}": "{2}"'.format(resource_type_name, resource_name, property_name,
                                                             orig_value)
                _LOG.debug(msg)

            if isinstance(e, ResourceAttributeNotFoundError):
                raise

            msg = 'Update Failed: {0} "{1}" - {2}'.format(resource_type_name, resource_name, e)
            _LOG.error(msg)
            raise ResourceUpdateError(msg)

        if resource.name != resource_name:
            del cls._resource_collection[resource_name]
            cls._resource_collection[resource.name] = resource

        _LOG.debug('Update Complete: {0} "{1}"'.format(resource_type_name, resource_name))

    @classmethod
    def _delete_resource(cls, resource_name):
        resource_type_name = cls._resource_type.__name__

        try:
            del cls._resource_collection[resource_name]
        except KeyError:
            msg = 'Delete Failed: {0} "{1}" not found.'.format(resource_type_name, resource_name)
            _LOG.debug(msg)
        else:
            msg = 'Delete Complete: {0} "{1}"'.format(resource_type_name, resource_name)
            _LOG.debug(msg)

    @classmethod
    def _find_resources(cls, attr_patterns):
        # TODO: Memoize
        _LOG.debug('Search Started')

        result = []

        for attribute, pattern in attr_patterns:
            op = operator.attrgetter(attribute)

            if pattern:
                _pattern = unicode(pattern).strip()
            else:
                _LOG.debug('Skipping Attribute "{0}": No Pattern "{1}"'.format(attribute, pattern))
                continue

            if _pattern:
                pattern = re.compile(_pattern)
            else:
                _LOG.debug('Skipping Attribute "{0}": Empty Pattern'.format(attribute))
                continue

            result.extend([r for r in cls._resource_collection.itervalues() if pattern.match(op(r))])

        result.sort(key=operator.attrgetter('name'))

        _LOG.debug('Search Complete: {0:3d} matches'.format(len(result)))
        return result
