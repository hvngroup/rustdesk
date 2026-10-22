import AppKit
import SwiftUI

/// HVN GROUP identity used across the app: colors, contact points and the logo.
enum Brand {
    static let appName = "HVN Remote Hub"
    /// Brand Red #EA4445, Dark Red #C93939, Medium Gray #808080.
    static let red = Color(red: 0xEA / 255, green: 0x44 / 255, blue: 0x45 / 255)
    static let darkRed = Color(red: 0xC9 / 255, green: 0x39 / 255, blue: 0x39 / 255)
    static let gray = Color(red: 0x80 / 255, green: 0x80 / 255, blue: 0x80 / 255)

    static let website = "hvn.vn"
    static let supportEmail = "kythuat@hvn.vn"
    static let hotline = "024.9999.7777"
    static let repository = "hvngroup/universal-remote-hub"
    static let websiteURL = URL(string: "https://hvn.vn")!
    static let supportMailURL = URL(string: "mailto:kythuat@hvn.vn?subject=HVN%20Remote%20Hub")!
    static let issuesURL = URL(string: "https://github.com/hvngroup/universal-remote-hub/issues/new/choose")!
    static let onlineGuideURL = URL(string: "https://github.com/hvngroup/universal-remote-hub/blob/master/macos-native/docs/user-guide.md")!

    static let disclaimer = "HVN Remote Hub is made by HVN GROUP. It works with UltraViewer but is not an official UltraViewer product and is not affiliated with or endorsed by the UltraViewer developers."

    static var version: String { info("CFBundleShortVersionString") ?? "dev" }
    static var build: String { info("CFBundleVersion") ?? "0" }

    private static func info(_ key: String) -> String? {
        Bundle.main.object(forInfoDictionaryKey: key) as? String
    }

    /// Images the packaging script copies into Contents/Resources.
    static func image(named name: String) -> NSImage? {
        Bundle.main.url(forResource: name, withExtension: "png").flatMap(NSImage.init(contentsOf:))
    }

    /// Opens the user guide packaged with the app in the default Markdown
    /// reader, or the online copy when none is installed.
    @MainActor
    static func openUserGuide() {
        if let guide = Bundle.main.url(forResource: "user-guide", withExtension: "md"),
           NSWorkspace.shared.urlForApplication(toOpen: guide) != nil {
            NSWorkspace.shared.open(guide)
        } else {
            NSWorkspace.shared.open(onlineGuideURL)
        }
    }

    /// The folder of third-party and upstream licenses inside the app.
    static var licensesURL: URL? {
        Bundle.main.resourceURL?.appendingPathComponent("Licenses", isDirectory: true)
    }
}

/// The HVN GROUP logo from the brand guideline: full color on light
/// backgrounds, white on dark ones. Falls back to the word mark in a
/// development build that has no packaged images.
struct HVNLogo: View {
    var height: CGFloat = 24
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        if let image = Brand.image(named: colorScheme == .dark ? "hvn-logo-white" : "hvn-logo-color") {
            Image(nsImage: image)
                .resizable()
                .interpolation(.high)
                .aspectRatio(contentMode: .fit)
                .frame(height: height)
                .accessibilityLabel(Text(verbatim: "HVN GROUP"))
        } else {
            Text(verbatim: "HVN GROUP")
                .font(.system(size: height * 0.6, weight: .bold))
                .foregroundStyle(Brand.red)
        }
    }
}
