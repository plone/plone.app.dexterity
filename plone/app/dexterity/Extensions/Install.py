def beforeUninstall(self, reinstall, product, cascade):
    cascade.remove('utilities')
    return None, cascade