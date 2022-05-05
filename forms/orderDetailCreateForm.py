from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class OrderDetailCreateForm(FlaskForm):
    orderId = IntegerField(
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "Id de orden..."},
    )

    description = StringField(
        validators=[
            InputRequired(),
            Length(min=1, max=50),
        ],
        render_kw={"placeholder": "Description..."},
    )
    
    quantity = IntegerField(
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "Cantidad..."},
    )

    unitCost = IntegerField(
        validators=[
            InputRequired(),
        ],
        render_kw={"placeholder": "Costo unitario..."},
    )

    submit = SubmitField("Crear")