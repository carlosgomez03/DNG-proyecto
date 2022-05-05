from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class OrderCreateForm(FlaskForm):
    buyer = StringField("Comprador",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
        render_kw={"placeholder": "Comprador"},
    )

    provider = StringField("Vendedor",
        validators=[
            InputRequired(),
            Length(min=3, max=20),
        ],
        render_kw={"placeholder": "Vendedor"},
    )

    discount = IntegerField("Descuento",
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "discount"},
    )

    tax = IntegerField("Impuesto",
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "impuesto"},
    )

    submit = SubmitField("Crear")
