from amapy.commands import CliAction
from amapy_core.api.repo_api import AssetAPI
from amapy_utils.common import exceptions
from amapy_utils.utils.log_utils import LogColors


class AssetTree(CliAction):
    name = "tree"
    help_msg = "displays information in the asset"
    requires_repo = True

    def run(self, args):
        api = AssetAPI(repo=self.repo).info
        if not api:
            return
        try:
            with api.environment():
                api.asset_tree()
        except exceptions.AssetException as e:
            self.user_log.message(e.msg, color=LogColors.ERROR)

    def get_options(self):
        return []
