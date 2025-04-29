from amapy.commands import CliAction
from amapy_core.api.store_api.fetch import FetchAPI


class FetchAssetClass(CliAction):
    name = "fetch"
    help_msg = "fetches asset-classes from remote"
    requires_repo = False

    def run(self, args):
        api = FetchAPI(store=self.asset_store, repo=self.repo)
        with api.environment():
            api.fetch_classes()

    def get_options(self):
        return []
