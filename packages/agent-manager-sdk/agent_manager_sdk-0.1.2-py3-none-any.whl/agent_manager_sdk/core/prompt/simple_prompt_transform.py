import enum


class ModelMode(enum.Enum):
    COMPLETION = 'completion'
    CHAT = 'chat'

    @classmethod
    def value_of(cls, value: str) -> 'ModelMode':
        """
        Get value of given mode.

        :param value: mode value
        :return: mode
        """
        for mode in cls:
            if mode.value == value:
                return mode
        raise ValueError(f'invalid mode value {value}')