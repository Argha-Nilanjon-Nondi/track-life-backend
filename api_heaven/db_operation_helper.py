from api_heaven.models import FileStorageTable

def image_post_process(data):
    """
    data={
          "value":  ,
          "parameter": 
    }

    saving the image is the model and return the id of the record
    """

    file=data["value"]

    file_obj=FileStorageTable(file=file)
    file_obj.save()

    file_id=str(file_obj.id)
    
    return {"file_id":file_id }

def delete_old_file(record_instance,field):
    file_field=record_instance.data_structure[field]
    if(file_field==None):
        return 0
    file_id=file_field['file_id']
    single_file=FileStorageTable.objects.get(id=file_id)
    print("DElete step",record_instance.id)
    single_file.delete()
    