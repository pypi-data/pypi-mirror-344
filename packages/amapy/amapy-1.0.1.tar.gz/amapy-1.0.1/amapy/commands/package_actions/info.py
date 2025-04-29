from amapy.commands import CliAction


class PackageInfo(CliAction):
    name = "info"
    help_msg = "displays information about asset package"
    requires_repo = False
    requires_auth = False
    requires_store = False

    def run(self, args):
        self.user_log.message("asset-manager")

    def get_options(self):
        return []
