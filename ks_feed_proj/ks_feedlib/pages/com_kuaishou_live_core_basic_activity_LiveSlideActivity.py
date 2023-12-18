# -*- coding: utf-8 -*-
import time

from uibase.upath import *
from uibase.controls import Window


class HomeActivity(Window):
    window_spec = {"path": UPath(activity_ == 'com.yxcorp.gifshow.HomeActivity')}

    def get_locators(self):
        return {
        }


