from heaobject.root import View, Permission
from heaobject.data import DataObject
from typing import final


class SettingsObject(DataObject, View):
    def __init__(self) -> None:
        super().__init__()
        self.__user: str | None = None

    @property
    def mime_type(self) -> str:
        return 'application/x.settingsobject'

    @property
    def user(self) -> str | None:
        return self.__user

    @user.setter
    def user(self, user: str | None):
        self.__user = str(user) if user is not None else None

    @property
    def type_display_name(self) -> str:
        return "Settings Object"

    @final
    @property
    def super_admin_default_permissions(self) -> list[Permission]:
        """
        Returns the default permissions that the super admin has for this object.
        """
        return list(p for p in Permission if p is not Permission.CREATOR)
