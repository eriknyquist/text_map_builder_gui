from collections import OrderedDict

from PyQt5 import QtWidgets, QtCore, QtGui

from text_game_map_maker.utils import yesNoDialog
from text_game_map_maker.constants import available_item_sizes
from text_game_map_maker.qt_auto_form import QtAutoForm

from text_game_maker.materials import materials
from text_game_maker.game_objects.items import (
    Item, Food, ItemSize, Flashlight, Battery, Coins, PaperBag, SmallBag, Bag,
    LargeBag, SmallTin, Lighter, BoxOfMatches, Lockpick, StrongLockpick
)


# ----- QtAutoForm subclasses -----

class ItemEditorAutoForm(QtAutoForm):
    def getAttribute(self, attrname):
        if attrname == 'size':
            val = getattr(self.instance, attrname)
            for s in available_item_sizes:
                if getattr(ItemSize, s) == val:
                    return s

        return getattr(self.instance, attrname)

    def setAttribute(self, attrname, value):
        if attrname == 'size':
            setattr(self.instance, attrname, getattr(ItemSize, value))
            return

        setattr(self.instance, attrname, value)


class ContainerItemEditorAutoForm(ItemEditorAutoForm):
    def __init__(self, *args, **kwargs):
        QtAutoForm.__init__(self, *args, **kwargs, extra_button=True,
                            extra_button_text="contained items...")

    def extraButtonClicked(self):
        dialog = ContainerItemBrowser(self, self.instance)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()


class ObjectBuilder(object):
    objtype = None
    spec = None

    def __init__(self):
        self.title = "%s editor" % self.__class__.objtype.__name__
        self.formTitle = ""
        self.desc = ''.join(self.__class__.objtype.__doc__.strip().split('\n'))

    def build_instance(self, formclass=ContainerItemEditorAutoForm):
        ins = self.__class__.objtype()
        print(self.__class__.objtype.__doc__)
        dialog = formclass(ins, title=self.title, formTitle=self.formTitle,
                           headerText=self.desc, scrollable=True, spec=self.__class__.spec)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()
        if not dialog.wasAccepted():
            return None

        self.process_dialog_settings(ins)
        return ins

    def edit_instance(self, ins, formclass=ContainerItemEditorAutoForm):
        dialog = formclass(ins, title=self.title, formTitle=self.formTitle,
                           headerText=self.desc, scrollable=True, spec=self.__class__.spec)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec_()
        self.process_dialog_settings(ins)
        return dialog.wasAccepted()

    def process_dialog_settings(self, ins):
        """
        Can be overridden by subclasses to transform any values set in the
        object editor dialog if needed
        """
        pass


# ----- ObjectBuilder subclasses -----

class ItemBuilder(ObjectBuilder):
    objtype = Item
    spec = OrderedDict([
        ("material", {"type": "choice", "choices": materials.get_materials(),
                      "tooltip": "Set this object's material type"}),
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("edible", {"type": "bool", "tooltip": "defines whether player can eat "
                                               "this item without taking damage"}),

        ("combustible", {"type": "bool", "tooltip": "defines whether this item "
                                                    "will burn"}),

        ("energy", {"type": "int", "tooltip": "defines health gained by player "
                            "from eating this item (if edible)"}),

        ("damage", {"type": "int", "tooltip": "defines health lost by player "
                                              "if damaged by this item"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])

class FlashlightBuilder(ObjectBuilder):
    objtype = Flashlight
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("damage", {"type": "int", "tooltip": "defines health lost by player "
                                              "if damaged by this item"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("fuel_decrement", {"type": "float", "label": "fuel decrement",
                      "tooltip": "defines how much fuel is lost per item use"}),

        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])


class BatteryBuilder(ObjectBuilder):
    objtype = Battery
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("fuel", {"type": "float", "tooltip": "current fuel level"})
    ])


class LighterBuilder(ObjectBuilder):
    objtype = Lighter
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("max_fuel", {"type": "float", "label": "Max. fuel",
                      "tooltip": "defines maximum possible fuel level value"}),

        ("fuel_decrement", {"type": "float", "label": "fuel decrement",
                      "tooltip": "defines how much fuel is lost per item use"}),

        ("fuel", {"type": "float", "tooltip": "current fuel level"})
    ])


class BoxOfMatchesBuilder(ObjectBuilder):
    objtype = BoxOfMatches
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("max_fuel", {"type": "float", "label": "Max. fuel",
                      "tooltip": "defines maximum possible fuel level value"}),

        ("fuel_decrement", {"type": "float", "label": "fuel decrement",
                      "tooltip": "defines how much fuel is lost per item use"}),

        ("fuel", {"type": "float", "tooltip": "current fuel level"})
    ])


class LockpickBuilder(ObjectBuilder):
    objtype = Lockpick
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("uses", {"type": "int", "tooltip": "number of times lockpick can be "
                                            "used before breaking"})
    ])


class StrongLockpickBuilder(ObjectBuilder):
    objtype = StrongLockpick
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                                              "the name of this object, usually 'a' "
                                              "or 'an' (e.g. 'a' sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                                            "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),

        ("uses", {"type": "int", "tooltip": "number of times lockpick can be "
                                            "used before breaking"})
    ])


class CoinsBuilder(ObjectBuilder):
    objtype = Coins
    spec = OrderedDict([
        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),
    ])


class PaperBagBuilder(ObjectBuilder):
    objtype = PaperBag
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                    "the name of this object, usually 'a' or 'an' (e.g. 'a' "
                    "sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                  "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),
    ])


class SmallBagBuilder(ObjectBuilder):
    objtype = SmallBag
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                    "the name of this object, usually 'a' or 'an' (e.g. 'a' "
                    "sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                  "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),
        ("capacity", {"type": "int", "tooltip": "defines number of items this bag "
                                                "can hold"}),
        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])


class SmallTinBuilder(ObjectBuilder):
    objtype = SmallTin
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                    "the name of this object, usually 'a' or 'an' (e.g. 'a' "
                    "sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                  "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),
        ("capacity", {"type": "int", "tooltip": "defines number of items this bag "
                                                "can hold"}),
        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])


class BagBuilder(ObjectBuilder):
    objtype = Bag
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                    "the name of this object, usually 'a' or 'an' (e.g. 'a' "
                    "sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                  "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),
        ("capacity", {"type": "int", "tooltip": "defines number of items this bag "
                                                "can hold"}),
        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])


class LargeBagBuilder(ObjectBuilder):
    objtype = LargeBag
    spec = OrderedDict([
        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                    "the name of this object, usually 'a' or 'an' (e.g. 'a' "
                    "sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                  "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                                                "'on the floor' or 'hanging from the wall'"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                                             "from selling this item"}),
        ("capacity", {"type": "int", "tooltip": "defines number of items this bag "
                                                "can hold"}),
        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])


class FoodBuilder(ObjectBuilder):
    objtype = Food
    spec = OrderedDict([
        ("material", {"type": "choice", "choices": materials.get_materials(),
                      "tooltip": "Set this object's material type"}),

        ("prefix", {"type": "str", "tooltip": "Set the word that should precede "
                    "the name of this object, usually 'a' or 'an' (e.g. 'a' "
                    "sandwich, 'an' apple)"}),

        ("name", {"type": "str", "tooltip": "name of this object, e.g. "
                  "'sandwich' or 'apple'"}),

        ("location", {"type": "str", "tooltip": "location of object, e.g. "
                      "'on the floor' or 'hanging from the wall'"}),

        ("combustible", {"type": "bool", "tooltip": "defines whether this item "
                         "will burn"}),

        ("energy", {"type": "int", "tooltip": "defines health gained by player "
                            "from eating this item (if edible)"}),

        ("value", {"type": "int", "tooltip": "defines coins gained by player "
                            "from selling this item"}),

        ("size", {"type": "choice", "choices": available_item_sizes,
                  "tooltip": "defines size class for this item. "
                             "items cannot contain items of a larger size class."})
    ])


class ItemBrowser(QtWidgets.QDialog):
    """
    Abstract implementation of class to browse items contained within another item
    """

    def __init__(self, parent, container):
        super(ItemBrowser, self).__init__(parent=parent)

        self.parent = parent
        self.container = container
        self.row_items = []

        self.classobjs = [
            FoodBuilder,
            ItemBuilder,
            FlashlightBuilder,
            BatteryBuilder,
            CoinsBuilder,
            PaperBagBuilder,
            SmallBagBuilder,
            BagBuilder,
            LargeBagBuilder,
            SmallTinBuilder,
            LighterBuilder,
            BoxOfMatchesBuilder,
            LockpickBuilder,
            StrongLockpickBuilder
        ]

        self.builders = {c.objtype.__name__: c() for c in self.classobjs}

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(['item type', 'item name', 'location'])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.populateTable()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        buttonBox = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.addButton = QtWidgets.QPushButton()
        self.editButton = QtWidgets.QPushButton()
        self.deleteButton = QtWidgets.QPushButton()
        self.addButton.setText("Add item")
        self.editButton.setText("Edit item")
        self.deleteButton.setText("Delete item")

        self.editButton.clicked.connect(self.editButtonClicked)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addWidget(self.deleteButton)
        self.buttonGroupBox = QtWidgets.QGroupBox("")
        self.buttonGroupBox.setLayout(buttonLayout)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.buttonGroupBox)
        mainLayout.addWidget(self.table)
        mainLayout.addWidget(buttonBox)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)

        self.setLayout(mainLayout)
        self.setWindowTitle("Item Editor")

    def sizeHint(self):
        return QtCore.QSize(500, 400)

    def addButtonClicked(self):
        item, accepted = QtWidgets.QInputDialog.getItem(self,
                                                        "select object type",
                                                        "Select an object type",
                                                        self.builders.keys(),
                                                        0, False)
        if not accepted:
            return

        builder = self.builders[item]
        instance = builder.build_instance()
        if not instance:
            return

        self.addRow(instance)
        self.row_items.append(instance)
        self.addItemToContainer(instance)

    def editButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            return

        item = self.row_items[selectedRow]
        classname = item.__class__.__name__
        builder = self.builders[classname]

        if not builder.edit_instance(item):
            return

        # Re-draw door browser table
        self.populateTable()

    def deleteButtonClicked(self):
        selectedRow = self.table.currentRow()
        if selectedRow < 0:
            return

        item = self.row_items[selectedRow]

        reply = yesNoDialog(self, "Really delete item?",
                            "Are you sure you want do delete this item (%s)?" % item.name)
        if not reply:
            return

        item.delete()
        self.table.removeRow(selectedRow)

    def addRow(self, item):
        nextFreeRow = self.table.rowCount()
        self.table.insertRow(nextFreeRow)

        clsname, name, loc = self.getRowInfo(item)
        item1 = QtWidgets.QTableWidgetItem(clsname)
        item2 = QtWidgets.QTableWidgetItem(name)
        item3 = QtWidgets.QTableWidgetItem(loc)

        self.table.setItem(nextFreeRow, 0, item1)
        self.table.setItem(nextFreeRow, 1, item2)
        self.table.setItem(nextFreeRow, 2, item3)

    def getRowInfo(self, item):
        raise NotImplementedError()

    def addItemToContainer(self, item):
        raise NotImplementedError()

    def populateTable(self):
        raise NotImplementedError()


# ----- ItemBrowser subclasses -----

class TileItemBrowser(ItemBrowser):
    """
    Concrete item browser implementation to browse items contained in a Tile object
    """

    def populateTable(self):
        self.row_items = []

        self.table.setRowCount(0)
        for loc in self.container.items:
            for item in self.container.items[loc]:
                self.addRow(item)
                self.row_items.append(item)

    def addItemToContainer(self, item):
        self.container.add_item(item)

    def getRowInfo(self, item):
        return item.__class__.__name__, item.name, item.location


class ContainerItemBrowser(ItemBrowser):
    """
    Concrete item browser implementation to browse items contained in another item
    """

    def populateTable(self):
        self.row_items = []

        self.table.setRowCount(0)
        for item in self.container.items:
            self.addRow(item)
            self.row_items.append(item)

    def addItemToContainer(self, item):
        self.container.add_item(item)

    def getRowInfo(self, item):
        loc = 'inside %s' % self.container.__class__.__name__
        return item.__class__.__name__, item.name, loc
