import logging
import operator
import re

_LOG = logging.getLogger(__name__)


class ResourceManager(object):
    def __init__(self):
        self._resources = {}

    @staticmethod
    def _create_resource(type, collection, name, *args, **kwargs):
        if name in collection:
            msg = 'Creation Failed: {0} "{1}" already exists.'.format(type.__name__, name)
            _LOG.error(msg)
            # TODO: Add ResourceAlreadyExists error
            raise RuntimeError()
        else:
            _LOG.debug('Creation Started: New {0}'.format(type.__name__))

        try:
            resource = type(name, *args, **kwargs)
        except ValueError as e:
            msg = 'Creation Failed: {0}'.format(e)
            _LOG.error(msg)
            # TODO: Add ResourceCreationFailed error
            raise
        else:
            collection[name] = resource

        _LOG.debug('Creation Complete: {0} "{1}"'.format(type.__name__, name))
        return resource

    @staticmethod
    def _get_resource(name, collection):
        try:
            result = collection[name]
        except KeyError:
            _LOG.error('Retrieval Failed: "{0}" not found.'.format(name))
            # TODO: Add ResourceNotFound error
            raise
        else:
            _LOG.debug('Retrieval Complete: "{0}"'.format(name))

        return result

    @staticmethod
    def _delete_resource(name, collection):
        try:
            del collection[name]
        except KeyError:
            msg = 'Delete Failed: "{0}" not found.'
            _LOG.debug(msg)
        else:
            msg = 'Delete Complete: "{0}"'.format(name)
            _LOG.debug(msg)

    @staticmethod
    def _find_resources(attr_patterns, collections):
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

            for collection in collections:
                result.extend([resource for resource in collection.itervalues() if pattern.match(op(resource))])

        result.sort(key=operator.attrgetter('name'))

        _LOG.debug('Search Complete: {0:3d} matches'.format(len(result)))
        return result
