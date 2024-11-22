import os
import re
import importlib
from random import randint
from datetime import datetime
from track_life_back.settings import FLEX_TABLE_STRUCTURE

def rename_file(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]

    # Remove special characters and replace spaces with underscores
    filename = re.sub(r'[^a-zA-Z0-9 ]', '', filename)  # Keep only alphanumeric and spaces
    filename = filename.replace(' ', '_')  # Replace spaces with underscores

    # Generate a random 7-digit number
    random_number = randint(1000000, 9999999)

    # Get the current date
    current_date = datetime.now().strftime('%Y%m%d')

    # Create the new filename
    new_filename = f"{filename}_{random_number}_{current_date}.{ext}"

    # Optional: Store in a specific subdirectory
    return os.path.join('uploads', new_filename)


def get_instance_from_settings(class_path):
    if(class_path==None):
        return None
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


def validate_fields(table_instance,data_dict):
    """

    Inputs --->

         data_dict = {
         "column1":something,
         "column2":something,
         }

         table_instance=Model.objects.get

     Outputs --->
          {
              "validation_status": true,
              "validation_msg": None,
              "data_bag": {
                            "money": {
                                        "data": {
                                                  "value": 200,
                                                  "parameter": None
                                                },

                                        "type": "integer"
                                     },

                            "info": {
                                        "data": {
                                                  "value": "jo",
                                                  "parameter": None
                                                },

                                        "type": "text"
                                    }
                            }
            }   
    """

    return_state={
        "validation_status":True,
        "validation_msg":None,
        "data_bag":None
    }

    post_data_bag={

    }

    table_structure=table_instance.table_structure
    
    for field in data_dict:

        # data that is sent by the client or browser
        req_field_value=data_dict[field]

        # get the field type and validation parameter from the table
        field_type=table_structure["column"][field]["type"]
        field_parameter=table_structure["column"][field]["parameter"]
        
        # get string defination of validation serializer class from settings.py 
        # and convert it to actual class
        field_serializer_defination=FLEX_TABLE_STRUCTURE["type"][field_type]["serializer"]
        serializer_class=get_instance_from_settings(field_serializer_defination)

        serializer_obj=serializer_class(data={"value":req_field_value,"parameter":field_parameter})
        if(serializer_obj.is_valid()==False):
            return_state["validation_status"]=False
            return_state["validation_msg"]=serializer_obj.errors
            return return_state
        
        post_data_bag[field]={"data":serializer_obj.validated_data,
                              "type":field_type,}



    return_state["data_bag"]=post_data_bag

    return return_state


def prepare_data_createRecord(data_bucket):
    """
    The function is used to prepare the data that will be saved in FlexRecordTable model in data_structure 
    field . It will make any necessary changes in the data like save add something or save a file before store 
    its file_id in data_structure .
    """
    prepared_data={}
    for field in data_bucket:
        field_type=data_bucket[field]["type"]
        field_data=data_bucket[field]["data"]

        field_postsave_defination=FLEX_TABLE_STRUCTURE["type"][field_type]["post_save"]
        postsave_function=get_instance_from_settings(field_postsave_defination)

        if(postsave_function!=None):
            task=postsave_function(field_data)
            prepared_data[field]={"file_id":task["file_id"]}
            
        else:
            field_value=data_bucket[field]["data"]["value"]
            prepared_data[field]=field_value

        
    return prepared_data


def fill_undefined_column(table_instance,data_dict):
    table_structure=table_instance.table_structure
    predined_fields=list(table_structure["column"])
    inputed_fields=list(data_dict)
    undefined_fields=set(predined_fields)-set(inputed_fields)

    for undefined_field in undefined_fields:
        data_dict[undefined_field]=None
    
    return data_dict