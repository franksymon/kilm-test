import abc

class AbstractRepository(abc.ABC):
    @abc.abstractmethod 
    def add(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, reference, page, per_page):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference, page, per_page):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, reference, fields):
        raise NotImplementedError 

    @abc.abstractmethod
    def delete(self, reference):
        raise NotImplementedError