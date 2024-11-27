import os
import re
import importlib
from random import randint
from datetime import datetime
from track_life_back.settings import FLEX_TABLE_STRUCTURE
import re

def is_valid_name(name: str) -> bool:
    """
    Validates a name based on specific rules.
    Rules:
    - Only alphabetic characters, spaces, hyphens (-), and apostrophes (') are allowed.
    - No consecutive special characters (e.g., --, '', etc.).
    - Cannot start or end with a special character or space.
    - Must contain at least one alphabetic character.
    
    :param name: str, the name to validate.
    :return: bool, True if the name is valid, False otherwise.
    """
    # Check if the name has invalid characters
    if not re.match(r"^[a-zA-Z][a-zA-Z\s'-]*[a-zA-Z]$", name):
        return False
    
    # Check for consecutive special characters or spaces
    if re.search(r"[ \-']{2,}", name):
        return False

    return True

def validate_column_structure(dict):
    """
    Input --->
         dict={ "column_name":"Coding",
                "type":"text",
                "parameter":{}
            }

    Output ---->
           return True or False
    """
    fields=list(dict)
    required_fields=["column_name","type","parameter"]

    for rf in required_fields:
        if(rf not in fields):
            return False
        
    column_name=dict["column_name"]
    type_=dict["type"]
    parameter=dict["parameter"]

    available_field_types=list(FLEX_TABLE_STRUCTURE["type"])

    if(is_valid_name(column_name)==False):
        return False
    
    if(type_ not in available_field_types):
        return False
    
    defined_required_paramter=FLEX_TABLE_STRUCTURE["type"][type_]["required_parameter"]

    if(defined_required_paramter!=None):
        # I will make the implementation later
        # Input variable is parameter
        pass

    return True


    """
    Converts a variable name written in snake_case into a human-readable textual representation.
    
    :param variable_name: The snake_case string to convert.
    :return: A string with words capitalized and separated by spaces.
    """
    # Split the variable name by underscores
    words = variable_name.split('_')
    # Capitalize each word and join with spaces
    return ' '.join(word.capitalize() for word in words)

def to_snake_case(textual_representation: str) -> str:
    """
    Converts a human-readable textual representation into snake_case.
    
    :param textual_representation: The textual representation to convert.
    :return: A snake_case string.
    """
    # Split the textual representation by spaces
    words = textual_representation.split()
    # Lowercase each word and join with underscores
    return '_'.join(word.lower() for word in words)

def create_column_structure(dict):
    """
    Input --->
            dict={ 
                    "column_name":"Coding",
                    "type":"text",
                    "parameter":{}
                }

    Output -->
              { 
                'field': 'coding', 
                'structure': {
                               'type': 'text', 
                               'represent': 'Coding', 
                               'parameter': {}
                            }
                }
    """
    final_structure={
        "field":None,
        "structure":None
    }

    column_name=dict["column_name"]
    type_=dict["type"]
    parameter=dict["parameter"]

    final_structure["field"]=to_snake_case(column_name)
    final_structure["structure"]={ "type":type_ ,
                                   "represent":column_name , 
                                   "parameter":parameter
                                }
    
    print(final_structure)

    return final_structure

def create_table_structure(list_):

    """
    Input -->
              list_ = [ 
                        { 
                           'column_name': 'Coding', 
                           'type': 'text', 
                           'parameter': {}
                         }
                     ]

    Output -->     
                { 
                  'column': {
                              'coding': {
                                          'type': 'text', 
                                          'represent': 
                                          'Coding', 'parameter': {}
                                        }
                            },
                }
     
    """

    final_structure={
        "column":{

        }
    }

    for column_blueprint in list_:
        column_structure=create_column_structure(column_blueprint)
        field_name=column_structure["field"]
        field_structure=column_structure["structure"]
        final_structure["column"][field_name]=field_structure

    return final_structure

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

         table_instance=FlexTable.objects.get

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
    It runs the function for a field that is defined in 
      settings.py --> FLEX_TABLE_STRUCTURE --> "type" --> "{the field}" --> "pre_save"

    Input : 
         data_bucket={  
              'money': {  
                           'data': {
                                      'value': 9000, 
                                      'parameter': None
                                    }, 
                            'type': 'integer'
                        },

              'info': {
                           'data': { 
                                     'value': 'mother', 
                                     'parameter': None
                                    }, 
                            'type': 'text'
                        }
        }

    Output : 
            {  
              'money': 9000, 
              'info': 'mother'
            }

    """
    prepared_data={}
    for field in data_bucket:
        field_type=data_bucket[field]["type"]
        field_data=data_bucket[field]["data"]

        field_postsave_defination=FLEX_TABLE_STRUCTURE["type"][field_type]["pre_save"]
        postsave_function=get_instance_from_settings(field_postsave_defination)

        if(postsave_function!=None):
            task_return_state=postsave_function(field_data)
            prepared_data[field]=task_return_state
            
        else:
            field_value=data_bucket[field]["data"]["value"]
            prepared_data[field]=field_value

        
    return prepared_data


def preUpdateOperation(record_instance,data_bucket):
    """
    The function is used to perform the operation before prepare data for saving like delete the old file .

    It runs the function for a field that is defined in 
      settings.py --> FLEX_TABLE_STRUCTURE --> "type" --> "{the field}" --> "pre_update"

    Input: 
           record_instance=FlexRecordTable.objects.get

           data_bucket={
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
    """
    for field in data_bucket:
        field_type=data_bucket[field]["type"]

        field_postsave_defination=FLEX_TABLE_STRUCTURE["type"][field_type]["pre_update"]
        preupdate_function=get_instance_from_settings(field_postsave_defination)

        if(preupdate_function!=None):
            preupdate_function(record_instance,field)


def fill_undefined_column(table_instance,data_dict):
    """
    Fill the fields that are not filled by user but present in the user defined 
    table_struncture in FlexTable model

    Input:
          data_dict={  
              'money': 9000, 
              'info': 'mother'
            }

        table_instance=FlexTable.objects.get


    Output:
           { 
            'money': 9000, 
            'info': 'mother', 
            'profile': None
           }
    """
    table_structure=table_instance.table_structure
    predined_fields=list(table_structure["column"])
    inputed_fields=list(data_dict)
    undefined_fields=set(predined_fields)-set(inputed_fields)

    for undefined_field in undefined_fields:
        data_dict[undefined_field]=None
    
    return data_dict