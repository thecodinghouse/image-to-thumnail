
def generate_thumb(original, size, image_format='JPEG'):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail. Also creates a Thumb File.
    Arguments:
    original -- The image being resize as `File`.
    size     -- Desired thumbnail size as `tuple`. Example: (70, 100)
    format   -- Format of the original image ('JPEG', 'PNG', ...) The thumbnail will be generated using this same format
    """
    Attachment = apps.get_model('attachments', 'Attachment')
    original.seek(0)
    image = Image.open(original)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    thumbnail = ImageOps.fit(image, size, Image.ANTIALIAS)
    io_file = io.BytesIO()
    if image_format.upper() == 'JPG':
        image_format = 'JPEG'
    thumb_title = object.title
    thumbnail.save(io_file, image_format)
    # To convert image to File .
    # This is helpful when u need to save Image in File field.
    thumb_file = InMemoryUploadedFile(io_file, None, 'foo_thumb.'+image_format,
                                      'image/jpeg', io_file.__sizeof__(), None)
    
    return ContentFile(io_file.getvalue())
