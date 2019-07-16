from wtforms.fields import Field
from wtforms.widgets import Select


class Many2manyField(Field):
    widget = Select(multiple=True)

    def __init__(self, label, model, validators=None, **kwargs):
        self.model = model
        # fixme
        self.available_records = self.model.query.all()
        super(Many2manyField, self).__init__(label=label, validators=validators, **kwargs)

    def iter_choices(self):
        for record in self.available_records:
            selected = self.data is not None and record in self.data
            yield (record, record.name, selected)

    def _value(self):
        return (self._name_to_obj(name) for name in self.data)

    def _name_to_obj(self, name):
        return self.model.query.filter_by(name=name).first()

    def process_data(self, value):
        try:
            self.data = list(self._name_to_obj(v) for v in value)
        except (ValueError, TypeError):
            self.data = None

    def process_formdata(self, valuelist):
        # TODO: check why valuelist is [tag(3): t2]
        self.data = list(self._name_to_obj(x.split(':')[-1].strip()) for x in valuelist)
        if not all(self.data):
            raise ValueError(self.gettext('Invalid choice(s): one or more data inputs could not be coerced'))

    def pre_validate(self, form):
        if self.data:
            for d in self.data:
                if not d:
                    raise ValueError(self.gettext("'%(value)s' is not a valid choice for this field") % dict(value=d))
