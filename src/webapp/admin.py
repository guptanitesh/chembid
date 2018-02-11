from django.contrib import admin
# from import_export import resources
# from tags_input import admin as tags_input_admin

if __name__ == '__main__':
    from models import *
else:
    from .models import *

# from import_export.admin import ImportExportModelAdmin



admin.site.register(Product)

admin.site.register(Mainproduct)

admin.site.register(Api)
admin.site.register(impurity)

admin.site.register(ProductAvailability)
admin.site.register(ImpurityAvailability)
