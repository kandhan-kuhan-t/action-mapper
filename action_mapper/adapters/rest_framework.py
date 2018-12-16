from rest_framework import views
from action_mapper import ActionMapperMixin


class ActionMappedAPIView(views.APIView, ActionMapperMixin):

    def map_incoming_to_action(self, in_data: dict, *args, **kwargs):
        raise NotImplementedError()

    def map_action_output_to_response(
            self,
            *args,
            **kwargs
    ):
        raise NotImplementedError()

    def response_generator(self, data):
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        response = self.run(incoming_data=request.data, *args, **kwargs)
        return self.response_generator(response)
