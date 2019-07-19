from .. import db


class ModelMixin:

    @classmethod
    def browse(cls, id):
        if not hasattr(cls, 'query'):
            raise NotImplementedError('Mixin not implemented in a model')
        return cls.query.filter_by(id=id).first()

    @classmethod
    def browse_all(cls, ids):
        if not hasattr(cls, 'query'):
            raise NotImplementedError('Mixin not implemented in a model')
        if not isinstance(ids, list):
            ids = list(ids)
        return cls.query.filter(cls.id.in_(ids)).all()

    @classmethod
    def name_get(cls, name):
        if not hasattr(cls, 'query'):
            raise NotImplementedError('Mixin not implemented in a model')
        return cls.query.filter_by(name=name).first()

    def __lt__(self, other):
        if not isinstance(other, db.Model):
            raise TypeError('Cannot compare the provided data type')
        return self.id < other.id
