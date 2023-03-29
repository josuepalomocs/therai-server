import io
import os

import openai
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import vision

from therai.utility import clean_html_string


def index(request):
    return HttpResponse("This is the index endpoint.")


# def gpt(request):
#     openai.api_key = os.getenv('OPENAI_API_KEY')
#     response = openai.Completion.create(model="text-davinci-003", prompt="Write a short sentence", temperature=0,
#                                         max_tokens=10)
#     http_response = "This is the response: " + response.choices[0].text
#     res = {'data': http_response}
#     return JsonResponse(res)
#
#
# def google_vision(request):
#     try:
#         client = vision.ImageAnnotatorClient()
#
#         file_name = os.path.abspath('static/reactdoc.jpg')
#
#         with io.open(file_name, 'rb') as image_file:
#             content = image_file.read()
#
#         image = vision.Image(content=content)
#
#         response = client.document_text_detection(image=image)
#         document = response.full_text_annotation
#
#         res = {'data': document.text}
#     except Exception as e:
#         res = {'data': str(e)}
#     return JsonResponse(res)

@csrf_exempt
def process_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # reading the attached file and extracting text using Google Vision OCR
            image_file = request.FILES['image']

            client = vision.ImageAnnotatorClient()

            content = image_file.read()

            image = vision.Image(content=content)

            response = client.document_text_detection(image=image)
            ocr_output = response.full_text_annotation.text

            # enhancing the OCR output using the OpenAI GPT model

            prompt = f"Given the following raw OCR output, summarize the content while conveying the original " \
                     f"information." \
                     f"\n\n{ocr_output}\n\n"

            openai.api_key = os.getenv('OPENAI_API_KEY')
            openai_response = openai.Completion.create(model="text-davinci-003", prompt=prompt,
                                                       temperature=0.7, max_tokens=250)
            openai_response_text = openai_response.choices[0].text

            openai_response_text_clean = clean_html_string(openai_response_text)

            json_response = {'text': openai_response_text_clean}
        except Exception as e:
            json_response = {'error': str(e)}
        return JsonResponse(json_response)
    return HttpResponseBadRequest('Invalid request.')
