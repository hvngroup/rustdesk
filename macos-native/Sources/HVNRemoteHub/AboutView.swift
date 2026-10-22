import AppKit
import SwiftUI

/// The About window: icon, version, the HVN GROUP logo and contact points,
/// the interoperability disclaimer and the bundled licenses.
struct AboutView: View {
    static let windowID = "about"

    var body: some View {
        VStack(spacing: 14) {
            Image(nsImage: NSApp.applicationIconImage)
                .resizable()
                .frame(width: 96, height: 96)
                .accessibilityHidden(true)
            VStack(spacing: 4) {
                Text(verbatim: Brand.appName).font(.title2.weight(.semibold))
                Text(LF("Version %@ (%@)", Brand.version, Brand.build))
                    .font(.callout).foregroundStyle(.secondary)
                    .textSelection(.enabled)
            }
            Text("Control computers running UltraViewer from your Mac, or share this Mac after you approve each request.")
                .font(.callout)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
            Divider()
            HVNLogo(height: 30)
            Text("Digital platform solutions and services for businesses")
                .font(.caption).foregroundStyle(.secondary)
            HStack(spacing: 16) {
                Link(destination: Brand.websiteURL) { Text(verbatim: Brand.website) }
                Link(destination: Brand.supportMailURL) { Text(verbatim: Brand.supportEmail) }
                Text(verbatim: Brand.hotline).foregroundStyle(.secondary).textSelection(.enabled)
            }
            .font(.callout)
            Text(LocalizedStringKey(Brand.disclaimer))
                .font(.caption)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
                .fixedSize(horizontal: false, vertical: true)
            HStack(spacing: 12) {
                Button("Licenses") {
                    if let url = Brand.licensesURL { NSWorkspace.shared.open(url) }
                }
                .disabled(Brand.licensesURL.map { !FileManager.default.fileExists(atPath: $0.path) } ?? true)
                Button("Help") { Brand.openUserGuide() }
            }
            .controlSize(.small)
            Text(verbatim: "© 2026 HVN GROUP · hvn.vn")
                .font(.caption2).foregroundStyle(.tertiary)
        }
        .padding(28)
        .frame(width: 420)
    }
}
