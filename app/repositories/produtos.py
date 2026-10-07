from app.models.produto import Produto, ParametroProduto
from app.repositories.operacional import Repository


class ProdutoRepository(Repository):
    model = Produto


class ParametroProdutoRepository(Repository):
    model = ParametroProduto
