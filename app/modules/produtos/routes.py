from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_database_session
from app.modules.produtos.schemas import (
    ProdutoCreate, ProdutoUpdate, ProdutoResponse,
    ParametroCreate, ParametroUpdate, ParametroResponse,
)
from app.modules.produtos.service import ProdutoService, ParametroProdutoService

router = APIRouter(prefix="/api/v1/produtos", tags=["Produtos"])


@router.post("", response_model=ProdutoResponse, status_code=201)
def create(data: ProdutoCreate, db: Session = Depends(get_database_session)):
    return ProdutoService(db).create(data)


@router.get("", response_model=list[ProdutoResponse])
def products(ativo: bool | None = None, limit: int = Query(50, ge=1, le=100),
             offset: int = Query(0, ge=0), db: Session = Depends(get_database_session)):
    return ProdutoService(db).list({"ativo": ativo}, limit, offset)


@router.get("/{produto_id}", response_model=ProdutoResponse)
def get(produto_id: UUID, db: Session = Depends(get_database_session)):
    return ProdutoService(db).get(produto_id)


@router.patch("/{produto_id}", response_model=ProdutoResponse)
def update(produto_id: UUID, data: ProdutoUpdate, db: Session = Depends(get_database_session)):
    return ProdutoService(db).update(produto_id, data)


@router.post("/{produto_id}/parametros", response_model=ParametroResponse, status_code=201)
def create_parameter(produto_id: UUID, data: ParametroCreate, db: Session = Depends(get_database_session)):
    return ParametroProdutoService(db).create(data, produto_id=produto_id)


@router.get("/{produto_id}/parametros", response_model=list[ParametroResponse])
def parameters(produto_id: UUID, limit: int = Query(50, ge=1, le=100),
               offset: int = Query(0, ge=0), db: Session = Depends(get_database_session)):
    return ParametroProdutoService(db).list_for_product(produto_id, limit, offset)


@router.patch("/{produto_id}/parametros/{parametro_id}", response_model=ParametroResponse)
def update_parameter(produto_id: UUID, parametro_id: UUID, data: ParametroUpdate,
                     db: Session = Depends(get_database_session)):
    return ParametroProdutoService(db).update_for_product(produto_id, parametro_id, data)
