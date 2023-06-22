from indexers import AbstractIndexer


class MockValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Mock<{self.value}>'


class SimpleDictIndexer(AbstractIndexer[str, dict, MockValue]):
    def create_object(self, obj: dict) -> dict:
        return MockValue(obj["value"])

    def obtain_id(self, obj: dict) -> str:
        return obj["id"]

    def update_object(self, old_obj: dict, new_obj: dict) -> None:
        old_obj.value = new_obj["value"]


def main():
    i = SimpleDictIndexer()
    ext = {"id": "4", "value": "ext"}
    ext = i.add(ext)
    assert i["4"] is ext
    def a():
        """
        This function is used to test the scope of the indexer
        """
        temp = {"id": "1", "value": "temp"}
        obj = i.add(temp)
        print(obj.value)
        x = 12
        assert i.get("1") is obj

    a()

    assert i.get("1", None) is None
    assert i["4"] is ext

    def b():
        """
        This function is used to test the scope of the indexer
        """
        nest = {"id": "2", "value": {"12": "2"}}
        nest = i.add(nest)
        return nest.value

    x = b()
    assert i.get("2") is None
    def c():
        """
        This function is used to test the scope of the indexer
        """
        nest = {"id": "5", "value": {"12": "2"}}
        nest = i.add(nest)
        nest.value["o"] = nest
        return nest.value

    y = c()
    assert i.get("5") is not None
    new_ext = i.add({"id": "4", "value": "13"})
    assert new_ext is ext
    assert i["4"].value == "13"
    assert i["4"] is ext
    z = i.add({"id": "5", "value": 12})
    assert z is y["o"]


if __name__ == "__main__":
    main()
