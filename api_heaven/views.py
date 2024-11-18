from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
import importlib
from track_life_back.settings import FLEX_TABLE_STRUCTURE
from .serializers import EmailTokenObtainPairSerializer,FlexTableSerializer
from .middlewares import simple_decorator,table_acess_middleware
from .models import FlexTable


class EmailTokenObtainPairView(TokenViewBase):
    serializer_class = EmailTokenObtainPairSerializer


def get_class_from_settings(class_path):
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

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
    print(request.age)
    single_table=FlexTable.objects.get(id=table_uuid)
    table_structure=single_table.table_structure

    post_data_bag={

    }
    
    for field in request.data:

        # data that is sent by the client or browser
        req_field_value=request.data[field]

        # get the field type and validation parameter from the table
        field_type=table_structure["column"][field]["type"]
        field_parameter=table_structure["column"][field]["parameter"]
        
        # get string defination of validation serializer class from settings.py 
        # and convert it to actual class
        field_serializer_defination=FLEX_TABLE_STRUCTURE["type"][field_type]["serializer"]
        serializer_class=get_class_from_settings(field_serializer_defination)

        serializer_obj=serializer_class(data={"value":req_field_value,"parameter":field_parameter})
        if(serializer_obj.is_valid()==False):
            return Response(serializer_obj.errors, status=status.HTTP_400_BAD_REQUEST)
        
        post_data_bag[field]={"value":serializer_obj.validated_data,
                              "type":field_type,
                              "parameter":field_parameter}

        print(post_data_bag)
        

    return Response("success")

        
    #     field_serializer=field_conf["serilizer"]
    #     if(field_serializer!=None):
    #         serializer_class=get_class_from_settings(field_serializer)
    #         serializer=serializer_class(data=request.data)

    


