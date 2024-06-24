from django.shortcuts import render , get_object_or_404
def main(request):
    return render(request, 'core/main.html', {})
