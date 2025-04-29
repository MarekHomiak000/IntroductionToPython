class Scheduler:
    def __init__(self, list_of_orders):
        self.offers = list_of_orders
        self.company = None

    def set_company(self, company):
        pass

    def get_active_offers(self, day_no):
        return []

    def get_new_project(self, day_no):
        return None

    def select_employees(self, order):
        raise RuntimeError("Method not implemented here")

    def select_offer(self, offers):
        raise RuntimeError("Method not implemented here")


class FirstScheduler(Scheduler):
    def __init__(self, list_of_orders):
        super().__init__(list_of_orders)

    def select_employees(self, order):
        return []

    def select_offer(self, offers):
        return None, None


class RandomScheduler(Scheduler):
    def __init__(self, list_of_orders):
        super().__init__(list_of_orders)

    def select_employees(self, order):
        return []

    def select_offer(self, offers):
        return None, None


class GreedyScheduler(Scheduler):
    def __init__(self, list_of_orders):
        super().__init__(list_of_orders)

    def select_employees(self, order):
        return []

    def select_offer(self, offers):
        return None, None


class CheapestEmployeeScheduler(Scheduler):
    def __init__(self, list_of_orders):
        super().__init__(list_of_orders)

    def select_employees(self, order):
        return []

    def select_offer(self, offers):
        return None, None


if __name__ == '__main__':
    # you can do some independent testing here
    pass
