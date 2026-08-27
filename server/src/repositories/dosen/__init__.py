from server.src.repositories.dosen.dosen_repository import (
    DosenRepositoryInterface,
    BaseDosenRepository,
    SQLDosenRepository,
    MySQLDosenRepository,
    ExcelDosenRepository,
    CompositeDosenRepository,
)

__all__ = [
    "DosenRepositoryInterface",
    "BaseDosenRepository",
    "SQLDosenRepository",
    "MySQLDosenRepository",
    "ExcelDosenRepository",
    "CompositeDosenRepository",
]
