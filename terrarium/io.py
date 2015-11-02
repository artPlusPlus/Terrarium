import logging

from .app import App
from .environment import Environment
from .runtime_profile import RuntimeProfile


_logger = logging.getLogger(__name__)

_fmt_base_missing_field = 'Failed to load {0} data: No "{{0}}" field found.'.format
_fmt_base_null_data = 'Failed to load {0} data: No "{{0}}" field found.'.format
_fmt_base_empty_data = 'Failed to load {0} data: No "{{0}}" field found.'.format


def load_json_app(app_data):
    _logger.debug('START Loading App from JSON')

    fmt_missing_field = _fmt_base_missing_field('App').format
    fmt_null_data = _fmt_base_null_data('App').format
    fmt_empty_data = _fmt_base_empty_data('App').format

    get_data_field = lambda field_name: _get_data_field(app_data, field_name,
                                                        fmt_missing_field=fmt_missing_field,
                                                        fmt_null_data=fmt_null_data,
                                                        fmt_empty_data=fmt_empty_data)

    app_name = get_data_field('name')
    app_location = get_data_field('location')
    app_executable = get_data_field('executable')
    app_description = get_data_field('description')




def _get_data_field(data, field_name, fmt_missing_field=None, fmt_null_data=None, fmt_empty_data=None):
    result = None

    try:
        result = data[field_name]
    except KeyError:
        msg = fmt_missing_field(field_name)
        _logger.exception(msg)
        return result

    if result is None:
        msg = fmt_null_data(field_name)
        _logger.exception(msg)
        return result

    result = unicode(result).strip()
    if not result:
        msg = fmt_empty_data(field_name)
        _logger.exception(msg)
        return None

    return result
