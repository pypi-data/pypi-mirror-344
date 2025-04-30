# Django Annotated Property

Decorator for Django model properties that returns annotated values when available, 
avoiding database queries (f.e. O(N) vs O(1) for N items).

If a queryset includes `annotated_<property>`, the decorator uses it instead of calling the original method.


## Example

```python
from django.db import models
from django_annotated_property.annotated_property import annotated_property

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @annotated_property
    def total_price(self):
        return self.product.price * self.quantity
```

now you can use the `total_price` property in your views or templates:

```python
items = (
    OrderItem.objects
    .annotate(annotated_total_price=models.F('product__price') * models.F('quantity'))
)
for item in items:
    print(item.total_price)  # returns annotated_total_price instead of the original method
```

## TODO

- [ ] Add tests