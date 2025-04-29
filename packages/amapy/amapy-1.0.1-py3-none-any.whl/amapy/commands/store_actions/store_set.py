from amapy.commands import CliAction, CliOption
from amapy_core.api.settings_api import SettingsAPI
from amapy_utils.common.user_commands import UserCommands
from amapy_utils.utils.log_utils import LogColors


class StoreSet(CliAction):
    name = "set"
    help_msg = "sets asset home"
    requires_store = False
    requires_repo = False

    def run(self, args):
        if args.target:
            SettingsAPI().set_asset_home(dst_dir=args.target)
        else:
            self.user_log.message("missing required parameter target-dir", LogColors.ERROR)
            self.user_log.message(f"to set asset home: {UserCommands().set_asset_store()}")

    def get_options(self):
        return [
            CliOption(
                dest="target",
                help_msg="destination directory",
                positional=True
            ),
        ]
