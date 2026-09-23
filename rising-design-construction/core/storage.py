from django.core.files.storage import Storage, storages
from django.utils.deconstruct import deconstructible


@deconstructible
class StorageAlias(Storage):
    """Serializable proxy to a named STORAGES entry, so migrations contain no credentials."""
    def __init__(self, alias):
        self.alias = alias

    @property
    def backend(self):
        return storages[self.alias]

    def __getattr__(self, name):
        return getattr(self.backend, name)

    def _open(self, name, mode="rb"):
        return self.backend.open(name, mode)

    def _save(self, name, content):
        return self.backend.save(name, content)

    def delete(self, name):
        return self.backend.delete(name)

    def exists(self, name):
        return self.backend.exists(name)

    def listdir(self, path):
        return self.backend.listdir(path)

    def size(self, name):
        return self.backend.size(name)

    def url(self, name):
        return self.backend.url(name)

    def path(self, name):
        return self.backend.path(name)
