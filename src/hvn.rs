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

/// Runs after `load_custom_client`, so HVN's server wins over any other
/// configuration and the user cannot point the app elsewhere.
pub fn apply() {
    let mut settings = config::OVERWRITE_SETTINGS.write().unwrap();
    settings.insert(
        keys::OPTION_CUSTOM_RENDEZVOUS_SERVER.to_owned(),
        RENDEZVOUS_SERVER.to_owned(),
    );
    if let Some(key) = RS_PUB_KEY.filter(|key| !key.is_empty()) {
        settings.insert(keys::OPTION_KEY.to_owned(), key.to_owned());
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
}
