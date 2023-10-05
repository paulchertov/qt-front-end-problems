from model.view_models import PSViewModel, ViewModelField


class TestView(PSViewModel):
    name = ViewModelField()
    description = ViewModelField()


if __name__ == "__main__":
    tv = TestView()
    target_string = ""

    def repr():
        """
        Function to test update event of ViewModel
        """
        assert f"{tv.name} {tv.description}" == target_string

    tv.updated.connect(repr)

    with tv.update(silent=True):
        tv.name = "123"
        tv.description = "321"

    target_string = "321 123"
    with tv.update():
        tv.name = "321"
        tv.description = "123"

    target_string = "xxx 123"
    tv.name = "xxx"
    target_string = "xxx zzz"
    tv.description = "zzz"

    target_string = "will never be equal"
    with tv.update():
        pass
