import json

from fastapi_cache import Coder, default_key_builder


class JsonCoder(Coder):
    """Кодирование и декодирование данных для кэширования."""

    @classmethod
    def encode(cls, value):
        """
        Кодирует данные для кэширования.

        Args:
            value: Данные для кодирования.

        Returns:
            Кодированные данные.
        """
        if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
            value = [cls._model_to_dict(item) for item in value]
        else:
            value = cls._model_to_dict(value)
        return json.dumps(value, default=str).encode()

    @classmethod
    def _model_to_dict(cls, model):
        """
        Конвертирует модель данных в словарь.

        Args:
            model: Модель данных.

        Returns:
            Словарь с данными модели.
        """
        if hasattr(model, "__table__"):
            return {c.name: getattr(model, c.name) for c in model.__table__.columns}
        return model

    @classmethod
    def decode(cls, value):
        """
        Декодирует данные из кэша.

        Args:
            value: Кодированные данные.

        Returns:
            Декодированные данные.
        """
        if isinstance(value, dict):
            return value
        if isinstance(value, bytes):
            return json.loads(value.decode())
        if isinstance(value, str):
            return json.loads(value)


def trading_key_builder(func, namespace="", *args, **kwargs):
    """
    Ключ для кэширования.

    Args:
        func: Функция, для которой строится ключ.
        namespace: Пространство имен для ключа.
        **kwargs: Дополнительные аргументы.

    Returns:
        Строенный ключ.
    """
    data = kwargs["kwargs"].get("data")
    limit = kwargs["kwargs"].get("limit")
    if limit:
        return default_key_builder(
            func, namespace, args=(), kwargs={"data": data, "limit": limit}
        )
    return default_key_builder(func, namespace, args=(), kwargs={"data": data})


def last_dates_key_builder(func, namespace="", *args, **kwargs):
    """
    Ключ для кэширования.

    Args:
        func: Функция, для которой строится ключ.
        namespace: Пространство имен для ключа.
        **kwargs: Дополнительные аргументы.

    Returns:
        Строенный ключ.
    """
    return default_key_builder(
        func, namespace, args=(), kwargs=kwargs["kwargs"].get("limit")
    )
