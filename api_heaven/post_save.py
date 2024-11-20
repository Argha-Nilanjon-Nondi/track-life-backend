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