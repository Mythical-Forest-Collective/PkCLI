from collections import UserList
from functools import partial
from types import NoneType
from typing import List, Callable, Any

from pluralkit import Client, Unauthorized as UnauthorisedAccess

from menubuilder import menu, Options


# A single page to allow information to be stored easily
class Page:
    def __init__(self, choices: List[Any], navigationKeys: bool=False):
        self.choices = choices
        self.navigationKeys = navigationKeys
        self.pageNumber = -1
        self.title = ""

    def display(self, parentPageList):
        return menu(
            f"{parentPageList.title} ({self.pageNumber}/{len(parentPageList)})",
            self.choices,
            self.navigationKeys
        )


# Multiple pages grouped together, just has a few helper methods
class Pages(UserList):
    def __init__(self, *args: List[Page]):
        UserList.__init__(self, *args)
        self.title = ""

        self._numberPages()

    def _numberPages(self):
        pageNum = 0
        while pageNum < len(self.data):
            self.data[pageNum].pageNumber = pageNum + 1
            self.data[pageNum].title = self.title
            pageNum += 1

    def call(self, callback: Callable[[int, int], NoneType]):
        self._numberPages()
        result = self.data[0].display(self)

        print(result)


    @property
    def page_count(self) -> int:
        return len(self.data)


# The base menu we should inherit from
class MenuBase:
    def __init__(self, client: Client):
        self.client: Client = client
        self.pages: Pages = Pages()

    def display(self): pass

    def _build_menu(self): pass


# The member editor menu
class MemberEditorMenu(MenuBase):
    def __init__(self, client: Client):
        super().__init__(client)
        self.members2DArray = []

    def _build_menu(self):
        self.members2DArray = []

        pages = []
        members = [_ for _ in self.client.get_members()]
        membersInPage = []
        amount_of_choices = 0

        # Build the basic page info
        for member in members:
            amount_of_choices += 1
            if amount_of_choices == 17:
                amount_of_choices = 0
                pages.append([len(pages)+1, membersInPage, True])
                pages.append(Page(membersInPage, navigationKeys=True))
                self.members2DArray.append(membersInPage)
                membersInPage = []

            membersInPage.append(member)

        self.pages.data = pages
        self.pages._numberPages()


# The main menu for managing the system
class MainMenu(MenuBase):
    def __init__(self, client: Client):
        super().__init__(client)
        self._build_menu()

    def _build_menu(self):
        pages = []

        self.pages.data = pages
        self.pages._numberPages()

    @staticmethod
    def callback(pageNum:int, option:int):
        pass
