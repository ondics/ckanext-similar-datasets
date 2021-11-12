# encoding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
import json
import os.path
import sys

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.search.common import make_connection
from ckan.common import config
from ckan.lib.plugins import DefaultTranslation


log = logging.getLogger(__name__)


def get_config(key, default=None):
    '''
    Get a configuration value.

    The key is automatically prefixed with ``ckanext.``.
    '''
    return config.get('ckanext.similar_datasets' + key, default)


def get_similar_datasets(id, max_num=5):
    '''
    Get similar datasets for a dataset.

    :param string id: ID of the target dataset. This must be the actual
        ID, passing the name is not supported.

    :param int max_num: Maximum number of datasets to return.

    :return: A list of similar dataset dicts sorted by decreasing score.
    '''
    solr = make_connection()
    query = 'id:"{}"'.format(id)
    fields_to_compare = 'text'
    fields_to_return = 'id validated_data_dict score'
    site_id = config.get('ckan.site_id')
    filter_query = '''
        +site_id:"{}"
        +dataset_type:dataset
        +state:active
        +capacity:public
        '''.format(site_id)
    results = solr.more_like_this(q=query,
                                  mltfl=fields_to_compare,
                                  fl=fields_to_return,
                                  fq=filter_query,
                                  rows=max_num)
    log.debug('Similar datasets for {}:'.format(id))
    print('Similar datasets for {}:'.format(id))
    for doc in results.docs:
        log.debug('  {id} (score {score})'.format(**doc))
        print('  {id} (score {score})'.format(**doc))
    return [json.loads(doc['validated_data_dict']) for doc in results.docs]


class SimilarDatasetsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    #
    # IConfigurer
    #

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    #
    # ITemplateHelpers
    #

    def get_helpers(self):
        return {
            'similar_datasets': get_similar_datasets,
            'similar_datasets_get_config': get_config,
            'similar_datasets_as_bool': toolkit.asbool,
        }

    #
    # ITranslation
    #

    def i18n_directory(self):
       module = sys.modules['ckanext.similar_datasets']
       module_dir = os.path.abspath(os.path.dirname(module.__file__))
       return os.path.join(module_dir, 'i18n')

    def i18n_domain(self):
       return 'ckanext-similar-datasets'
