from __future__ import annotations

from abc import ABC, abstractmethod


class DigitalProduct(ABC):
    """
    Абстрактный цифровой продукт (например: подписка, пресет-пак, курс).
    """

    def __init__(self, sku: str, price: float, in_stock: int) -> None:
        """
        Args:
            sku: Уникальный артикул/код продукта (не пустой).
            price: Цена (>= 0).
            in_stock: Количество доступных единиц (>= 0).
        """
        if not isinstance(sku, str) or not sku.strip():
            raise ValueError("sku must be a non-empty string")
        if price < 0:
            raise ValueError("price must be >= 0")
        if in_stock < 0:
            raise ValueError("in_stock must be >= 0")

        self.sku: str = sku.strip()
        self.price: float = float(price)
        self.in_stock: int = int(in_stock)

    @abstractmethod
    def apply_discount(self, percent: float) -> float:
        """
        Применить скидку и вернуть новую цену (не меняя обязательно состояние объекта).

        Args:
            percent: Скидка в процентах (0..100).

        Returns:
            Новая цена.

        Examples:
            >>> class DemoProduct(DigitalProduct):
            ...     def apply_discount(self, percent: float) -> float:
            ...         if not (0 <= percent <= 100):
            ...             raise ValueError("percent must be between 0 and 100")
            ...         return round(self.price * (1 - percent / 100), 2)
            ...     def reserve(self, quantity: int) -> None:
            ...         if quantity <= 0:
            ...             raise ValueError("quantity must be > 0")
            ...         if quantity > self.in_stock:
            ...             raise ValueError("not enough stock")
            ...         self.in_stock -= quantity
            ...     def deliver(self, email: str) -> str:
            ...         if "@" not in email:
            ...             raise ValueError("invalid email")
            ...         return f"Delivered {self.sku} to {email}"
            ...
            >>> p = DemoProduct("PACK-001", 10.0, 5)
            >>> p.apply_discount(15)
            8.5
        """
        ...

    @abstractmethod
    def reserve(self, quantity: int) -> None:
        """
        Зарезервировать указанное количество (может уменьшать остаток).

        Args:
            quantity: Количество для резерва (> 0).

        Returns:
            None
        """
        ...

    @abstractmethod
    def deliver(self, email: str) -> str:
        """
        Доставить цифровой продукт на e-mail.

        Args:
            email: Почта получателя.

        Returns:
            Сообщение о доставке.
        """
        ...


class Vehicle(ABC):
    """
    Абстрактное транспортное средство.
    """

    def __init__(self, vin: str, mileage_km: float, fuel_level: float) -> None:
        """
        Args:
            vin: VIN-номер (ровно 17 символов).
            mileage_km: Пробег в км (>= 0).
            fuel_level: Уровень топлива (0..1).
        """
        if not isinstance(vin, str) or len(vin.strip()) != 17:
            raise ValueError("vin must be a string of length 17")
        if mileage_km < 0:
            raise ValueError("mileage_km must be >= 0")
        if not (0.0 <= fuel_level <= 1.0):
            raise ValueError("fuel_level must be between 0 and 1")

        self.vin: str = vin.strip()
        self.mileage_km: float = float(mileage_km)
        self.fuel_level: float = float(fuel_level)

    @abstractmethod
    def start(self) -> None:
        """
        Запустить двигатель/систему движения.

        Returns:
            None
        """
        ...

    @abstractmethod
    def drive(self, distance_km: float) -> float:
        """
        Проехать указанную дистанцию.

        Args:
            distance_km: Дистанция в км (> 0).

        Returns:
            Новый пробег (км).
        """
        ...

    @abstractmethod
    def refuel(self, amount: float) -> float:
        """
        Заправить/зарядить транспорт.

        Args:
            amount: Количество топлива/заряда (> 0).

        Returns:
            Новый fuel_level в диапазоне 0..1.

        Examples:
            >>> class DemoCar(Vehicle):
            ...     def start(self) -> None:
            ...         return None
            ...     def drive(self, distance_km: float) -> float:
            ...         if distance_km <= 0:
            ...             raise ValueError("distance_km must be > 0")
            ...         self.mileage_km += distance_km
            ...         # расход условный
            ...         self.fuel_level = max(0.0, self.fuel_level - distance_km / 1000)
            ...         return self.mileage_km
            ...     def refuel(self, amount: float) -> float:
            ...         if amount <= 0:
            ...             raise ValueError("amount must be > 0")
            ...         self.fuel_level = min(1.0, self.fuel_level + amount)
            ...         return self.fuel_level
            ...
            >>> car = DemoCar("1234567890ABCDEFG", 1000.0, 0.20)
            >>> car.refuel(0.50)
            0.7
        """
        ...


class OnlineCourse(ABC):
    """
    Абстрактный онлайн-курс.
    """

    def __init__(self, title: str, max_students: int, enrolled: int) -> None:
        """
        Args:
            title: Название (не пустое).
            max_students: Максимум студентов (> 0).
            enrolled: Текущее число записанных (0..max_students).
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if max_students <= 0:
            raise ValueError("max_students must be > 0")
        if not (0 <= enrolled <= max_students):
            raise ValueError("enrolled must be between 0 and max_students")

        self.title: str = title.strip()
        self.max_students: int = int(max_students)
        self.enrolled: int = int(enrolled)

    @abstractmethod
    def enroll(self, student_name: str) -> bool:
        """
        Записать студента на курс.

        Args:
            student_name: Имя студента (не пустое).

        Returns:
            True если запись успешна, иначе False.
        """
        ...

    @abstractmethod
    def unenroll(self, student_name: str) -> bool:
        """
        Отписать студента от курса.

        Args:
            student_name: Имя студента (не пустое).

        Returns:
            True если отписали, иначе False.
        """
        ...

    @abstractmethod
    def completion_percent(self, student_name: str) -> float:
        """
        Вернуть прогресс студента в процентах (0..100).

        Args:
            student_name: Имя студента.

        Returns:
            Прогресс в процентах.

        Examples:
            >>> class DemoCourse(OnlineCourse):
            ...     def __init__(self, title: str, max_students: int, enrolled: int) -> None:
            ...         super().__init__(title, max_students, enrolled)
            ...         self._progress: dict[str, float] = {}
            ...     def enroll(self, student_name: str) -> bool:
            ...         if not student_name.strip():
            ...             raise ValueError("student_name must be non-empty")
            ...         if self.enrolled >= self.max_students:
            ...             return False
            ...         self.enrolled += 1
            ...         self._progress[student_name] = 0.0
            ...         return True
            ...     def unenroll(self, student_name: str) -> bool:
            ...         if student_name in self._progress:
            ...             del self._progress[student_name]
            ...             self.enrolled = max(0, self.enrolled - 1)
            ...             return True
            ...         return False
            ...     def completion_percent(self, student_name: str) -> float:
            ...         return float(self._progress.get(student_name, 0.0))
            ...
            >>> c = DemoCourse("Python OOP", 2, 0)
            >>> c.enroll("Amina")
            True
            >>> c.completion_percent("Amina")
            0.0
        """
        ...


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
# TODO Написать 3 класса с документацией и аннотацией типов

if __name__ == "__main__":
    # TODO работоспособность экземпляров класса проверить с помощью doctest
    pass
