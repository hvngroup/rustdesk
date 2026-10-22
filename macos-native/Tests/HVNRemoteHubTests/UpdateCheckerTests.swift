import Foundation
import Testing
@testable import HVNRemoteHub

@Test func updateVersionsCompareNumerically() {
    #expect(UpdateChecker.isVersion("0.3.2", newerThan: "0.3.1"))
    #expect(UpdateChecker.isVersion("0.10.0", newerThan: "0.9.9"))
    #expect(UpdateChecker.isVersion("1.0", newerThan: "0.99.99"))
    #expect(UpdateChecker.isVersion("0.3.1.1", newerThan: "0.3.1"))
    #expect(!UpdateChecker.isVersion("0.3.1", newerThan: "0.3.1"))
    #expect(!UpdateChecker.isVersion("0.3", newerThan: "0.3.0"))
    #expect(!UpdateChecker.isVersion("0.3.0", newerThan: "0.3.1"))
    #expect(!UpdateChecker.isVersion("0.3.2-beta", newerThan: "0.3.2"))
}

@Test func updateReleaseParsingPicksTheNewestMacReleaseAndItsDMG() throws {
    let base = "https://github.com/hvngroup/universal-remote-hub/releases"
    let json = """
    [{"tag_name": "v1.5.1-1", "html_url": "\(base)/tag/v1.5.1-1", "draft": false, "prerelease": false,
      "assets": [{"name": "HVNRemoteHub-1.5.1-aarch64.dmg", "browser_download_url": "\(base)/download/v1.5.1-1/HVNRemoteHub-1.5.1-aarch64.dmg"}]},
     {"tag_name": "mac-v0.3.2", "html_url": "\(base)/tag/mac-v0.3.2", "draft": false, "prerelease": false,
      "assets": [
        {"name": "HVNRemoteHub-0.3.2.zip", "browser_download_url": "\(base)/download/mac-v0.3.2/HVNRemoteHub-0.3.2.zip"},
        {"name": "HVNRemoteHub-0.3.2.dmg", "browser_download_url": "\(base)/download/mac-v0.3.2/HVNRemoteHub-0.3.2.dmg"},
        {"name": "SHA256SUMS.txt", "browser_download_url": "\(base)/download/mac-v0.3.2/SHA256SUMS.txt"}
      ]},
     {"tag_name": "mac-v0.3.1", "html_url": "\(base)/tag/mac-v0.3.1", "assets": []}]
    """
    let release = try UpdateChecker.parseLatestRelease(Data(json.utf8))
    #expect(release.version == "0.3.2")
    #expect(release.dmgURL?.lastPathComponent == "HVNRemoteHub-0.3.2.dmg")
    #expect(release.pageURL.absoluteString.hasSuffix("/releases/tag/mac-v0.3.2"))
}

@Test func updateReleaseParsingSkipsPrereleasesForeignHostsAndOtherProducts() {
    let base = "https://github.com/hvngroup/universal-remote-hub/releases"
    let json = """
    [{"tag_name": "mac-v0.4.0-beta", "html_url": "\(base)/tag/mac-v0.4.0-beta", "prerelease": true, "assets": []},
     {"tag_name": "mac-v0.3.2", "html_url": "\(base)/tag/mac-v0.3.2",
      "assets": [{"name": "HVNRemoteHub-0.3.2.dmg", "browser_download_url": "https://example.com/HVNRemoteHub-0.3.2.dmg"}]},
     {"tag_name": "v1.5.1-1", "html_url": "\(base)/tag/v1.5.1-1", "assets": []}]
    """
    #expect(throws: (any Error).self) { try UpdateChecker.parseLatestRelease(Data(json.utf8)) }
}

@MainActor
@Test func automaticUpdateChecksRespectTheSetting() throws {
    let suite = "UpdateCheckerTests-\(UUID().uuidString)"
    let defaults = try #require(UserDefaults(suiteName: suite))
    defer { defaults.removePersistentDomain(forName: suite) }
    let checker = UpdateChecker(currentVersion: "0.3.2", defaults: defaults)
    defaults.set(false, forKey: UpdateChecker.automaticKey)
    checker.checkAutomatically()
    #expect(checker.state == .idle)
}

@Test func updateNotesDropTheInstallSection() {
    let body = """
    ## Install
    1. Download the DMG.
    2. Drag HVN Remote Hub to Applications.

    ## What's Changed
    * Close connections when quitting
    """
    #expect(UpdateChecker.releaseNotes(body) == "## What's Changed\n* Close connections when quitting")
    #expect(UpdateChecker.releaseNotes("") == "")
}
