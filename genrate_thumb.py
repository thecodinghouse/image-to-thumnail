
def generate_thumb(object, original, size, image_format='JPEG'):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail
    Arguments:
    original -- The image being resize as `File`.
    size     -- Desired thumbnail size as `tuple`. Example: (70, 100)
    format   -- Format of the original image ('JPEG', 'PNG', ...) The thumbnail will be generated using this same format
    """
    Attachment = apps.get_model('attachments', 'Attachment')
    original.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(original)
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    thumbnail = ImageOps.fit(image, size, Image.ANTIALIAS)
    io_file = io.BytesIO()
    if image_format.upper() == 'JPG':
        image_format = 'JPEG'
    thumb_title = object.title
    thumbnail.save(io_file, image_format)
    thumb_file = InMemoryUploadedFile(io_file, None, thumb_title+'_thumb.'+image_format,
                                      'image/jpeg', io_file.__sizeof__(), None)
    thumb = 'thumbnail'
    thumb_attach = Attachment.objects.create(attachment_type=thumb,
                                             attached_file=thumb_file,
                                             content_object=object.content_object,
                                             object_id=object.object_id,
                                             content_type=object.content_type,
                                             title=object.title,
                                             description=object.description)
    # return ContentFile(io_file.getvalue())
