import io
import os
from PIL import Image, ImageDraw

############### OCR ###############
from google.cloud import vision # Imports the Google Cloud client library
i = 0
FILE_PATH = './files/'

def run_model(img_path, record_path):
    # Set environmen`t variable
    # credential_path = "/Users/ihaneul/Desktop/mldl/eyekey-venv/eyekey/eyekey-OCR.json"
    credential_path = os.path.abspath("eyekey-OCR.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

    # Instantiates a client
    ocr_client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    image_name = os.path.abspath(img_path)

    # Loads the image into memory
    with io.open(image_name, 'rb') as image_file:
        ocr_content = image_file.read()

    image = vision.Image(content=ocr_content)
    img = Image.open(img_path[2:]).convert('RGB')

    # Performs text detection on the image file
    ocr_response = ocr_client.text_detection(image=image)
    ocr_texts = ocr_response.text_annotations

    ############### STT ###############

    from google.cloud import speech

    credential_path_STT = os.path.abspath("eyekey-STT.json")
    # credential_path_STT = '/Users/ihaneul/Desktop/mldl/eyekey-venv/eyekey/eyekey-STT.json'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path_STT

    stt_client = speech.SpeechClient()

    stt_file = os.path.abspath(record_path)

    with io.open(stt_file, 'rb') as audio_file:
        stt_content = audio_file.read()

    audio = speech.RecognitionAudio(content=stt_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code='ko-KR',
        use_enhanced=True)

    stt_response = stt_client.recognize(config=config, audio=audio)
    for search in stt_response.results:
        search = search.alternatives[0].transcript

    ###############     ###############

    first_array = []
    second_array = []
    third_array = []
    fourth_array = []

    for text in ocr_texts:
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices])
        if text.description in search:
            right_up, left_down = vertices[1], vertices[3]
            first_array.append(int(right_up[1:4]))
            second_array.append(int(right_up[5:8]))
            third_array.append(int(left_down[1:4]))
            fourth_array.append(int(left_down[5:8]))

    while len(first_array) == 0:
        sys.exit('검색 결과가 없습니다.')

    draw = ImageDraw.Draw(img)

    for i in range(len(first_array)):
        bound = [first_array[i]+10, second_array[i]-10, third_array[i]-10, fourth_array[i]+10]
        draw.rectangle((bound), outline=(255,0,0), width = 6)

    i = i+1
    img.save(FILE_PATH + f'{i}.jpg')
    return(FILE_PATH + f'{i}.jpg')