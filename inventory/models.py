from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    # TODO: image field

    price = models.DecimalField(max_digits=10, decimal_places=2)

    # is_active = models.BooleanField(default=True)
    # ...
    # is_sale_item = ....
    # barcode = ....

    def __str__(self):
        return self.title


class Category(MPTTModel):
    """
    Fields - Created At, Updated At, Title, Description, Image URL, Price, Parent
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    parent = TreeForeignKey("self", null=True, blank=True, related_name="children", db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        if self.parent:
            return "{} - {}".format(self.name, self.parent)
        else:
            return "{}".format(self.name)
            # django-mptt
