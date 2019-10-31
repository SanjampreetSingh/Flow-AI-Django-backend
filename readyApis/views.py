import json
import requests
import time

# Django
from django.conf import settings

# Django Rest Framework Files
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Django Rest Framework JWT
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Local
from .models import (
    ReadyApis,
    ReadyApiMedia,
    ReadyApiCategory
)
from .serializer import (
    ReadyApiSerializer,
    ReadyApiMediaSerializer,
    ReadyApiCategorySerializer,
    ReadyApiDemoSerializer
)
from comman import response


# Ready Api's List
class ReadyApiList(ListAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = ReadyApis.objects.filter(category=category)
        else:
            queryset = ReadyApis.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ReadyApiSerializer(queryset, many=True)
        response_data = {
            'readyApis': serializer.data
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api list.', response_data, status.HTTP_200_OK)


# Ready Api's Retrieve
class ReadyApiRetrieve(RetrieveAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'reference_url'

    def retrieve(self, request, reference_url):
        queryset = ReadyApis.objects.all()
        serializer = ReadyApiSerializer(queryset, many=True)
        response_data = {
            'readyApiData': serializer.data[0]
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api details.', response_data, status.HTTP_200_OK)


# Ready Api's Media List
class ReadyApiMediaList(ListAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = ReadyApiMedia.objects.filter(category=category)
        else:
            queryset = ReadyApiMedia.objects.all()
        return queryset

    def list(self, request):
        queryset = ReadyApiMedia.objects.all()
        serializer = ReadyApiMediaSerializer(queryset, many=True)
        response_data = {
            'readyApisMedia': serializer.data
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api media list.', response_data, status.HTTP_200_OK)


# Ready Api Category List
class ReadyApiCategoryList(ListAPIView):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = ReadyApiCategory.objects.all()
        serializer = ReadyApiCategorySerializer(queryset, many=True)
        response_data = {
            'readyApisCategory': serializer.data
        }
        return response.MessageWithStatusSuccessAndData(True, 'Ready api categories list.', response_data, status.HTTP_200_OK)


# Ready Api Demo
@api_view(['POST'])
@permission_classes((AllowAny,))
def readyApiDemo(request):
    if request.method == 'POST':
        image_id = str(request.data.get('data'))
        if image_id == "1":
            api_data = '{"demoData":{"statusCode":200,"headers":{"Content-Type":"application/json"},"body":[[315.84075927734375,56.21873474121094,370.674560546875,128.3153839111328,0.9999943971633911],[81.28703308105469,249.41310119628906,167.98178100585938,359.01800537109375,0.999994158744812],[430.3829650878906,43.89359664916992,493.8914489746094,124.37181091308594,0.999991774559021],[203.74072265625,105.91801452636719,269.01702880859375,191.30026245117188,0.9999885559082031],[352.22607421875,150.14749145507812,412.84454345703125,226.40687561035156,0.9999833106994629],[329.4535827636719,246.4987030029297,396.7242736816406,334.6027526855469,0.9999792575836182],[170.6697998046875,0.12641143798828125,244.57606506347656,77.04454040527344,0.9999616146087646],[124.02422332763672,110.30476379394531,193.867919921875,191.3720245361328,0.9999344348907471],[486.0078125,228.91690063476562,568.6431884765625,298.56524658203125,0.999923586845398],[73.91069030761719,0.006099700927734375,133.17337036132812,54.27813720703125,0.9999010562896729],[373.1219482421875,0.49541664123535156,433.6070556640625,43.566307067871094,0.9929908514022827]]}}'
        if image_id == "2":
            api_data = '{"demoData":{"statusCode":200,"headers":{"Content-Type":"application/json"},"body":[[102.26375579833984,159.255859375,210.79351806640625,299.20941162109375,0.9999998807907104],[9.990856170654297,112.81219482421875,67.08401489257812,190.006591796875,0.9999947547912598],[28.007137298583984,229.0876922607422,97.17388916015625,305.4299011230469,0.9999873638153076],[140.69015502929688,67.93753051757812,189.73574829101562,134.13894653320312,0.999981164932251],[229.39453125,133.30929565429688,310.93194580078125,234.14633178710938,0.9999321699142456]]}}'
        if image_id == "3":
            api_data = '{"demoData":{"statusCode":200,"headers":{"Content-Type":"application/json"},"body":[[366.3166809082031,136.19155883789062,426.15435791015625,208.92369079589844,0.9999880790710449],[346.7185363769531,55.96726989746094,379.60711669921875,97.50863647460938,0.999968409538269],[270.28289794921875,72.3869857788086,300.5570983886719,109.03252410888672,0.9999488592147827],[125.82087707519531,197.2235870361328,172.5245819091797,257.1383361816406,0.9999463558197021],[468.8818359375,180.88497924804688,519.5628662109375,239.59657287597656,0.9999431371688843],[182.73532104492188,130.5444793701172,228.47152709960938,195.9250946044922,0.9999340772628784],[283.2081604003906,111.96135711669922,329.02203369140625,172.52381896972656,0.9998680353164673],[212.1682891845703,70.08675384521484,247.77395629882812,115.73612213134766,0.9998194575309753],[431.4896240234375,104.11209869384766,475.8827209472656,158.36978149414062,0.9997896552085876],[270.9354553222656,35.45942687988281,297.115234375,66.37181854248047,0.9997395873069763],[543.4480590820312,196.06605529785156,587.3153076171875,249.15090942382812,0.9996433258056641]]}}'
        if image_id == "4":
            api_data = '{"demoData":{"statusCode":200,"headers":{"Content-Type":"application/json"},"body":[[467.5672912597656,65.9019546508789,543.3988037109375,152.509521484375,0.9999688863754272],[34.65276336669922,52.63544464111328,202.54263305664062,264.7346496582031,0.9999377727508545],[361.38690185546875,88.02693176269531,403.79852294921875,151.15695190429688,0.9995026588439941]]}}'
        if image_id == "6":
            api_data = '{"demoData":{"statusCode":200,"headers":{"Content-Type":"application/json"},"body":[[133.1839599609375,81.20558166503906,198.7433319091797,174.05496215820312,0.9999736547470093],[242.86758422851562,32.01306915283203,274.3721008300781,67.8658447265625,0.9998873472213745],[47.55480194091797,11.717527389526367,81.9598159790039,53.61799621582031,0.9998769760131836],[211.40347290039062,-0.17023849487304688,245.79843139648438,35.24086380004883,0.999874472618103],[25.5382137298584,54.148460388183594,71.46881866455078,110.9757080078125,0.9997939467430115],[231.11732482910156,78.09113311767578,274.74151611328125,133.32183837890625,0.9997711777687073],[76.04698944091797,90.12435913085938,120.40255737304688,142.63262939453125,0.9995819926261902],[108.44792175292969,24.67598533630371,151.38002014160156,78.59083557128906,0.9993640780448914],[168.59063720703125,3.3677024841308594,201.70953369140625,46.81584548950195,0.9992069602012634],[82.93480682373047,9.621786117553711,112.58179473876953,50.64106750488281,0.9988973140716553],[200.239501953125,66.98273468017578,233.527099609375,110.89488220214844,0.99747234582901],[133.37179565429688,-0.5755443572998047,159.84640502929688,26.41443634033203,0.9918246865272522],[11.225198745727539,-1.2903509140014648,38.62762451171875,19.7777099609375,0.9370516538619995],[269.375732421875,5.59990119934082,284.2210693359375,34.56988525390625,0.6577404141426086]]}}'

        response_data = json.loads(api_data)
        time.sleep(1)
        return response.MessageWithStatusSuccessAndData(True, 'Ready api demo.', response_data, status.HTTP_200_OK)
    else:
        return response.Error400WithMessage('Bad Request.')

# def readyApiDemo(request):
#     if request.method == 'POST':
#         serializer = ReadyApiDemoSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             apikey = settings.DEMO_API_KEY

#             api = ReadyApis.objects.get(pk=serializer.data.get('api_id'))

#             api_data = {
#                 'data': serializer.data.get('data')
#             }

#             data = json.dumps(api_data)

#             headers = {
#                 'x-api-key': apikey,
#                 'Content-Type': 'application/x-www-form-urlencoded'
#             }

#             req = requests.post(
#                 api.cloud_url, data=data, headers=headers)

#             response_data = {
#                 'demoData': req.json()
#             }

#             return response.MessageWithStatusSuccessAndData(True, 'Ready api demo.', response_data, status.HTTP_200_OK)
#         else:
#             return response.SerializerError(serializer.errors)
#     else:
#         return response.Error400WithMessage('Bad Request.')
