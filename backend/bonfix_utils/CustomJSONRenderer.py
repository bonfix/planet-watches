# renderers.py
from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = ""
        success = True
        error = {}
        final_data = {}
        if renderer_context and 'response' in renderer_context:
            status_code = renderer_context.get("response").status_code
            # 2xx -> successful
            if is_success(status_code):
                final_data = data
            else:
                success = False
                if isinstance(data, dict) and 'error_code' in data:
                    error =data
                else:
                    error = {'error_code': '', 'errors': data}

        response_data = {'success': success, 'data': final_data, 'message': '', 'error': error,
                         'status_code': status_code}

        # getattr(renderer_context.get('view').get_serializer().Meta,'resource_name', 'objects')

        # call super to render the response
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)

        return response
