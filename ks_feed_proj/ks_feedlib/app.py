# -*- coding: utf-8 -*-
# 2023/11/30 auto generated by ShootsIDE
# MODIFY SHOULD BE CAREFULLY

from shoots_android.androidapp import AccessibilityApp
from shoots_android_byted import AndroidAppMixin


class KsFeedApp(AndroidAppMixin, AccessibilityApp):
    app_spec = {
        "package_name": "com.smile.gifmaker",
        "package_names": ["com.smile.gifmaker"],  # app multiple package name, find installed package from left to right
        "init_device": True,  # whether to wake up device
        "process_name": "",  # main process name of app
        "start_activity": "",  # leave it empty to be detected automatically
        "grant_all_permissions": True,  # grant all permissions before starting app
        "clear_data": False,  # pm clear app data
        "kill_process": False  # whether to kill previously started app
    }
    popup_rules = [ ]

    def before_launch_app(self):
        self.disable_sso_auth()

