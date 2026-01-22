from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
#from .models import Customer, Delivery, Order


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')

#admin.site.register(Book, BookAdmin)
#admin.site.register(Customer)
#admin.site.register(Delivery)
#admin.site.register(Order)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("date_of_birth", "profile_photo"),
        }),
    )

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
        "date_of_birth",
    )

    search_fields = ("username", "email")