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

    # quantity = forms.FloatField(
    #     label="Quantidade",
    #     widget=forms.NumberInput(attrs={"min": 0, "step": 1}),
    # )
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
