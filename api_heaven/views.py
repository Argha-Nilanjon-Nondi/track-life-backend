from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from track_life_back.settings import FLEX_TABLE_STRUCTURE
from .serializers import EmailTokenObtainPairSerializer,FlexTableSerializer
from .middlewares import simple_decorator,table_acess_middleware
from .models import FlexTable,FlexRecordTable
from .utils import validate_fields,prepare_data_createRecord,fill_undefined_column,preUpdateOperation



class EmailTokenObtainPairView(TokenViewBase):
    serializer_class = EmailTokenObtainPairSerializer





@api_view(["GET"])
@simple_decorator
@permission_classes([IsAuthenticated])
def profile(request):
    print(f"Age is {request.age}")
    return Response("You have access to this view because you're authenticated!")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_table(request):

    table_name=request.data["table_name"]
    table_structure=request.data["table_structure"]


    serializer = FlexTableSerializer(data=request.data)
    if serializer.is_valid():
        table=FlexTable(user=request.user,table_name=table_name,table_structure=table_structure)
        table.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@table_acess_middleware
def add_to_table(request,table_uuid):
    single_table=FlexTable.objects.get(id=table_uuid)
    

    validate_state=validate_fields(table_instance=single_table,data_dict=request.data)

    validation_status=validate_state["validation_status"]
    validation_msg=validate_state["validation_msg"]
    post_data_bag=validate_state["data_bag"]
    
   
    if(validation_status==False):
        return Response(validation_msg, status=status.HTTP_400_BAD_REQUEST)

    
    prepared_data=prepare_data_createRecord(post_data_bag)

    final_data=fill_undefined_column(table_instance=single_table,data_dict=prepared_data)

    record=FlexRecordTable.objects.create(
        flex_table=single_table,
        data_structure=final_data
    )
        
    print(record.id)

    return Response("success")

        
    #     field_serializer=field_conf["serilizer"]
    #     if(field_serializer!=None):
    #         serializer_class=get_class_from_settings(field_serializer)
    #         serializer=serializer_class(data=request.data)

    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@table_acess_middleware
def update_record(request,table_uuid,record_uuid):
    single_table=FlexTable.objects.get(id=table_uuid)
    single_record=FlexRecordTable.objects.get(id=record_uuid)
    
    validate_state=validate_fields(table_instance=single_table,data_dict=request.data)

    validation_status=validate_state["validation_status"]
    validation_msg=validate_state["validation_msg"]
    post_data_bag=validate_state["data_bag"]

    if(validation_status==False):
        return Response(validation_msg, status=status.HTTP_400_BAD_REQUEST)
    
    preUpdateOperation(record_instance=single_record,data_bucket=post_data_bag)

    

    
    prepared_data=prepare_data_createRecord(post_data_bag)

    for field in prepared_data:
        single_record.data_structure[field]=prepared_data[field]

    single_record.save()

    print(single_record.id)

    return Response("success")

