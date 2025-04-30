from amapy_server import models
from .readonly_admin import ReadOnlyAdminView


class AssetRefAdmin(ReadOnlyAdminView):
    column_list = ('id',
                   'src_version',
                   'dst_version',
                   'label',
                   'properties',
                   'created_at',
                   'created_by',
                   )
    column_searchable_list = ['label']

    def __init__(self):
        super(AssetRefAdmin, self).__init__(model=models.AssetRef)
