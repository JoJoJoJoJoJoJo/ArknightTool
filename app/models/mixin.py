

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
