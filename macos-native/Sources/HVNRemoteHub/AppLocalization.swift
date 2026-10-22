import AppKit
import Foundation
import SwiftUI

/// The interface language. Vietnamese by default; English or the system
/// language on request. SwiftUI text and `L(_:)` follow a change at once;
/// the menus AppKit draws follow it after a relaunch.
enum AppLanguage: String, CaseIterable, Identifiable {
    case vi, en, system
    static let defaultsKey = "HVNRemoteHub.language"
    static let fallback = AppLanguage.vi
    var id: Self { self }
    var title: String {
        switch self { case .system: "System language"; case .en: "English"; case .vi: "Tiếng Việt" }
    }
    var locale: Locale { self == .system ? .current : Locale(identifier: rawValue) }
    static var current: AppLanguage { resolve(UserDefaults.standard.string(forKey: defaultsKey)) }
    static func resolve(_ stored: String?) -> AppLanguage { stored.flatMap(AppLanguage.init(rawValue:)) ?? fallback }

    /// The language the menu bar of this process uses.
    @MainActor private(set) static var launched = fallback

    /// Runs before the app starts, so AppKit's own menus use the chosen language.
    @MainActor
    static func applyToSystemMenus(_ defaults: UserDefaults = .standard) {
        launched = resolve(defaults.string(forKey: defaultsKey))
        if let languages = launched.appleLanguages {
            defaults.set(languages, forKey: "AppleLanguages")
        } else {
            defaults.removeObject(forKey: "AppleLanguages")
        }
    }

    /// The `AppleLanguages` override for this choice; nil follows the system.
    var appleLanguages: [String]? { self == .system ? nil : [rawValue] }

    @MainActor
    static func relaunch() {
        let configuration = NSWorkspace.OpenConfiguration()
        configuration.createsNewApplicationInstance = true
        NSWorkspace.shared.openApplication(at: Bundle.main.bundleURL, configuration: configuration) { _, _ in
            Task { @MainActor in NSApp.terminate(nil) }
        }
    }
    static func localized(_ key: String, language: AppLanguage = current) -> String {
        let identifier = language == .system
            ? (Locale.preferredLanguages.first?.hasPrefix("vi") == true ? "vi" : "en") : language.rawValue
        // Inside the packaged app the catalogs sit in Contents/Resources; the
        // SwiftPM resource bundle is only consulted by tests and `swift run`.
        let sources = Bundle.main.bundleURL.pathExtension == "app" ? [Bundle.main] : [Bundle.main, Bundle.module]
        for source in sources {
            if let path = source.path(forResource: identifier, ofType: "lproj"), let bundle = Bundle(path: path) {
                let value = bundle.localizedString(forKey: key, value: nil, table: "Localizable")
                if value != key { return value }
            }
        }
        // Session state remains plain English internally. Translate the two
        // parameterized connection messages without touching peer names/IDs.
        for (prefix, suffix, format) in [("Connected to ", ".", "Connected to %@."),
                ("Connecting to ", "…", "Connecting to %@…"),
                ("Computer audio stopped: ", "", "Computer audio stopped: %@"),
                ("Remote input stopped: ", "", "Remote input stopped: %@"),
                ("Remote control could not be updated: ", "", "Remote control could not be updated: %@"),
                ("The remote action could not be completed: ", "", "The remote action could not be completed: %@"),
                ("Connected, but the password could not be saved: ", "", "Connected, but the password could not be saved: %@"),
                ("Saved passwords could not be removed: ", "", "Saved passwords could not be removed: %@"),
                ("Saved password unavailable: ", " Enter it manually.", "Saved password unavailable: %@ Enter it manually.")] {
            if key != format, key.hasPrefix(prefix), key.hasSuffix(suffix), key.count > prefix.count + suffix.count {
                let value = String(key.dropFirst(prefix.count).dropLast(suffix.count))
                let translated = localized(format, language: language)
                return String(format: translated, locale: language.locale, value)
            }
        }
        return key
    }
}

func L(_ key: String) -> String { AppLanguage.localized(key) }
func LF(_ key: String, _ values: CVarArg...) -> String {
    String(format: L(key), locale: AppLanguage.current.locale, arguments: values)
}

private struct AppLanguageModifier: ViewModifier {
    @AppStorage(AppLanguage.defaultsKey) private var language = AppLanguage.fallback.rawValue
    func body(content: Content) -> some View {
        content.environment(\.locale, AppLanguage.resolve(language).locale)
    }
}
extension View {
    func appLanguage() -> some View { modifier(AppLanguageModifier()) }
}
