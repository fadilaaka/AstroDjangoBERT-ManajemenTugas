import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from transformers import TextClassificationPipeline, BertTokenizer, BertForSequenceClassification
from safetensors.torch import load_file
import logging

logger = logging.getLogger("mylogger")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.safetensors')
logger.info(MODEL_PATH)
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model_state = load_file(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=3, state_dict=model_state)

def index(request):
    if request.method == 'GET':
        tugas = Task.objects.all()
        data = list(tugas.values())
        response = {
            'status': True,
            'data': data,
        }
        return JsonResponse(response)

@csrf_exempt
def tambah(request):
    if request.method == 'POST':
        try:
            RoleClassModelPipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False)

            def get_RoleClass(INPUT: str):
                id: int = int(RoleClassModelPipe(INPUT)[0]['label'].split("_")[1])
                mapping = {
                    0: "rendah",
                    1: "sedang",
                    2: "tinggi"
                }
                return mapping.get(id, "Unknown")

            body = json.loads(request.body)
            judul = body.get('judul')
            deskripsi = body.get('deskripsi')
            deadline = body.get('deadline')
            status = body.get('status', 'belum_selesai')
            # prioritas = body.get('prioritas')

            hasil_prioritas = get_RoleClass(judul)
            logger.info(hasil_prioritas)

            if not all([judul, deskripsi, deadline]):
                return JsonResponse({'status': False, 'message': 'Missing required fields'}, status=400)

            task = Task.objects.create(
                judul=judul,
                deskripsi=deskripsi,
                deadline=deadline,
                status=status,
                prioritas=hasil_prioritas
            )

            response = {
                'status': True,
                'message': 'Data berhasil ditambahkan',
                'data': {
                    'id': task.id,
                    'judul': task.judul,
                    'deskripsi': task.deskripsi,
                    'deadline': task.deadline,
                    'status': task.status,
                    'prioritas': task.prioritas,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at,
                }
            }
            return JsonResponse(response, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method'}, status=405)

# @csrf_exempt fungsi untuk menghilangkan protection csrf
@csrf_exempt 
def edit(request, id):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            try:
                task = Task.objects.get(id=id)
            except Task.DoesNotExist:
                return JsonResponse({'status': False, 'message': 'Task not found'}, status=404)
            
            task.judul = body.get('judul', task.judul)
            task.deskripsi = body.get('deskripsi', task.deskripsi)
            task.deadline = body.get('deadline', task.deadline)
            task.status = body.get('status', task.status)
            task.prioritas = body.get('prioritas', task.prioritas)
            task.save()

            response = {
                'status': True,
                'message': 'Data berhasil diperbarui',
                'data': {
                    'id': task.id,
                    'judul': task.judul,
                    'deskripsi': task.deskripsi,
                    'deadline': task.deadline,
                    'status': task.status,
                    'prioritas': task.prioritas,
                    'created_at': task.created_at,
                    'updated_at': task.updated_at,
                }
            }
            return JsonResponse(response, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def hapus(request, id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return JsonResponse({'status': True, 'message': 'Data berhasil dihapus'}, status=204)
        except Task.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'Task not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method'}, status=405)