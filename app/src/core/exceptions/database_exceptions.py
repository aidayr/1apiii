class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail
        super().__init__(detail)


class UserNotFound(BaseDatabaseException):
    pass


class UserAlreadyExists(BaseDatabaseException):
    pass


class LocationAlreadyExists(BaseDatabaseException):
    pass


class LocationNotFound(BaseDatabaseException):
    pass


class CategoryNotFoundById(BaseDatabaseException):
    _exception_text_template = "Категория с id='{id}' не найдена в БД"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)
        super().__init__(detail=self._exception_text_template)


class CategorySlugIsOccupied(BaseDatabaseException):
    _exception_text_template = "Категория с slug='{slug}' уже существует в БД"

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)
        super().__init__(detail=self._exception_text_template)


class PostNotFoundById(BaseDatabaseException):
    _exception_text_template = "Пост с id='{id}' не найден в БД"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)
        super().__init__(detail=self._exception_text_template)


class PostNotFoundByAuthor(BaseDatabaseException):
    _exception_text_template = "Пост у автора с id='{author_id}' не найден в БД"

    def __init__(self, author_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            author_id=author_id
        )
        super().__init__(detail=self._exception_text_template)


class CommentNotFoundById(BaseDatabaseException):
    _exception_text_template = "Комментарий с id='{id}' не найден в БД"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)
        super().__init__(detail=self._exception_text_template)
