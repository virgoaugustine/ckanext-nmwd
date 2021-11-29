from pylons import config
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

# use the env function
import ckan.lib.helpers as h

from datetime import datetime

def dataset_groups():
    '''Return a list of the groups in the dataset.'''

    # Get a list of all the site's groups from CKAN, sorted by number of
    # datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={ 'all_fields': True})
    return groups


def topics_count():
    return len(dataset_groups())

def sources_count():
    orgs = toolkit.get_action('organization_list')(data_dict={})
    return len(orgs)

def datasets_count():
    datasets = toolkit.get_action('package_list')(data_dict={})
    return len(datasets)


def popular_datasets(limit=3):
    '''Return the most popular datasets'''
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']
    except:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(
                data_dict={'id': pkg['id']})
            modified = datetime.strptime(
                package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['uploaded'] = modified.strftime('%d %b %Y')
            pkgs.append(package)
        return pkgs

