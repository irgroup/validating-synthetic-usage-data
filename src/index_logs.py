import util
util.start_database()

from glob import glob
from util import database_collection, parse_log

dbc = database_collection()

for f_name in glob('data/logs/*.json'):
    year_str = f_name.split('/')[-1][:4]
    if int(year_str) >= 2016 and int(year_str) < 2022:
        print(f_name)
        logs = []
        with open(f_name, 'r') as f_in:     
            json_lines = f_in.readlines()
            for line in json_lines:   
                session = parse_log(line)
                if len(session.get('Documents')) >= 20 and len(session.get('Keywords')) > 0:   
                    logs.append(session)
        if len(logs) > 0:                            
            dbc.insert_many(logs)        

dbc.create_index([ ("Keywords", -1)])