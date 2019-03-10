from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.contenttypes.models import ContentType


class AdminSiteModelRegistration:
    """
    Registers all models of the project to admin site.

    Attributes
    ----------

    models:
        The list of models

    Methods
    -------

    get_models:
        Finds the models and stores in models list
    register_models:
        Iterates over all the models and registers all

    """

    models = set()

    def __init__(self):
        self.get_models()
        self.register_models()

    def get_models(self):
        try:
            for content_type in ContentType.objects.all():
                model = content_type.model_class()
                if model:
                    self.models.add(model)
        except:
            pass

    def register_models(self):
        for model in self.models:
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                print('%s already registered' % model.__name__)


AdminSiteModelRegistration()
