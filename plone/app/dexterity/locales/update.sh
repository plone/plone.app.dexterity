domain=plone.app.dexterity
i18ndude rebuild-pot --pot $domain.pot --merge $domain-manual.pot --create $domain ../
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po
