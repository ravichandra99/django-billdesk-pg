from django.contrib import admin
from payments.models import Transaction,Amount
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Transaction)
class TxnAdmin(ImportExportModelAdmin):
    pass

@admin.register(Amount)
class AmountAdmin(ImportExportModelAdmin):
    pass
