import uuid


def document_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "other"
    if instance.university_name:
        folder_name = "{}/{}".format("University Guide", instance.university_name.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.file.name)


def university_logo_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "University Log"
    if instance.university_name:
        folder_name = "{}/{}".format("University Logo", instance.university_name.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.university_logo.name)

def tanseeq_guide_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "University Tanseeq Guide"
    if instance.university_name:
        folder_name = "{}/{}".format("University Tanseeq Guide", instance.university_name.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.tanseeq_guide.name)


def registration_guide_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "University Registration Guide"
    if instance.university_name:
        folder_name = "{}/{}".format("University Registration Guide", instance.university_name.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.registration_guide.name)


def university_stamp_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "University Stamp"
    if instance.university_name:
        folder_name = "{}/{}".format("University Stamp", instance.university_name.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.university_stamp.name)