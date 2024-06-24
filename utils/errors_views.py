from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def handler404(request, exception):
    message = ["Path not found: {}".format(request.path)]
    response = JsonResponse(data={"error": message})
    response.status_code = 404
    return response


@requires_csrf_token
def handler500(request, exception):
    message = ["Internal server error message"]
    response = JsonResponse(data={"error": message})
    response.status_code = 500
    return response
