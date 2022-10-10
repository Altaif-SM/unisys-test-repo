import uuid


def document_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "other"
    if instance.university_name:
        folder_name = "{}/{}".format("University Guide", instance.university_name.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.file.name)
