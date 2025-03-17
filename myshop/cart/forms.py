from django import forms

class CartAddProductForm(forms.Form):
    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)

        if product and product.is_by_weight:
            self.min_value = 0.25
            step = 0.25
        else:
            self.min_value = 1
            step = 1
        print(self.min_value)
        self.fields['quantity'] = forms.DecimalField(
            max_value=100,
            min_value=self.min_value,
            decimal_places=2,
            max_digits=4,
            initial=self.min_value,
            widget=forms.NumberInput(attrs={'step': str(step), 'class': 'border-transparent border-b-principal border-2 font-light text-2xl w-20 text-center [&::-webkit-inner-spin-button]:appearance-none', 'id':'quantity-input'})
        )

        self.fields['override'] = forms.BooleanField(
            required=False,
            initial=False,
            widget=forms.HiddenInput
        )

        self.fields['override'] = forms.BooleanField(
            required=False,
            initial=False,
            widget=forms.HiddenInput
        )
