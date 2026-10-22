use base::config::keys;
use hbb_common::config;

/// HVN Remote Hub always connects through HVN Connect, HVN GROUP's own
/// ID/relay server. A build may point at another server for testing.
const RENDEZVOUS_SERVER: &str = match option_env!("HVN_RENDEZVOUS_SERVER") {
    Some(server) => server,
    None => "connect.hvn.vn",
};

/// The server's public key (`id_ed25519.pub`). It is not secret, but it only
/// exists once the server is deployed, so release builds pass it in.
const RS_PUB_KEY: Option<&str> = option_env!("HVN_RS_PUB_KEY");

/// RustDesk's macOS install, uninstall and update scripts put the app name
/// into paths, launchd labels and process names unquoted, so the internal
/// name has no spaces. Users see `DISPLAY_NAME`.
const APP_NAME: &str = "HVNRemoteHub";
const DISPLAY_NAME: &str = "HVN Remote Hub";

/// HVN Remote Hub speaks Vietnamese unless the user picks another language.
const LANGUAGE: &str = "vi";

/// The version users see. `crate::VERSION` stays the RustDesk version this
/// fork is built from, because peers and the server compare it to decide which
/// protocol features the other side has.
pub const VERSION: &str = "2.0.0";

/// Runs after `load_custom_client`, so HVN's server wins over any other
/// configuration and the user cannot point the app elsewhere.
pub fn apply() {
    // Tests share one process, and other tests expect the stock app name.
    #[cfg(not(test))]
    {
        *config::APP_NAME.write().unwrap() = APP_NAME.to_owned();
    }
    // A default rather than an override: users can still pick another language.
    config::DEFAULT_LOCAL_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_LANGUAGE.to_owned(), LANGUAGE.to_owned());
    let mut settings = config::OVERWRITE_SETTINGS.write().unwrap();
    settings.insert(
        keys::OPTION_CUSTOM_RENDEZVOUS_SERVER.to_owned(),
        RENDEZVOUS_SERVER.to_owned(),
    );
    if let Some(key) = RS_PUB_KEY.filter(|key| !key.is_empty()) {
        settings.insert(keys::OPTION_KEY.to_owned(), key.to_owned());
    }
}

/// The name shown to users. `get_app_name()` keeps the internal name, which
/// paths, the URL scheme and the macOS scripts depend on.
pub fn display_name() -> String {
    display_name_of(crate::get_app_name())
}

fn display_name_of(app_name: String) -> String {
    if app_name == APP_NAME {
        DISPLAY_NAME.to_owned()
    } else {
        app_name
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use hbb_common::config::Config;

    #[test]
    fn hvn_connect_is_the_rendezvous_server() {
        apply();
        assert_eq!(
            Config::get_option(keys::OPTION_CUSTOM_RENDEZVOUS_SERVER),
            RENDEZVOUS_SERVER
        );
        assert!(Config::get_rendezvous_server().starts_with(RENDEZVOUS_SERVER));
    }

    #[test]
    fn vietnamese_is_the_default_language() {
        apply();
        assert_eq!(
            crate::lang::translate_locale("Settings".to_owned(), "en-US"),
            "Cài đặt"
        );
    }

    #[test]
    fn packages_carry_the_hvn_version() {
        // Line by line, because Windows checkouts may use CRLF.
        let has_line = |text: &str, line: String| text.lines().any(|l| l.trim_end() == line);
        let pubspec = include_str!("../flutter/pubspec.yaml");
        assert!(pubspec
            .lines()
            .any(|l| l.starts_with(&format!("version: {VERSION}+"))));
        let workflow = include_str!("../.github/workflows/flutter-build.yml");
        assert!(has_line(workflow, format!("  VERSION: \"{VERSION}\"")));
        for spec in [
            include_str!("../res/rpm-flutter.spec"),
            include_str!("../res/rpm-flutter-suse.spec"),
        ] {
            assert!(has_line(spec, format!("Version:    {VERSION}")));
        }
        assert!(has_line(
            include_str!("../res/PKGBUILD"),
            format!("pkgver={VERSION}")
        ));
        for appimage in [
            include_str!("../appimage/AppImageBuilder-x86_64.yml"),
            include_str!("../appimage/AppImageBuilder-aarch64.yml"),
        ] {
            assert!(has_line(appimage, format!("    version: {VERSION}")));
        }
        assert!(has_line(
            include_str!("../libs/portable/Cargo.toml"),
            format!("version = \"{VERSION}\"")
        ));
    }

    #[test]
    fn users_see_hvn_remote_hub() {
        assert_eq!(display_name_of(APP_NAME.to_owned()), "HVN Remote Hub");
        assert_eq!(display_name_of("RustDesk".to_owned()), "RustDesk");
    }
}
