from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import update_last_login
from .models import FlexTable

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop(self.username_field, None) 
        self.fields.pop("password", None)  

        self.fields["email"] = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        # Get the email from the request data
        email = self.initial_data.get('email')

        if not email:
            raise AuthenticationFailed("Email is required for authentication.")

        try:
            # Check if the email exists in the database
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("No active account found with the given email.")

        if not user.is_active:
            raise AuthenticationFailed("User account is inactive.")

        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)

        update_last_login(None, user)
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class FlexTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlexTable
        fields = ['table_name', 'table_structure']

    # table_name=serializers.CharField(max_length=255,required=True)
    # table_structure=serializers.JSONField(required=True)

    def validate(self, data):

        table_structure=data["table_structure"]

        for column in table_structure:

            if(("column_name" not in column) or ("type" not in column) or ("data" not in column)):
                raise serializers.ValidationError("Missing required keys in table_structure")

        return data

# input_data=[{
#          "column_name":"Coding",
#          "type":"text",
#          "data":{}}
#          ]


# fts=FlexTableSerializer(data={"table_name":"Hello Table","table_structure":input_data})
# print(fts.is_valid())

"""
Starter code for a field serilizer .


class ExampleFieldSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        value=data["value"]
        parameter=data["parameter"]

        field = serializers.ExampleField() # act as helper from the rest_framework

        try:
            validated_data = field.run_validation(value)
            return {"value":validated_data,"parameter":None}
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)

"""

class IntegerFieldSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        value=data["value"]
        parameter=data["parameter"]

        field = serializers.IntegerField()

        try:
            validated_data = field.run_validation(value)
            return {"value":validated_data,"parameter":None}
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        

class DateFieldSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        value=data["value"]
        parameter=data["parameter"]

        field = serializers.DateField()

        try:
            validated_data = field.run_validation(value)
            return {"value":str(validated_data),"parameter":None}
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)


# Using IntegerFieldSerializer
# obj=IntegerFieldSerializer(data={"value":"90","parameter":None})
# print(obj.is_valid())
# print(obj.validated_data)        


class TextFieldSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        value=data["value"]
        parameter=data["parameter"]

        field = serializers.CharField()

        try:
            validated_data = field.run_validation(value)
            return {"value":validated_data,"parameter":None}
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        

class ImageFieldSerializer(serializers.Serializer):

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        value=data["value"]
        parameter=data["parameter"]

        field = serializers.ImageField(allow_empty_file=False)



        try:
            validated_data = field.run_validation(value)
            return {"value":validated_data,"parameter":None}
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)
        
    
