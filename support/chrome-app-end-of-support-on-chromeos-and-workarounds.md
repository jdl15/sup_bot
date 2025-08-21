# Chrome App - End of Support on ChromeOS and Workarounds

* [Google Chrome Apps End-of-Support Timeline](#EoS)
* [Who Is Affected](#Affected)
* [Workaround 1: Webplayer on Google Admin Console](#Workaround1)
* [Workaround 2: Downloading OptiSigns from the Google Play Store](#Workaround2)
* [Workaround 3: Downloading OptiSigns APK from OptiSigns Website](#Workaround3)
* [Recommendations](#Recommendations)

Google is phasing out **Chrome Apps** on Chrome OS. The OptiSigns Chrome App (available in the [Chrome Web Store](https://chromewebstore.google.com/detail/optisigns-digital-signage/ankpffnbahhgegojammhgdnbmdbfnnfe)) is affected by this change and may no longer run on certain Chrome OS versions.

If your Chrome OS device can no longer run the OptiSigns Chrome App, you can still use OptiSigns by downloading our app from the [Google Play Store](https://play.google.com/store/apps/details?id=com.optisigns.playe1&hl=en-US), or our **Android APK** version directly from our [website](https://download.optisignsapp.com/Android/optisigns_googleVersion_release_latest_stable.apk). The latter option requires access to Developer Mode.

---

## **Google Chrome Apps End-of-Support Timeline**

According to [Google’s official statement](https://support.google.com/chrome/a/answer/15950395?sjid=12937841724344377860-NC):

* **July 2025 (ChromeOS M138)** – Last release supporting **user-installed Chrome Apps** (like the OptiSigns Chrome App).
* **July 2026 (ChromeOS M150)** – Last release supporting **Chrome Apps in kiosk mode**. LTS channel devices supported until April 2027.
* **February 2028 (ChromeOS M168)** – Final end of **all Chrome Apps**. LTS devices supported until October 2028.

---

## **Who Is Affected**

You may be affected if:

* You use the **OptiSigns Chrome App** on Chrome OS.
* Your device has updated beyond **ChromeOS M138** for regular installs, or beyond **M150** for kiosk mode.
* The app fails to launch, shows “App not supported,” or no longer appears in your app list.

**Check your Chrome OS version:**

1. Go to **Settings → About Chrome OS**.
2. Note your version and channel (Stable, Beta, Dev, LTS, LTC).

---

## **Workaround 1 (Recommended): Use OptiSigns Webplayer on Google Admin Console**

Enabling the OptiSigns Webplayer on your kiosk via the Google Admin Console is the most reliable workaround to this issue. When properly configured, it allows OptiSigns to autostart upon reboot.

To do this, you'll need to allow [**webplayer.optisigns.com**](https://webplayer.optisigns.com/) to be installed on your ChromeOS devices.

For more on performing these actions, see:

* [Google Admin Console - Enrolling ChromeOS Devices](https://support.google.com/chrome/a/answer/1360534?hl=en)
* [Managing Chrome kiosk settings](https://support.google.com/chrome/a/answer/9273974?hl=en)

---

## **Workaround 2: Download OptiSigns App from the Google Play Store**

Downloading the app from the [Google Play Store](https://play.google.com/store/apps/details?id=com.optisigns.playe1&hl=en-US) is another easy method. However, auto-start will need to be configured manually.

---

## **Workaround 3: Download the OptiSigns Android APK from OptiSigns Website**

We have tested and confirmed that the OptiSigns Android APK works on Chrome OS devices even when the Chrome App no longer runs.

**How to Install the APK:**

**Download the APK**  
- Go to the official OptiSigns [website](https://www.optisigns.com/download) and download the latest [Android APK](https://download.optisignsapp.com/Android/optisigns_googleVersion_release_latest_stable.apk).

1. **Enable “Unknown Sources”**
   1. Go to **Settings → Security & Privacy → Install unknown apps**.
   2. Allow installation from your browser or file manager.
2. **Install the APK**
   1. Open the downloaded APK in the Files app.
   2. Follow prompts to install.
3. **Launch OptiSigns**
   1. Find it in your launcher, sign in, and start using your displays.

Note that to run the APK, you will need access to [**Developer Mode**](https://developer.android.com/studio/debug/dev-options).

---

## **Recommendations**

* If you still need kiosk mode, use the APK in combination with Chrome OS kiosk settings (if supported by your device).
* Keep Chrome OS updated to the latest version your device supports.
* For long-term deployments, consider switching to a fully supported [Android](https://www.optisigns.com/product/hardware) or [Pro/ProMax](https://www.optisigns.com/product/hardware) player.

### That’s all!

OptiSigns is the leader in [digital signage software](https://www.optisigns.com/). If you have any additional questions, concerns or any feedback about OptiSigns, feel free to reach out to our support team at [support@optisigns.com](mailto:support@optisigns.com).