
import pytest

class NotInRange(Exception):
    def __init__(self, message="value not in range"):        
        self.message = message
        super().__init__(self.message)

# for pytest to recognize start methods with test_

    def test_generic():
        # assertion will always be true, if test case pass
        a = 5
        with pytest.raises(NotInRange):
            if a not in range(10,20):
                raise NotInRange
        