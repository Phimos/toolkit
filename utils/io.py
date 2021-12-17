import json
import os
import pickle

import yaml


def create_parent_dir(file_path):
    parent_dir = os.path.dirname(file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)


def load_yaml(file_path):
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def load_pickle(file_path):
    with open(file_path, 'rb') as stream:
        try:
            return pickle.load(stream)
        except pickle.UnpicklingError as exc:
            print(exc)


def load_json(file_path):
    with open(file_path, 'r') as stream:
        try:
            return json.load(stream)
        except json.JSONDecodeError as exc:
            print(exc)


def save_yaml(file_path, data):
    create_parent_dir(file_path)
    with open(file_path, 'w') as stream:
        try:
            yaml.dump(data, stream, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)


def save_pickle(file_path, data):
    create_parent_dir(file_path)
    with open(file_path, 'wb') as stream:
        try:
            pickle.dump(data, stream, pickle.HIGHEST_PROTOCOL)
        except pickle.PicklingError as exc:
            print(exc)


def save_json(file_path, data):
    create_parent_dir(file_path)
    with open(file_path, 'w') as stream:
        try:
            json.dump(data, stream, indent=4)
        except json.JSONDecodeError as exc:
            print(exc)
