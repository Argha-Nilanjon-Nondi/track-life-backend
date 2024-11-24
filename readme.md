### Adding a new field

##### Add a new datatype for the database system . A datatype hold some data under some conditions . 

#### Step 01 :
Create a serializer class in serializers.py . It is responsible for validating inputted data  . Here is starter code for it .
```python

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ExampleFieldSerializer(serializers.Serializer):

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
        

```
You have to write your validation logic in <strong>validate</strong> function . Inside the <strong>validate</strong> function , <strong>value</strong> variable holds the actual data as value and <strong>parameter</strong> variable holds the information from the model that is necessary for validating the <strong>value</strong> variable . When the returning the validation result , <strong>validate</strong> function should return 
```python
    {"value": #The actual value . It will be stored passed towards ,
    "parameter":# It can be None
    }
```
when the validation is successful or raise a <strong>serializers.ValidationError</strong> if the data is not validated .

You can run the serializer class alone to understand it's data flow . Like running the <strong>IntegerFieldSerializer</strong> from <strong>serializers.py</strong> . Here is the code :
```python
obj=IntegerFieldSerializer(data={"value":"9","parameter":None})
print(obj.is_valid())
print(obj.validated_data)
```
Output
```
False
{}
```
<br></br>
```python
obj=IntegerFieldSerializer(data={"value":"90","parameter":None})
print(obj.is_valid())
print(obj.validated_data)
```
Output
```
True
{'value': 90, 'parameter': None}
```
Now add the serializer class in <strong>settings.py</strong> . Format is :
```python
FLEX_TABLE_STRUCTURE={
    "type":{

        "field_name":{
            "serializer":"app_name.file_name.serializer_class",
            "post_save":None , # can be a fuction,
            "pre_update":None # can be a fuction
        }

    }
}
```
Like adding <strong>IntegerFieldSerializer</strong> in <strong>settings.py</strong> .
```python
FLEX_TABLE_STRUCTURE={
    "type":{

        "integer":{
            "serializer":"api_heaven.serializers.IntegerFieldSerializer",
            "post_save":None,
            "pre_update":None
        }

    }
}
```