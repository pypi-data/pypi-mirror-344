# -*- coding: utf-8 -*-
import requests
from hashlib import sha256
from json import dumps
import heimdall
from heimdall.decorators import get_database, create_database


CREATOR_ID_PID = 'dc:identifier'


@get_database('zotero:api')
def getDatabase(url, **options):
    r"""Generates a dummy database.

    The generated datbase contains a single item, and this item contains and a single metadata.
    The generated metadata property identifier is ``message``, and its value is passed as a parameter (default: ``EXAMPLE``).

    :param url: (:py:class:`str`) Library URL
    :param \**options: Keyword arguments
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`
    """  # nopep8: E501
    headers = {'accept': 'application/json', }
    payload = {'page': 1, 'limit': 25, }
    response = _request(url, headers, payload)
    tree = heimdall.util.tree.create_empty_tree()
    for o in response:
        data = o['data']
        eid = data['itemType']
        item = heimdall.createItem(tree, eid=eid)

        repeatable = dict()
        for key, value in data.items():
            if key in CUSTOM.keys():
                continue
            aid = _get_aid(item, key)
            if type(value) is list:
                for v in value:
                    heimdall.createMetadata(item, str(value), aid=aid, pid=key)
            else:  # type(value) is str
                assert type(value) in (str, int)
                heimdall.createMetadata(item, str(value), aid=aid, pid=key)

        # custom Zotero logic here : specific ways to add metadata,
        # creation of relational items, and so on
        for key, (action, default) in CUSTOM.items():
            action(tree, item, key, data.get(key, default))

    heimdall.util.update_entities(tree)
    return tree


def _request(url, headers, payload):
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    # NOTE: maybe check for response.headers, too?
    return response.json()


def _create_tags(tree, item, key, data):
    assert type(data) is list
    aid = _get_aid(item, key)
    for value in data:
        heimdall.createMetadata(item, value['tag'], aid=aid, pid=key)


def _create_relations(tree, item, key, data):
    assert type(data) is dict
    aid = _get_aid(item, key)
    for pid, value in data.items():
        if type(value) is list:
            for v in value:
                heimdall.createMetadata(item, v, aid=aid, pid=pid)
        else:
            heimdall.createMetadata(item, value, aid=aid, pid=pid)


def _create_creators(tree, item, key, data):
    for creator in data:
        uid = _create_uid(creator)
        eid = creator.pop('creatorType', 'creator')

        def by_author(e):
            values = heimdall.getValues(e, pid=CREATOR_ID_PID)
            return e.get('eid') == eid and uid in values

        target = heimdall.getItem(tree, by_author)
        if target is None:
            creator[CREATOR_ID_PID] = uid
            target = heimdall.createItem(tree, eid=eid)
            for k, v in creator.items():
                taid = _get_aid(target, k)
                heimdall.createMetadata(target, v, aid=taid, pid=k)
        heimdall.createMetadata(item, uid, aid=_get_aid(item, eid), pid=key)


def _get_aid(item, key):
    eid = item.get('eid')
    return f'{eid}.{key}'


def _create_uid(data):
    dump = dumps(data, sort_keys=True)
    return sha256(dump.encode('utf-8')).hexdigest()


CUSTOM = {
    'creators': (_create_creators, []),
    'relations': (_create_relations, {}),
    'tags': (_create_tags, []),
    }


__version__ = '0.5.1'
__all__ = ['getDatabase', '__version__']
