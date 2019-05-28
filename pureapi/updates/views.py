import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Update
from django.views.generic import View
from restapi.mixing import JsonResponseMixing
from django.core.serializers import serialize
# Create your views here.

def json_example_view(request):
    data={
        'count':1000,
        'content':'some new content'
    }
    #json_data=json.dumps(data)
    #return HttpResponse(json_data)
    return JsonResponse(data)

class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        data={
            'count':1000,
            'content':'some new content'
        }
        #json_data=json.dumps(data)
        #return HttpResponse(json_data)
        return JsonResponse(data)


class JsonCBV2(JsonResponseMixing, View):
    def get(self, request, *args, **kwargs):
        data={
            'count':1000,
            'content':'some new content'
        }
        return self.render_to_json_response(data)

class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj=Update.objects.get(id=1)
        #data=serialize("json", [obj,], fields=('user', 'content'))
        data=obj.serialize()
        return HttpResponse(data, content_type='application/json')

class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        #qs=Update.objects.all()
        #data=serialize("json", qs, fields=('user', 'content'))
        data=Update.objects.all().serialize()
        return HttpResponse(data)
