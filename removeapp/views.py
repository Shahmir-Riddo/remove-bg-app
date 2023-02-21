from django.shortcuts import render
from PIL import Image
import io
from .models import Photo
from rembg import remove

def home(request):
    if request.method == 'POST':
        # get the uploaded image from the form data
        image = request.FILES.get('image')
        if not image:
            # if no image was uploaded, return an error
            return render(request, 'index.html', {'error': 'Please upload an image.'})
        
        # read the image data into a PIL image object
        image_data = io.BytesIO(image.read())
        image = Image.open(image_data)
        
        # use the rembg library to remove the background from the image
        try:
            removed_bg = remove(image)
        except Exception as e:
            # if the background removal fails, return an error
            return render(request, 'index.html', {'error': str(e)})
        
        # save the image with the removed background to a file
        image_file = io.BytesIO()
        removed_bg.save(image_file, format='PNG')
        
        # create a new Photo object and save the image to the database
        photo = Photo()
        photo.image.save('removed_bg.png', image_file, save=True)
        
        # pass the image URL to the template for display
        context = {'image_url': photo.image.url}
        return render(request, 'index.html', context)
    
    return render(request, 'index.html')
