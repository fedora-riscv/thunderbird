pref("app.update.enabled", false);
pref("app.update.autoInstallEnabled", false);
# Allow users to set custom colors
# pref("browser.display.use_system_colors",   true);
pref("general.useragent.vendor", "Fedora");
pref("general.useragent.vendorSub", "THUNDERBIRD_RPM_VR");
pref("intl.locale.matchOS", true);
pref("mail.shell.checkDefaultClient", false);
pref("toolkit.networkmanager.disable", false);
pref("offline.autoDetect", true);

# Disable global indexing by default
pref("mailnews.database.global.indexer.enabled", false);

# Do not switch to Smart Folders after upgrade to 3.0b4
pref("mail.folder.views.version", "1")
pref("extensions.shownSelectionUI", true);
pref("extensions.autoDisableScope", 0);

# For rhbz#1024232
pref("ui.SpellCheckerUnderlineStyle",       1);

/* Workaround for rhbz#1134876 */
pref("javascript.options.baselinejit",      false);
/* Workaround for rhbz#1110291 */
pref("network.negotiate-auth.allow-insecure-ntlm-v1", true);
/* Workaround for mozbz#1063315 */
pref("security.use_mozillapkix_verification", false);
