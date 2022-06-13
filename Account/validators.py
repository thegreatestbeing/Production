def video(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.avi' '.mkv', '.m4v']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')


def image(value):
	import os
	from django.core.exceptions import ValidationError
	ext = os.path.splitext(value.name)[1] # [0] returns path+filename
	valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
	if not ext.lower()in valid_extensions:
		raise ValidationError(u'Unsupported file extension.')