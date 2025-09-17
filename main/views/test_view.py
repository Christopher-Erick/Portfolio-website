from django.shortcuts import render
from django.http import HttpResponse

def test_social_links(request):
    """Test view to check social links rendering"""
    return render(request, 'test_social_links.html')