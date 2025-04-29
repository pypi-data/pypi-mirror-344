from amapy.commands import CliAction, CliOption
from amapy_core.api.repo_api import AssetAPI


class AssetVersions(CliAction):
    name = "versions"
    help_msg = "list information of the asset versions"

    def run(self, args):
        api = AssetAPI(repo=self.repo).version
        with api.environment():
            api.list_versions_summary(list_all=args.all)

    def get_options(self):
        return [
            CliOption(
                dest="all",
                help_msg="optional: list all the versions available",
                is_boolean=True
            ),
        ]
