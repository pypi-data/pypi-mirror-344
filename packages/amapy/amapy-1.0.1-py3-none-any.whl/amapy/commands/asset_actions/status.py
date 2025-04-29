from amapy.commands import CliAction
from amapy_core.api.repo_api import AssetAPI


class AssetStatus(CliAction):
    name = "status"
    help_msg = "display current status of the asset including uncommitted changes"
    requires_repo = True

    def run(self, args):
        api = AssetAPI(self.repo).status
        if api:
            with api.environment():
                api.display_status()

    def get_options(self):
        return []
