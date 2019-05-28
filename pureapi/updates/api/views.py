from updates.models import Update as UpdateModel
from django.views.generic import View
from django.http import HttpResponse
from .mixins import CSRFExemptMixin
import json
from restapi.mixing import HttpResponseMixin
from updates.forms import UpdateModelForm
from .utility import is_json

class UpdateModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):

    is_json=True #for HttpResponseMixin

    def get_object(self, id=None):

        #First Method to get the object by its id
        # try:
        #     obj=UpdateModel.objects.get(id=id)
        # except:
        #     obj=None

        #Another method to get the object by its id
        qs=UpdateModel.objects.filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None


    #for create
    def post(self, request, id, *args, **kwargs):
        json_data=json.dumps({'message':'Not allowed, please use the api/updates/ endpoint'})
        return self.render_to_response(json_data, status=403)


    #for retrieve
    def get(self, request, id, *args, **kwargs):
        #obj=UpdateModel.objects.get(id=id)

        #after creating get_object mehtod we can write above statement as below
        obj=self.get_object(id=id)
        if obj is None:
            error_data=json.dumps({'message':'object not found'})
            return self.render_to_response(error_data, status=404)

        json_data=obj.serialize()
        #return HttpResponse(json_data, content_type='application/json')

        return self.render_to_response(json_data)

    #for update
    def put(self, request, id, *args, **kwargs):
        #for validating that the data is json or not
        valid_json=is_json(request.body)
        if not valid_json:
            error_data=json.dumps({'message':'invalid data please send it through JSON'})
            return self.render_to_response(error_data, status=400)



        #return HttpResponse(json_data, content_type='application/json')
        obj=self.get_object(id=id)
        if obj is None:
            error_data=json.dumps({'message':'object not found'})
            return self.render_to_response(error_data, status=404)

        #print(dir(request))
        #print(request.body)
        #print(request.data)

        #this portion is for validating data as we validate it in post method of UpdateModelListAPIView class
        data = json.loads(obj.serialize())
        passed_data=json.loads(request.body)
        for key,value in passed_data.items():
            data[key]=value

        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data=json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_response(json_data, status=400)
        #======================================================================================================

        # new_data=json.loads(request.body)
        # print(new_data['content'])

        json_data=json.dumps({'message':'something'})
        #return HttpResponse(json_data, content_type='application/json')

        return self.render_to_response(json_data)


    #for delete
    def delete(self, request, id, *args, **kwargs):
        #return HttpResponse(json_data, content_type='application/json')
        obj=self.get_object(id=id)
        if obj is None:
            error_data=json.dumps({'message':'object not found'})
            return self.render_to_response(error_data, status=404)

        deleted = obj.delete()
        if deleted==1:
            json_data=json.dumps({'message':'Successfully deleted'})
            #return HttpResponse(json_data, content_type='application/json')
            return self.render_to_response(json_data, status=200)
        error_data=json.dumps({'message':'Could not delete object'})
        return self.render_to_response(error_data, status=403)





# so this is below is the complete one view which handle only one endpoint 'api/updates/'

class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):

    is_json=True
    queryset=None
    # def render_to_response(data, status=200):
    #     return HttpResponse(data, content_type='application/json', status=status)

    def get_queryset(self):
        qs=UpdateModel.objects.all()
        self.queryset=qs
        return qs

    def get_object(self, id=None):
        if id is None:
            return None
        qs=self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return None

    #listview
    def get(self, request, *args, **kwargs):
        data=json.loads(request.body)
        passed_id=data.get('id',None)
        if passed_id is not None:
            obj=self.get_object(id=passed_id)
            if obj is None:
                error_data=json.dumps({'message':'object not found'})
                return self.render_to_response(error_data, status=404)
            json_data=obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs=self.get_queryset()
            json_data=qs.serialize()
            return self.render_to_response(json_data)

    #for create
    def post(self, request, *args, **kwargs):

        #this is for checking that data is json data or not
        valid_json=is_json(request.body)
        if not valid_json:
            error_data=json.dumps({'message':'invalid data please send it through JSON'})
            return self.render_to_response(error_data, status=400)
        data=json.loads(request.body)


        #this is for form manipulation
        #print(request.POST)
        #form = UpdateModelForm(request.POST)
        form = UpdateModelForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data=obj.serialize()
            return self.render_to_response(obj_data, status=201)


        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_response(json_data, status=400)

        #ending of form manipulation

        #This is for old one
        json_data=json.dumps({"message":"not allowed"})
        return self.render_to_response(json_data, status=400)


    # def delete(self, request, *args, **kwargs):
    #     json_data=json.dumps({'message':'you cannot delete an entire list'})
    #     return self.render_to_response(json_data, status=403)

    #for update
    def put(self, request, *args, **kwargs):
        valid_json=is_json(request.body)
        if not valid_json:
            error_data=json.dumps({'message':'invalid data please send it through JSON'})
            return self.render_to_response(error_data, status=400)
        passed_data=json.loads(request.body)
        passed_id=passed_data.get('id', None)

        if not passed_id:
            error_data=json.dumps({'id':'This is an required field to update item'})
            return self.render_to_response(error_data, status=400)

        obj=self.get_object(id=passed_id)
        if obj is None:
            error_data=json.dumps({'message':'object not found'})
            return self.render_to_response(error_data, status=404)

        data = json.loads(obj.serialize())
        passed_data=json.loads(request.body)
        for key,value in passed_data.items():
            data[key]=value

        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data=json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_response(json_data, status=400)

        json_data=json.dumps({'message':'something'})
        return self.render_to_response(json_data)

    #for delete
    def delete(self, request, *args, **kwargs):
        valid_json=is_json(request.body)
        if not valid_json:
            error_data=json.dumps({'message':'invalid data please send it through JSON'})
            return self.render_to_response(error_data, status=400)
        passed_data=json.loads(request.body)
        passed_id=passed_data.get('id', None)

        if not passed_id:
            error_data=json.dumps({'id':'This is an required field to delete item'})
            return self.render_to_response(error_data, status=400)

        obj=self.get_object(id=passed_id)
        if obj is None:
            error_data=json.dumps({'message':'object not found'})
            return self.render_to_response(error_data, status=404)


        deleted_ = obj.delete()
        if deleted_==True:
            json_data=json.dumps({'message':'Successfully deleted'})
            #return HttpResponse(json_data, content_type='application/json')
            return self.render_to_response(json_data, status=200)
        else:
            error_data=json.dumps({'message':'Could not delete object'})
            return self.render_to_response(error_data, status=403)
