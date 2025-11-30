# from django.shortcuts import render
# from .forms import ImageUploadForm
# from upload.services.model import Image3DConverter  # Ensure correct class name
# import os
# from django.conf import settings
# from django.http import JsonResponse
# import base64

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the uploaded image
#             image = form.save()
#             image_path = image.image.path

#             # Convert the image to a 3D model
#             api_key = 'YOUR_API_KEY'  # Replace with your actual API key
#             converter = Image3DConverter(api_key)
#             model_data = converter.convert_image(image_path)

#             if model_data:
#                 # Save the generated 3D model
#                 model_dir = os.path.join(settings.MEDIA_ROOT, 'models')
#                 os.makedirs(model_dir, exist_ok=True)  # Create directory if it doesn't exist
#                 model_path = os.path.join(model_dir, f'{image.id}.glb')

#                 with open(model_path, 'wb') as f:
#                     f.write(model_data)  # Ensure model_data is in binary format

#                 # Prepend MEDIA_URL to model_path for use in the template
#                 model_url = os.path.join(settings.MEDIA_URL, 'models', f'{image.id}.glb')
#                 return render(request, 'upload/result.html', {'model_file': model_url})
#             else:
#                 return render(request, 'upload/upload.html', {'form': form, 'error': 'Failed to convert image to 3D model.'})
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload/upload.html', {'form': form})







# from django.conf import settings

# def d3(request, model_id):
#     model_file = f'{settings.MEDIA_URL}models/{model_id}.glb'
#     return render(request, 'upload/3d.html', {'model_file': model_file})




# def save_image(request):
#     if request.method == 'POST':
#         data_url = request.body.decode('utf-8').split('imageData=')[1]
#         format, imgstr = data_url.split(';base64,') 
#         ext = format.split('/')[-1]  # Get the image extension
#         filename = f'models/rendered_image.{ext}'  # Change the filename as needed
#         path = os.path.join(settings.MEDIA_ROOT, filename)
        
#         # Save the image
#         with open(path, 'wb') as f:
#             f.write(base64.b64decode(imgstr))
        
#         return JsonResponse({'status': 'Image saved successfully!', 'path': filename})
#     return JsonResponse({'status': 'Failed to save image.'})






from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ImageUploadForm, SignupForm
from .models import ImageUpload
from upload.services.model import Image3DConverter
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import os
import base64
import json
import time
from .services.mongo import mongo_log_signup, mongo_log_login


def home(request):
    import os
    from django.conf import settings
    
    # Get all 3D models from the models directory
    models_dir = os.path.join(settings.MEDIA_ROOT, 'models')
    models = []
    
    if os.path.exists(models_dir):
        for filename in os.listdir(models_dir):
            if filename.endswith('.glb'):
                model_id = filename.replace('.glb', '')
                # Try to get the corresponding uploaded image
                try:
                    # Check if model_id is a valid integer
                    if model_id.isdigit():
                        image = ImageUpload.objects.get(id=int(model_id))
                        image_url = image.image.url
                        image_name = os.path.basename(image.image.name)
                    else:
                        # Handle non-numeric model IDs (like test_model)
                        image_url = None
                        image_name = f"Model {model_id}"
                except (ImageUpload.DoesNotExist, ValueError):
                    image_url = None
                    image_name = f"Model {model_id}"
                
                models.append({
                    'id': model_id,
                    'name': image_name,
                    'image_url': image_url,
                    'model_url': f'/upload/3d/{model_id}/',
                    'file_size': os.path.getsize(os.path.join(models_dir, filename))
                })
    
    # Sort models by ID (newest first), handling non-numeric IDs
    def sort_key(model):
        try:
            return int(model['id'])
        except ValueError:
            return 0  # Put non-numeric IDs at the end
    
    models.sort(key=sort_key, reverse=True)
    
    return render(request, 'home.html', {'models': models})

@login_required(login_url='/upload/login/')
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
            print(image.id, image.image)
            return render(request, 'upload/confirm.html', {
                'image': image,
                'form': form
            })
    else:
        form = ImageUploadForm()
    return render(request, 'upload/upload.html', {'form': form})

@login_required(login_url='/upload/login/')
def confirm_conversion(request, image_id):
    try:
        # image = get_object_or_404(YourImageModel, id=image_id)
        print("confirm_invoked")
        image = ImageUpload.objects.get(id=image_id)
    except ImageUpload.DoesNotExist:
        return render(request, 'upload/error.html', {'error': 'Image not found.'})

    if request.method == 'POST':
        api_key = settings.STABILITY_API_KEY
        # Set to False to use real API, True for testing without credits
        converter = Image3DConverter(api_key, mock_mode=False)
        try:
            model_data = converter.convert_image(image.image.path)
        except Exception as e:
            return render(request, 'upload/error.html', {'error': str(e)})

        if model_data:
            model_dir = os.path.join(settings.MEDIA_ROOT, 'models')
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, f'{image.id}.glb')

            with open(model_path, 'wb') as f:
                f.write(model_data)

            model_url = os.path.join(settings.MEDIA_URL, 'models', f'{image.id}.glb')
            return redirect(reverse('d3_view', kwargs={'model_id': image.id}))
        else:
            return render(request, 'upload/error.html', {'error': 'Failed to convert image to 3D model.'})

    return render(request, 'upload/confirm.html', {'image': image})

def d3(request, model_id):
    model_file = f'{settings.MEDIA_URL}models/{model_id}.glb'
    return render(request, 'upload/3d.html', {'model_file': model_file})

@login_required(login_url='/upload/login/')
def save_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data_url = data.get('imageData', '')
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]
            filename = f'rendered_image_{int(time.time())}.{ext}'
            path = os.path.join(settings.MEDIA_ROOT, 'captured', filename)
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            with open(path, 'wb') as f:
                f.write(base64.b64decode(imgstr))
            
            return JsonResponse({'status': 'Image saved successfully!', 'path': os.path.join(settings.MEDIA_URL, 'captured', filename)})
        except Exception as e:
            return JsonResponse({'status': f'Failed to save image: {str(e)}'}, status=400)
    return JsonResponse({'status': 'Invalid request method.'}, status=405)


@login_required(login_url='/upload/login/')
def gallery(request):
    import os
    from django.conf import settings
    
    # Get all 3D models from the models directory
    models_dir = os.path.join(settings.MEDIA_ROOT, 'models')
    models = []
    
    if os.path.exists(models_dir):
        for filename in os.listdir(models_dir):
            if filename.endswith('.glb'):
                model_id = filename.replace('.glb', '')
                model_file_path = os.path.join(models_dir, filename)
                # Try to get the corresponding uploaded image
                try:
                    if model_id.isdigit():
                        image = ImageUpload.objects.get(id=int(model_id))
                        image_url = image.image.url
                        image_name = os.path.basename(image.image.name)
                        created_at = getattr(image, 'uploaded_at', None)
                        # As a fallback, use the file's modified time
                        if created_at is None:
                            created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(model_file_path)))
                    else:
                        image_url = None
                        image_name = f"Model {model_id}"
                        created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(model_file_path)))
                except (ImageUpload.DoesNotExist, ValueError):
                    image_url = None
                    image_name = f"Model {model_id}"
                    created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(model_file_path)))

                models.append({
                    'id': model_id,
                    'name': image_name,
                    'image_url': image_url,
                    'model_url': f'/upload/3d/{model_id}/',
                    'file_size': os.path.getsize(model_file_path),
                    'created_at': created_at,
                })
    
    # Sort models by ID (newest first), handling non-numeric IDs
    def sort_key(model):
        try:
            return int(model['id'])
        except ValueError:
            return 0  # Put non-numeric IDs at the end
    
    models.sort(key=sort_key, reverse=True)
    
    return render(request, 'upload/gallery.html', {'models': models})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            dob = form.cleaned_data.get('date_of_birth')
            mongo_log_signup({
                'username': user.username,
                'email': user.email,
                'date_of_birth': str(dob) if dob else None,
                'event': 'signup',
                'ts': int(time.time())
            })
            login(request, user)
            return redirect('upload_image')
    else:
        form = SignupForm()
    return render(request, 'upload/auth/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            mongo_log_login({
                'username': username,
                'event': 'login',
                'ts': int(time.time())
            })
            return redirect('upload_image')
        return render(request, 'upload/auth/login.html', {'error': 'Invalid credentials'})
    return render(request, 'upload/auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@require_POST
def delete_model(request, model_id):
    models_dir = os.path.join(settings.MEDIA_ROOT, 'models')
    model_path = os.path.join(models_dir, f'{model_id}.glb')

    # Remove the .glb file if present
    if os.path.exists(model_path):
        try:
            os.remove(model_path)
        except OSError:
            pass

    # If a matching ImageUpload exists, delete its image file and the DB row
    if str(model_id).isdigit():
        try:
            image_obj = ImageUpload.objects.get(id=int(model_id))
            # Delete uploaded image file from storage
            if image_obj.image and hasattr(image_obj.image, 'path') and os.path.exists(image_obj.image.path):
                try:
                    os.remove(image_obj.image.path)
                except OSError:
                    pass
            image_obj.delete()
        except ImageUpload.DoesNotExist:
            pass

    return redirect('gallery')


@require_POST
def delete_all_models(request):
    models_dir = os.path.join(settings.MEDIA_ROOT, 'models')

    # Delete all .glb files
    if os.path.exists(models_dir):
        for filename in os.listdir(models_dir):
            if filename.endswith('.glb'):
                file_path = os.path.join(models_dir, filename)
                try:
                    os.remove(file_path)
                except OSError:
                    pass

    # Delete all uploaded images and DB rows
    for image_obj in ImageUpload.objects.all():
        if image_obj.image and hasattr(image_obj.image, 'path') and os.path.exists(image_obj.image.path):
            try:
                os.remove(image_obj.image.path)
            except OSError:
                pass
        image_obj.delete()

    # Optionally clear captured screenshots if present
    captured_dir = os.path.join(settings.MEDIA_ROOT, 'captured')
    if os.path.exists(captured_dir):
        for filename in os.listdir(captured_dir):
            file_path = os.path.join(captured_dir, filename)
            try:
                os.remove(file_path)
            except OSError:
                pass

    return redirect('gallery')