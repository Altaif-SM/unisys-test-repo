import uuid
from tanseeq_app import models

def profile_picture_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "Profile Picture"
    if instance.application:
        folder_name = "{}/{}".format("Profile Picture", instance.application.tanseeq_id.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.photo.name)


def school_certificate_upload_path(instance, filename):
    """
    helper function to add unique identifier to file name
    """
    folder_name = "School Certificate"
    if instance.application:
        folder_name = "{}/{}".format("School Certificate", instance.application.tanseeq_id.strip())
    return '{}/{}--{}'.format(folder_name, str(uuid.uuid4()), instance.school_certificate.name)


def get_tanseeq_application(user):
    return models.ApplicationDetails.objects.filter(created_by=user).first()

def get_tanseeq_application_by_email(application_email):
    return models.ApplicationDetails.objects.filter(user__username=application_email).first()