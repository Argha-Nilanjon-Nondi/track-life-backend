
from django.utils.decorators import decorator_from_middleware

class CustomMiddleware:

    def __init__(self, view_func, *m_args, **m_kwargs):
        """
        Initialize the decorator with the view function and additional arguments.
        
        :param view_func: The view function to be decorated.
        :param m_args: Additional positional arguments for the decorator.
        :param m_kwargs: Additional keyword arguments for the decorator.
        """
        self.view_func = view_func
        self.m_args = m_args
        self.m_kwargs = m_kwargs

    def process_request(self, request):
        print("Processing request")
        # You can return an HttpResponse to stop further processing
        request.age=90
        # If "None" is return , it indicates that further process should be continue , 
        # else further process should be stopped (Include : process_response and views )
        return None # HttpResponse("kkj")

    def process_response(self, request, response):
        print("Processing response")
        response.headers["Age"] = 120

        # response should be returned . There is no scope for "None"
        return response
    
simple_decorator=decorator_from_middleware(CustomMiddleware)




class IsUserHasAccessToTableMiddleware:

    def __init__(self, view_func, *m_args, **m_kwargs):
        """
        Initialize the decorator with the view function and additional arguments.
        
        :param view_func: The view function to be decorated.
        :param m_args: Additional positional arguments for the decorator.
        :param m_kwargs: Additional keyword arguments for the decorator.
        """
        self.view_func = view_func
        self.m_args = m_args
        self.m_kwargs = m_kwargs

    def process_request(self, request):
        
        return None # HttpResponse("kkj")

    def process_response(self, request, response):
        print("Processing response")
        response.headers["Age"] = 120

        # response should be returned . There is no scope for "None"
        return response
    
table_acess_middleware=decorator_from_middleware(IsUserHasAccessToTableMiddleware)

