from django.shortcuts import render
from PIL import Image
import io
from .models import Photo
from rembg import remove

def home(request):
    if request.method == 'POST':

        image = request.FILES.get('image')
        if not image:
       
            return render(request, 'index.html', {'error': 'Please upload an image.'})
        
  
        image_data = io.BytesIO(image.read())
        image = Image.open(image_data)
        

        try:
            removed_bg = remove(image)
        except Exception as e:
      
            return render(request, 'index.html', {'error': str(e)})
        

        image_file = io.BytesIO()
        removed_bg.save(image_file, format='PNG')

        photo = Photo()
        photo.image.save('removed_bg.png', image_file, save=True)

        context = {'image_url': photo.image.url}
        return render(request, 'index.html', context)
    
    return render(request, 'index.html')
