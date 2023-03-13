from pymongo import MongoClient
import docker
import json
import re
import random

from pyclick.click_models.task_centric.TaskCentricSearchSession import TaskCentricSearchSession
from pyclick.search_session.SearchResult import SearchResult

json_str = open('./settings.json').read()
settings = json.loads(json_str)

db_client = MongoClient(settings.get('MONGO').get('IP'),
                        settings.get('MONGO').get('PORT'))

def start_database(image_tag=settings.get('MONGO').get('IMAGE_TAG'),
                    container_name=settings.get('MONGO').get('CONTAINER_NAME'),
                    port=settings.get('MONGO').get('PORT')):
    client = docker.from_env(timeout=86400)
    client.containers.run(image_tag,
                            name=container_name,
                            ports={27017: port},
                            detach=True,
                            restart_policy={'Name': 'always'})
    print("MongoDB is running.")
    
def rm_database(container_name=settings.get('MONGO').get('CONTAINER_NAME'),
                rm_img=True,
                image_tag=settings.get('MONGO').get('IMAGE_TAG')):
    client = docker.from_env(timeout=86400)
    container = client.containers.get(container_name)
    container.stop()
    container.remove()
    print('Removed container!')
    if rm_img:
        client.images.remove(image_tag)
        print('Removed image!')

def database_collection(database_name=settings.get('MONGO').get('DB_NAME'),
                        collection_name=settings.get('MONGO').get('COLLECTION_NAME')):
    return db_client[database_name][collection_name]

def drop_database_collection(database_name=settings.get('MONGO').get('DB_NAME'),
                             collection_name=settings.get('MONGO').get('COLLECTION_NAME')):
    db_client[database_name][collection_name].drop()
    print('Dropped', collection_name)
    
def database(database_name=settings.get('MONGO').get('DB_NAME')):
    return db_client[database_name]

def drop_database(database_name=settings.get('MONGO').get('DB_NAME')):
    db_client.drop_database(database_name)
    print('Dropped', database_name)

def parse_log(line):
    session = json.loads(line)   
    date_created = session.get('DateCreated')       
    date = int(re.findall(r'\d+', date_created)[0]) 
    session['DateCreated'] = date
    session.pop('Url')
    session.pop('Title')
    session.pop('DOI')
    session.pop('ClinicalAreas')
    return session

def parse_session(session):
    clicked_docs = [log.get('click') for log in session.get('clicks')]
    task = session.get('_id')
    query = session.get('clicks')[0].get('query')
    results = session.get('clicks')[0].get('documents')
    _session = TaskCentricSearchSession(task, query)
    for result in results:
        _click = 1 if result in clicked_docs else 0
        _result = SearchResult(result, _click)
        _session.web_results.append(_result)
    return _session

def interleave(ranking_base, ranking_exp):
    # team draft interleaving
    # implementation taken from https://bitbucket.org/living-labs/ll-api/src/master/ll/core/interleave.py

    result = {}
    result_set = set([])

    max_length = len(ranking_base)

    pointer_exp = 0
    pointer_base = 0

    length_ranking_exp = len(ranking_exp)
    length_ranking_base = len(ranking_base)

    length_exp = 0
    length_base = 0

    pos = 1

    while pointer_exp < length_ranking_exp and pointer_base < length_ranking_base and len(result) < max_length:
        if length_exp < length_base or (length_exp == length_base and bool(random.getrandbits(1))):
            result.update({pos: {"docid": ranking_exp[pointer_exp], 'type': 'EXP'}})
            result_set.add(ranking_exp[pointer_exp])
            length_exp += 1
            pos += 1
        else:
            result.update({pos: {"docid":  ranking_base[pointer_base], 'type': 'BASE'}})
            result_set.add(ranking_base[pointer_base])
            length_base += 1
            pos += 1
        while pointer_exp < length_ranking_exp and ranking_exp[pointer_exp] in result_set:
            pointer_exp += 1
        while pointer_base < length_ranking_base and ranking_base[pointer_base] in result_set:
            pointer_base += 1
    return result