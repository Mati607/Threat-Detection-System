import pandas as pd
import numpy as np  
import os
import json
import tarfile
import argparse
import re

def extract_json_from_tar_gz(folder_path):
    """
    Extract all .json.tar.gz files under 'folder_path'.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith('.json.tar.gz'):
            try:
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(path=folder_path)
            except Exception as e:
                print(f"Failed to extract {filename}: {str(e)}")
        else:
            pass


def set_username(path):
    global uid, uname

    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    user_id_match = re.search(r'"userId":"([^"]+)"', content)
    username_match = re.search(r'"username":\{"string":"([^"]+)"\}', content)

    user_id = user_id_match.group(1) if user_id_match else None
    username = username_match.group(1) if username_match else None
    
    if user_id is not None:
        uid = user_id
    
    if username is not None:
        uname = username

def json_file_iterator(folder_path):
    """
    Yields each JSON record (line) from all .json or .json.* files 
    under 'folder_path', sorted by filename.
    """
    global cdm

    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.json') or '.json.' in file_name:
            file_path = os.path.join(folder_path, file_name)
            print("Reading File: " + file_path)
            set_username(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if f"{cdm}.FileObject" in line or f"{cdm}.Event" in line or f"{cdm}.Subject" in line or f"{cdm}.NetFlowObject" in line:
                            if not ("FILE_OBJECT_UNIX_SOCKET" in line or "FILE_OBJECT_DIR" in line):
                                try:
                                    record = json.loads(line.strip())
                                    yield record
                                except json.JSONDecodeError as e:
                                    print(f"Error decoding JSON from {file_name}: {e}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except IOError as e:
                print(f"Error opening file {file_path}: {e}")


def prepare_id_files(folder_path):
    """
    Iterates over all JSON lines in 'folder_path' and writes two files:
      1. *_id_to_type.json
      2. *_net2prop.json
    into a subdirectory {folder_path}/{title}_data.
    """
    global title, scene, cdm, output_dir

    id_to_type_file = f'{output_dir}/{scene}_id_to_type.json'
    net2prop_file   = f'{output_dir}/{scene}_net2prop.json'

    os.makedirs(f'{output_dir}', exist_ok=True) 

    net2prop_buffer = []
    id_to_type_buffer = []
    buffer_size = 100000

    def append_to_file(file_path, data):
        with open(file_path, 'a') as file:
            for item in data:
                file.write(json.dumps(item) + '\n')

    def check_and_flush_buffer():
        nonlocal net2prop_buffer, id_to_type_buffer
        if len(net2prop_buffer) >= buffer_size:
            append_to_file(net2prop_file, net2prop_buffer)
            net2prop_buffer = []
        if len(id_to_type_buffer) >= buffer_size:
            append_to_file(id_to_type_file, id_to_type_buffer)
            id_to_type_buffer = []

    for line in json_file_iterator(folder_path):
        str_line = json.dumps(line)
        
        if f"avro.cdm{cdm}.NetFlowObject" in str_line:
            net_flow_object = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.NetFlowObject']
            try:
                nodeid = net_flow_object['uuid']
                srcaddr = net_flow_object['localAddress'].get('string')
                srcport = net_flow_object['localPort'].get('int')
                dstaddr = net_flow_object['remoteAddress'].get('string')
                dstport = net_flow_object['remotePort'].get('int')

                net2prop_data = {nodeid: [srcaddr, srcport, dstaddr, dstport]}
                id_to_type_data = {nodeid: 'NETFLOW'}
                net2prop_buffer.append(net2prop_data)
                id_to_type_buffer.append(id_to_type_data)
            except:
                pass

        if f"schema.avro.cdm{cdm}.Subject" in str_line:
            subject = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Subject']
            uuid = subject['uuid']
            record_type = subject['type'] 
            id_to_type_data = {uuid: record_type}
            id_to_type_buffer.append(id_to_type_data)

        if f"schema.avro.cdm{cdm}.FileObject" in str_line:
            file_object = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.FileObject']
            uuid = file_object['uuid']
            file_type = file_object['type']
            id_to_type_data = {uuid: file_type}
            id_to_type_buffer.append(id_to_type_data)
        
        check_and_flush_buffer()
            
    append_to_file(net2prop_file, net2prop_buffer)
    append_to_file(id_to_type_file, id_to_type_buffer)


def load_dict_from_jsonl(file_path):
    """
    Loads line-delimited JSON from 'file_path' into a single dict (merged).
    """
    result = {}
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            result.update(data)
    return result


def fill_missing_paths_for_subject_process(df):
    actorID_exec_map = dict(
        df.loc[df['exec'] != '', ['actorID', 'exec']]
          .drop_duplicates(subset=['actorID'])  
          .values
    )
    
    mask = (df['object'] == 'SUBJECT_PROCESS') & (df['properties'] == '')
    rows_to_update = df[mask].index

    for idx in rows_to_update:
        object_id = df.at[idx, 'objectID']
        if object_id in actorID_exec_map:
            df.at[idx, 'properties'] = {'objectpath':actorID_exec_map[object_id]}

    return df

def stitch(data_buffer):
    """
    Uses the ID-to-type and net2prop files in {folder_path}/{title}_data 
    to add object type and netflow attributes to 'data_buffer'.
    """
    global title, scene, cdm, output_dir

    id_to_type_file = f'{output_dir}/{scene}_id_to_type.json'
    net2prop_file   = f'{output_dir}/{scene}_net2prop.json'
    
    id_to_type = load_dict_from_jsonl(id_to_type_file)
    net2prop   = load_dict_from_jsonl(net2prop_file)
    info       = data_buffer
    
    for i in range(len(info)):
        try:
            typ = id_to_type[info[i]['objectID']]
            info[i]['object'] = typ
            info[i]['actor_type'] = id_to_type[info[i]['actorID']]
            if typ == 'NETFLOW':
                attr = net2prop[info[i]['objectID']]
                info[i]['properties'] = {
                        'localAddress': attr[0],
                        'localPort': str(attr[1]),
                        'remoteAddress': attr[2],
                        'remotePort': str(attr[3])
                    }
        except:
            info[i]['object'] = None
            info[i]['actor_type'] = None
            
    df = pd.DataFrame.from_records(info)
    df = df.dropna()

    os.remove(id_to_type_file)
    os.remove(net2prop_file)

    output_file = os.path.join(output_dir, f"{title}_{scene}.json")
    df = fill_missing_paths_for_subject_process(df)
    df.to_json(output_file, orient='records', lines=True)  


def query_json(folder_path):
    global title, scene, cdm, uid, uname

    info_buffer = []

    for line in json_file_iterator(folder_path):
        try:
            action = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['type']
        except:
            action = ''
        try:
            hostid = line['hostId']
        except:
            hostid = ''
        try:
            actor = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['subject'][f'com.bbn.tc.schema.avro.cdm{cdm}.UUID']
        except:
            actor = ''
        try:
            obj = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['predicateObject'][f'com.bbn.tc.schema.avro.cdm{cdm}.UUID']
        except:
            obj = ''
        try:
            cmd = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['properties']['map']['exec']
        except:
            cmd = ''
        try:
            path = {'objectpath': line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['predicateObjectPath']['string']}
        except:
            path = ''
        try:
            timestampnano = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['timestampNanos']
        except:
            timestampnano = ''
        try:
            timestamp = line['@timestamp']
        except:
            timestamp = ''
        try:
            cmdline = line['datum'][f'com.bbn.tc.schema.avro.cdm{cdm}.Event']['properties']['map']['cmdLine']
        except:
            cmdline = ''

        info_data = {
            'actorID': actor,
            'objectID': obj,
            'action': action,
            'timestampNanos': timestampnano,
            'timestamp': timestamp,
            'exec': cmd,
            'properties': path,
            'cmdline': cmdline,
            'hostid': hostid,
            'username':uname,
            'userid':uid
        }
        info_buffer.append(info_data)
    
    if info_buffer:
        stitch(info_buffer)


def count_missing_semantics():
    global title, scene, output_dir
    
    input_file = os.path.join(output_dir, f"{title}_{scene}.json")
    df = pd.read_json(input_file, orient='records', lines=True)
    
    output_content = ""
    
    for actor_type, group in df.groupby('actor_type'):
        count_with_empty_exec = group[group['exec'] == ''].shape[0]
        total = group.shape[0]
        percent_missing_exec = (count_with_empty_exec / total * 100) if total > 0 else 0
        output_content += (f"Actor Type: {actor_type}\n"
                           f"Count of actorIDs with missing exec: {count_with_empty_exec}\n"
                           f"Percentage with missing exec: {percent_missing_exec:.2f}%\n\n")
    
    for object_type, group in df.groupby('object'):
        count_with_empty_path = group[group['properties'] == ''].shape[0]
        total = group.shape[0]
        percent_missing_path = (count_with_empty_path / total * 100) if total > 0 else 0
        output_content += (f"Object Type: {object_type}\n"
                           f"Count of objectIDs with missing properties: {count_with_empty_path}\n"
                           f"Percentage with missing properties: {percent_missing_path:.2f}%\n\n")
    
    outfile = os.path.join(output_dir, f"{title}_{scene}_meta.txt")
    
    with open(outfile, "w") as file:
        file.write(output_content)

def main():
    parser = argparse.ArgumentParser(description="Process JSON.tar.gz CDM files and generate JSON output.")
    parser.add_argument('--directory', required=True, help="Directory containing the .json.tar.gz files.")
    parser.add_argument('--title', required=True, help="Title name (e.g., E3 or E5).")
    parser.add_argument('--scene', required=True, help="Scene name (e.g., theia, cadets, etc.).")
    parser.add_argument('--output_dir', required=True, help="Directory where the final JSON results will be stored.")

    args = parser.parse_args()

    global title, scene, cdm, output_dir, uid, uname
    directory = args.directory
    title = args.title
    scene = args.scene
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    cdm = "18" if title == 'E3' else "20"

    extract_json_from_tar_gz(directory)
    prepare_id_files(directory)
    query_json(directory)
    count_missing_semantics()


if __name__ == '__main__':
    main()
