from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from tinydb import TinyDB
import database.tinyDB_utils as tinyDB_utils

tiny = TinyDB('db.json')


def get_table(table_name: str):
	return tinyDB_utils.get_table(tiny, table_name)

def get_one(table_name: str, field_name: str, field_value: str):
	return tinyDB_utils.get_one(tiny, table_name, field_name, field_value)

def insert_entry(table_name: str, entry_data: dict):
	return tinyDB_utils.insert_entry(tiny, table_name, entry_data)

def update_entry(table_name: str, field_name: str, field_value: str, update_data: dict):
	return tinyDB_utils.update_entry(tiny, table_name, field_name, field_value, update_data)

def delete_entry(table_name: str, field_name: str, field_value: str):
	return tinyDB_utils.delete_entry(tiny, table_name, field_name, field_value)