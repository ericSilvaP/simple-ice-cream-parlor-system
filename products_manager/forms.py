from django import forms

from products.models import Category, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "quantity", "quantity_unit", "cover"]
        labels = {
            "name": "Nome",
            "price": "Preço",
            "quantity": "Quantidade",
            "category": "Categoria",
        }

    quantity_unit = forms.ChoiceField(
        label="Unidade",
        choices=(
            ("ml", "Mililitro"),
            ("g", "Grama"),
            ("kg", "Quilo"),
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Categoria",
        empty_label="Selecione uma categoria",
    )

    def clean_name(self):
        product_name = self.cleaned_data.get("name", "")
        if len(product_name) < 5:
            raise forms.ValidationError("Nome deve ter mais que 5 caracteres")
        return product_name

    def clean_price(self):
        price = self.cleaned_data.get("price", "")
        try:
            if int(price) <= 0:
                raise forms.ValidationError("Preço deve ser maior que zero")
        except ValueError:
            raise forms.ValidationError("Preço deve ser um valor numérico")

        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity", "")
        try:
            if int(quantity) <= 0:
                raise forms.ValidationError("Quantidade deve ser maior que zero")
        except ValueError:
            raise forms.ValidationError("Quantidade deve ser um valor numérico")

        return quantity

    def clean(self):
        return super().clean()
