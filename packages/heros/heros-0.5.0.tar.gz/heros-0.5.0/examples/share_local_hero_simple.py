import time
from heros import LocalHERO


class TestObject(LocalHERO):

    testme: int = 0

    def read_temp(self, min: int, max: int) -> float:
        return (max + min) / 2

    def hello(self) -> str:
        self.testme += 1
        return "world"


with TestObject("my_hero") as obj:

    # keep running with infinite loop
    while True:
        time.sleep(1)
