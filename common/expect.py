class Expect(object):

    def __init__(self, item1: object):
        self.item1 = item1
        self.reverse = False

    def __reverse_result_if_not(self, result):
        return not result if self.reverse else result

    @property
    def not_(self):
        self.reverse = not self.reverse
        return self

    def to_be(self, item2: object):
        assert self.__reverse_result_if_not(self.item1 is item2)

        return self

    def to_be_true(self):
        self.to_be(True)

        return self

    def to_be_false(self):
        self.to_be(False)

        return self

    def to_be_none(self):
        self.to_be(None)

        return self

    def to_equals(self, item2: object):
        assert self.__reverse_result_if_not(self.item1 == item2)

        return self

    def to_be_in(self, item2: object):
        assert self.__reverse_result_if_not(self.item1 in item2)

        return self

    def to_be_contains(self, item2: object):
        assert self.__reverse_result_if_not(item2 in self.item1)

        return self


    def to_less_than(self, item2: object, allow_equal=False):
        if allow_equal:
            assert self.__reverse_result_if_not(self.item1 <= item2)
        else:
            assert self.__reverse_result_if_not(self.item1 < item2)

        return self


    def to_more_than(self, item2: object, allow_equal=False):
        if allow_equal:
            assert self.__reverse_result_if_not(self.item1 >= item2)
        else:
            assert self.__reverse_result_if_not(self.item1 > item2)

        return self

    def to_be_empty(self):
        """
        限定 item1 为 str 或 list
        """
        if isinstance(self.item1, str) or isinstance(self.item1, list):
            assert self.__reverse_result_if_not(len(self.item1) == 0)
        else:
            raise Exception("item1 is not str or list")
        return self

    def is_instance_of(self, class_type: type):
        assert self.__reverse_result_if_not(isinstance(self.item1, class_type))
        return self
