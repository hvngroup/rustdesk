import AppKit
import SwiftUI

/// Applies the saved interface language before AppKit reads `AppleLanguages`,
/// so the menu bar opens in Vietnamese by default.
@main
@MainActor
enum Launcher {
    static func main() {
        AppLanguage.applyToSystemMenus()
        HVNRemoteHubApp.main()
    }
}

struct HVNRemoteHubApp: App {
    @StateObject private var model = ConnectionModel(adapter: NativeUltraViewerAdapter())
    @StateObject private var hosting = MacHostingModel()
    @StateObject private var capture = RemoteCaptureController()
    @StateObject private var updater = UpdateChecker()
    @NSApplicationDelegateAdaptor(HVNAppDelegate.self) private var applicationDelegate

    var body: some Scene {
        WindowGroup(Brand.appName) {
            ConnectionView(model: model, hosting: hosting, remoteCapture: capture, updater: updater)
                .frame(minWidth: 960, minHeight: 680)
                .onAppear {
                    applicationDelegate.capture = capture
                    applicationDelegate.model = model
                    applicationDelegate.hosting = hosting
                    updater.startAutomaticChecks()
                }
                .tint(Brand.red)
                .appLanguage()
        }
        .defaultSize(width: 1120, height: 800)
        .commands { HVNCommands(model: model, updater: updater) }

        Window(L("About HVN Remote Hub"), id: AboutView.windowID) {
            AboutView().tint(Brand.red).appLanguage()
        }
        .windowResizability(.contentSize)
        .windowStyle(.hiddenTitleBar)

        Settings {
            HVNSettingsView(model: model, updater: updater).tint(Brand.red).appLanguage()
        }
    }
}

struct HVNCommands: Commands {
    @ObservedObject var model: ConnectionModel
    @ObservedObject var updater: UpdateChecker
    @Environment(\.openWindow) private var openWindow

    var body: some Commands {
        CommandGroup(replacing: .newItem) {}
        CommandGroup(replacing: .appInfo) {
            Button(L("About HVN Remote Hub")) { openWindow(id: AboutView.windowID) }
            Button(L("Check for Updates…")) { updater.check(userInitiated: true) }
        }
        CommandMenu(L("Connection")) {
            Button(L("Connect")) { model.connect() }
                .keyboardShortcut("k", modifiers: [.command])
                .disabled(!model.canConnect)
            Button(L("Disconnect")) { model.disconnect() }
                .keyboardShortcut("d", modifiers: [.command, .shift])
                .disabled(!model.isSessionActive)
        }
        CommandGroup(replacing: .help) {
            Button(L("HVN Remote Hub Help")) { Brand.openUserGuide() }
                .keyboardShortcut("?", modifiers: [.command])
            Button(L("User Guide Online")) { NSWorkspace.shared.open(Brand.onlineGuideURL) }
            Divider()
            Button(L("HVN GROUP Website")) { NSWorkspace.shared.open(Brand.websiteURL) }
            Button(L("Email Technical Support")) { NSWorkspace.shared.open(Brand.supportMailURL) }
            Button(L("Report an Issue…")) { NSWorkspace.shared.open(Brand.issuesURL) }
        }
    }
}

struct HVNSettingsView: View {
    @ObservedObject var model: ConnectionModel
    @ObservedObject var updater: UpdateChecker
    @AppStorage(ConnectionModel.rememberPartnersKey) private var rememberPartners = true
    @AppStorage("HVNRemoteHub.smoothScreen") private var smoothScreen = true
    @AppStorage("HVNRemoteHub.scrollSensitivity") private var scrollSensitivity = 1.0
    @AppStorage(AppLanguage.defaultsKey) private var language = AppLanguage.fallback.rawValue
    @AppStorage(UpdateChecker.automaticKey) private var checkForUpdates = true
    @AppStorage(SessionToolsModel.shareClipboardKey) private var shareClipboard = true

    var body: some View {
        Form {
            Section("Language") {
                Picker("App language", selection: $language) {
                    ForEach(AppLanguage.allCases) { option in
                        Text(LocalizedStringKey(option.title)).tag(option.rawValue)
                    }
                }
                Text("The window changes at once. The menu bar changes after HVN Remote Hub restarts.")
                    .font(.caption).foregroundStyle(.secondary)
                if AppLanguage.resolve(language) != AppLanguage.launched {
                    Button("Restart Now") { AppLanguage.relaunch() }
                }
            }
            Section("History") {
                Toggle("Remember successfully connected partner IDs", isOn: $rememberPartners)
                    .onChange(of: rememberPartners) { _, enabled in
                        if !enabled { model.clearRecentPartners() }
                    }
                Text("Saved passwords are kept separately in macOS Keychain.")
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Button("Clear Recent Partners") { model.clearRecentPartners() }
                    .disabled(model.recentPartners.isEmpty)
                Button("Forget saved passwords", action: model.forgetSavedPasswords)
            }
            Section("Clipboard") {
                Toggle("Share clipboard with the other computer", isOn: $shareClipboard)
                Text("Text copied on either computer can be pasted on the other. Applies to new sessions.")
                    .font(.caption).foregroundStyle(.secondary)
            }
            Section("Remote screen") {
                Toggle("Smooth image scaling", isOn: $smoothScreen)
                Slider(value: $scrollSensitivity, in: 0.25...2, step: 0.25) {
                    Text("Scroll speed")
                }
                LabeledContent("Scroll speed", value: String(format: "%.2g×", scrollSensitivity))
            }
            Section("About") {
                LabeledContent("Application", value: "\(Brand.appName) \(Brand.version)")
                Toggle("Automatically check for updates", isOn: $checkForUpdates)
                Button(L("Check for Updates…")) { updater.check(userInitiated: true) }
                    .disabled(updater.state == .checking)
                Text(LocalizedStringKey(Brand.disclaimer))
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
        .formStyle(.grouped)
        .frame(width: 490, height: 600)
    }
}

@MainActor
final class HVNAppDelegate: NSObject, NSApplicationDelegate {
    weak var capture: RemoteCaptureController?
    weak var model: ConnectionModel?
    weak var hosting: MacHostingModel?
    private var isFinishing = false

    func applicationDidFinishLaunching(_ notification: Notification) {
        // LaunchServices may retain a generic icon from the first local build.
        // Give the running application its bundled icon directly as well.
        if let url = Bundle.main.url(forResource: "AppIcon", withExtension: "icns"),
           let icon = NSImage(contentsOf: url) { NSApp.applicationIconImage = icon }
    }

    // Closing the only window ends HVN Remote Hub, and with it every connection.
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }

    func applicationShouldTerminate(_ sender: NSApplication) -> NSApplication.TerminateReply {
        guard !isFinishing else { return .terminateLater }
        isFinishing = true
        Task {
            if let capture, capture.isRecording || capture.isFinishingRecording || capture.isPreparingRecording {
                await capture.stopRecording()
            }
            // Tell the other computer the session is over before the process
            // exits; otherwise it waits for a relay timeout. Never block quit
            // for long on an unresponsive network.
            await withTaskGroup(of: Void.self) { group in
                group.addTask { await self.closeConnections() }
                group.addTask { try? await Task.sleep(for: .seconds(2)) }
                await group.next()
                group.cancelAll()
            }
            sender.reply(toApplicationShouldTerminate: true)
        }
        return .terminateLater
    }

    private func closeConnections() async {
        await model?.shutdown()
        await hosting?.shutdown()
    }
}
