from rest_framework.routers import DefaultRouter


class NoPutRouter(DefaultRouter):

    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)

        if 'put' in bound_methods.keys():
            del bound_methods['put']

        return bound_methods
