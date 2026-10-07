from fastapi import HTTPException

from app.repositories.produtos import ProdutoRepository, ParametroProdutoRepository
from app.services.operacional import CrudService, invalid


class ProdutoService(CrudService):
    repository = ProdutoRepository


class ParametroProdutoService(CrudService):
    repository = ParametroProdutoRepository

    def validate(self, values, previous=None, changed=None):
        ProdutoService(self.db).get(values["produto_id"])
        minimum, maximum = values.get("valor_minimo"), values.get("valor_maximo")
        if minimum is not None and maximum is not None and minimum > maximum:
            invalid("valor_minimo deve ser menor ou igual a valor_maximo.")

    def get_for_product(self, product_id, parameter_id):
        ProdutoService(self.db).get(product_id)
        parameter = self.get(parameter_id)
        if parameter.produto_id != product_id:
            raise HTTPException(404, "Parametro nao pertence ao produto.")
        return parameter

    def list_for_product(self, product_id, limit, offset):
        ProdutoService(self.db).get(product_id)
        return self.list({"produto_id": product_id}, limit, offset)

    def update_for_product(self, product_id, parameter_id, data):
        self.get_for_product(product_id, parameter_id)
        return self.update(parameter_id, data)
