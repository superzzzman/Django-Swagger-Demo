from django.db import models


class UncheckUniqueForeignKey(models.ForeignKey):

    def _check_unique_target(self):
        return []
