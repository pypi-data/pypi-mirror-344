from amapy_server import models
from .readonly_admin import ReadOnlyAdminView


class AssetObjectRelationsAdmin(ReadOnlyAdminView):
    column_list = ('id',
                   'asset',
                   'object',
                   'created_at',
                   'created_by',
                   )

    def __init__(self):
        super().__init__(model=models.AssetObjectRelations)
