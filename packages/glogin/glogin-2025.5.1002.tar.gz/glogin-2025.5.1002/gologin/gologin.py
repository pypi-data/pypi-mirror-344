import json
import logging
import time
import os
import stat
import sys
import shutil
import requests
import zipfile
import subprocess
import pathlib
import tempfile
import socket
import random
import psutil

from gologin.extensionsManager import ExtensionsManager
from gologin.cookiesManager import CookiesManager

API_URL = "https://api.gologin.com"
PROFILES_URL = "https://gprofiles-new.gologin.com/"
GET_TIMEZONE_URL = "https://geo.myip.link"
FILES_GATEWAY = "https://files-gateway.gologin.com"


class ProtocolException(Exception):
    def __init__(self, data: dict):
        self._json = data
        super().__init__(data.__repr__())

    @property
    def json(self) -> dict:
        return self._json


class GoLogin(object):
    def __init__(self, options):
        self.access_token = options.get("token")
        self.profile_id = options.get("profile_id")
        self.tmpdir = options.get("tmpdir", tempfile.gettempdir())
        self.address = options.get("address", "127.0.0.1")
        self.extra_params = options.get("extra_params", [])
        self.port = options.get("port", 0)
        self.extensions = options.get("extensions", [])
        if self.port == 0:
            self.port = getRandomPort()

        self.ws = None
        self.headless = options.get("headless", True)
        self.local = options.get("local", False)
        self.spawn_browser = options.get("spawn_browser", True)
        self.credentials_enable_service = options.get("credentials_enable_service")
        self.cleaningLocalCookies = options.get("cleaningLocalCookies", False)
        self.uploadCookiesToServer = options.get("uploadCookiesToServer", False)
        self.writeCookiesFromServer = options.get("writeCookiesFromServer", False)
        self.restore_last_session = options.get("restore_last_session", False)
        self.executablePath = options.get("executablePath")
        self.is_cloud_headless = options.get("is_cloud_headless", True)
        self.is_new_cloud_browser = options.get("is_new_cloud_browser", True)
        if self.extra_params:
            print("extra_params", self.extra_params)
        self.setProfileId(options.get("profile_id"))
        self.preferences = {}
        self.pid = int()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()

    def setProfileId(self, profile_id):
        self.profile_id = profile_id
        if self.profile_id == None:
            return
        self.profile_path = os.path.join(self.tmpdir, "gologin_" + self.profile_id)
        self.profile_default_folder_path = os.path.join(self.profile_path, "Default")
        self.profile_zip_path = os.path.join(
            self.tmpdir, "gologin_" + self.profile_id + ".zip"
        )
        self.profile_zip_path_upload = os.path.join(
            self.tmpdir, "gologin_" + self.profile_id + "_upload.zip"
        )

    def loadExtensions(self):
        profile = self.profile
        chromeExtensions = profile.get("chromeExtensions")
        extensionsManagerInst = ExtensionsManager()
        pathToExt = ""
        profileExtensionsCheck = []
        for ext in chromeExtensions:
            try:
                ver = extensionsManagerInst.downloadExt(ext)
                pathToExt += os.path.join(
                    pathlib.Path.home(),
                    ".gologin",
                    "extensions",
                    "chrome-extensions",
                    ext + "@" + ver + ",",
                )
                profileExtensionsCheck.append(
                    os.path.join(
                        pathlib.Path.home(),
                        ".gologin",
                        "extensions",
                        "chrome-extensions",
                        ext + "@" + ver,
                    )
                )
            except Exception as e:
                print("error downloading extension", e)
                continue

        pref_file = os.path.join(self.profile_path, "Default", "Preferences")
        with open(pref_file, "r", encoding="utf-8") as pfile:
            preferences = json.load(pfile)

        noteExtExist = ExtensionsManager().extensionIsAlreadyExisted(
            preferences, profileExtensionsCheck
        )

        if noteExtExist:
            return
        else:
            return pathToExt

    def spawnBrowser(self):
        proxy = self.proxy
        proxy_host = ""
        if proxy:
            if proxy.get("mode") is None or proxy.get("mode") == "geolocation":
                proxy["mode"] = "http"
            proxy_host = proxy.get("host")
            proxy = self.formatProxyUrl(proxy)

        tz = self.tz.get("timezone")

        params = [
            self.executablePath,
            "--remote-debugging-port=" + str(self.port),
            "--user-data-dir=" + self.profile_path,
            "--password-store=basic",
            "--gologin-profile=" + self.profile_name,
            "--lang=en-US",
            "--disable-gpu",
            "--webrtc-ip-handling-policy=default_public_interface_only",
            "--disable-features=PrintCompositorLPAC",
        ]
        if self.headless:
            params.append("--headless=new")

        chromeExtensions = self.profile.get("chromeExtensions")
        if chromeExtensions and len(chromeExtensions) > 0:
            paths = self.loadExtensions()
            if paths is not None:
                extToParams = "--load-extension=" + paths
                params.append(extToParams)

        if self.extensions:
            extToParams = "--load-extension=" + ",".join(self.extensions)
            params.append(extToParams)

        if proxy:
            hr_rules = "MAP * 0.0.0.0 , EXCLUDE %s" % (proxy_host)
            params.append("--proxy-server=" + proxy)
            params.append("--host-resolver-rules=" + hr_rules)

        if self.restore_last_session:
            params.append("--restore-last-session")

        for param in self.extra_params:
            params.append(param)

        print("platform", sys.platform)

        print("params", params)

        open_browser = subprocess.Popen(
            params,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
        self.pid = open_browser.pid

        url = f"{self.address}:{self.port}"
        self.ws = self.waitBrowser(url, 5)

        return url

    def start(self):
        profile_path = self.createStartup()
        if self.spawn_browser is True:
            return self.spawnBrowser()
        return profile_path

    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                path = os.path.join(root, file)
                if not os.path.exists(path):
                    continue
                if stat.S_ISSOCK(os.stat(path).st_mode):
                    continue
                ziph.write(path, path.replace(self.profile_path, ""))

    def waitUntilProfileUsing(self, try_count=0):
        if try_count > 10:
            return
        time.sleep(1)
        profile_path = self.profile_path
        if os.path.exists(profile_path):
            try:
                os.rename(profile_path, profile_path)
            except OSError as e:
                print("waiting chrome termination")
                self.waitUntilProfileUsing(try_count + 1)

    def waitBrowser(self, url, timeout=10) -> str:
        cnt = 0
        url = f"http://{url}/json/version"
        while cnt < timeout:
            cnt += 1
            time.sleep(1)
            try:
                r = requests.get(url, timeout=1)
                return r.json()["webSocketDebuggerUrl"]

            except Exception:
                pass

        return ""

    def stop(self):
        for proc in psutil.process_iter(["pid"]):
            if proc.info.get("pid") == self.pid:
                proc.kill()
        self.waitUntilProfileUsing()
        self.sanitizeProfile()
        if self.local is False:
            self.commitProfile()
            os.remove(self.profile_zip_path_upload)
            shutil.rmtree(self.profile_path)
        print("profile stopped")

    def commitProfile(self):
        print("commitProfile")
        zipf = zipfile.ZipFile(self.profile_zip_path_upload, "w", zipfile.ZIP_DEFLATED)
        self.zipdir(self.profile_default_folder_path, zipf)
        zipf.writestr("First Run", "")
        zipf.close()

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "User-Agent": "Selenium-API",
            "Content-Type": "application/zip",
            "browserId": self.profile_id,
        }

        data = requests.put(
            FILES_GATEWAY + "/upload",
            data=open(self.profile_zip_path_upload, "rb"),
            headers=headers,
        )
        print("commitProfile completed", data)

    def commitProfileOld(self):
        zipf = zipfile.ZipFile(self.profile_zip_path_upload, "w", zipfile.ZIP_DEFLATED)
        self.zipdir(self.profile_path, zipf)
        zipf.close()

        headers = {
            "Authorization": "Bearer " + self.access_token,
            "User-Agent": "Selenium-API",
        }
        # print('profile size=', os.stat(self.profile_zip_path_upload).st_size)

        signedUrl = requests.get(
            API_URL + "/browser/" + self.profile_id + "/storage-signature",
            headers=headers,
        ).content.decode("utf-8")

        requests.put(signedUrl, data=open(self.profile_zip_path_upload, "rb"))

        # print('commit profile complete')

    def sanitizeProfile(self):
        if self.cleaningLocalCookies:
            path_to_coockies = os.path.join(
                self.profile_path, "Default", "Network", "Cookies"
            )
            os.remove(path_to_coockies)

        SEPARATOR = os.sep

        remove_dirs = [
            f"Default{SEPARATOR}Cache",
            f"Default{SEPARATOR}Service Worker",
            f"Default{SEPARATOR}Code Cache",
            f"Default{SEPARATOR}GPUCache",
            f"Default{SEPARATOR}Service Worker",
            f"Default{SEPARATOR}Extensions",
            f"Default{SEPARATOR}IndexedDB",
            f"Default{SEPARATOR}GPUCache",
            f"Default{SEPARATOR}DawnCache",
            f"Default{SEPARATOR}fonts_config",
            f"GrShaderCache",
            f"ShaderCache",
            f"biahpgbdmdkfgndcmfiipgcebobojjkp",
            f"afalakplffnnnlkncjhbmahjfjhmlkal",
            f"cffkpbalmllkdoenhmdmpbkajipdjfam",
            f"Dictionaries",
            f"enkheaiicpeffbfgjiklngbpkilnbkoi",
            f"oofiananboodjbbmdelgdommihjbkfag",
            f"SafetyTips",
            f"fonts",
        ]

        for d in remove_dirs:
            fpath = os.path.join(self.profile_path, d)
            if os.path.exists(fpath):
                try:
                    shutil.rmtree(fpath)
                except:
                    continue

    def formatProxyUrl(self, proxy):
        return (
            proxy.get("mode", "http")
            + "://"
            + proxy.get("host", "")
            + ":"
            + str(proxy.get("port", 80))
        )

    def formatProxyUrlPassword(self, proxy):
        mode = "socks5h" if proxy.get("mode") == "socks5" else proxy.get("mode", "http")
        if proxy.get("username", "") == "":
            return (
                mode + "://" + proxy.get("host", "") + ":" + str(proxy.get("port", 80))
            )
        else:
            return (
                mode
                + "://"
                + proxy.get("username", "")
                + ":"
                + proxy.get("password")
                + "@"
                + proxy.get("host", "")
                + ":"
                + str(proxy.get("port", 80))
            )

    def getTimeZone(self):
        proxy = self.proxy
        if proxy:
            proxies = {
                "http": self.formatProxyUrlPassword(proxy),
                "https": self.formatProxyUrlPassword(proxy),
            }
            data = requests.get(GET_TIMEZONE_URL, proxies=proxies)
        else:
            data = requests.get(GET_TIMEZONE_URL)
        return json.loads(data.content.decode("utf-8"))

    def getProfile(self, profile_id=None):
        profile = self.profile_id if profile_id == None else profile_id
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "User-Agent": "Selenium-API",
        }
        data = json.loads(
            requests.get(
                API_URL + "/browser/" + profile, headers=headers
            ).content.decode("utf-8")
        )
        if data.get("statusCode") == 404:
            raise Exception(data.get("error") + ": " + data.get("message"))
        return data

    def downloadProfileZip(self):
        print("downloadProfileZip")
        s3path = self.profile.get("s3Path", "")
        data = ""
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "User-Agent": "Selenium-API",
            "browserId": self.profile_id,
        }

        data = requests.get(FILES_GATEWAY + "/download", headers=headers).content
        # print size MB
        #
        print("profile_zip_path: ", self.profile_zip_path)
        if len(data) == 0:
            print("data is 0 - creating empty profile")
            self.createEmptyProfile()
        else:
            with open(self.profile_zip_path, "wb") as f:
                f.write(data)

        try:
            print("extracting profile")
            self.extractProfileZip()
        except Exception as e:
            print("ERROR!", e)
            self.uploadEmptyProfile()
            self.createEmptyProfile()
            self.extractProfileZip()

        # if not os.path.exists(os.path.join(self.profile_path, 'Default', 'Preferences')):
        #     print('preferences not found - creating fresh profile content')
        #    z self.uploadEmptyProfile()
        #    z self.createEmptyProfile()
        #    z  b 
    def downloadProfileZipOld(self):
        print("downloadProfileZip")
        s3path = self.profile.get("s3Path", "")
        data = ""
        if s3path == "":
            # print('downloading profile direct')
            headers = {
                "Authorization": "Bearer " + self.access_token,
                "User-Agent": "Selenium-API",
            }
            data = requests.get(
                API_URL + "/browser/" + self.profile_id, headers=headers
            ).content
        else:
            # print('downloading profile s3')
            s3url = PROFILES_URL + s3path.replace(" ", "+")
            data = requests.get(s3url).content

        if len(data) == 0:
            print("data is 0 - creating fresh profile content")
            self.createEmptyProfile()
        else:
            print("data is not 0")
            with open(self.profile_zip_path, "wb") as f:
                f.write(data)

        try:
            print("extracting profile")
            self.extractProfileZip()
        except Exception as e:
            print("exception", e)
            # self.uploadEmptyProfile()
            self.createEmptyProfile()
            self.extractProfileZip()

        if not os.path.exists(
            os.path.join(self.profile_path, "Default", "Preferences")
        ):
            print("preferences not found - creating fresh profile content")
            # self.uploadEmptyProfile()
            self.createEmptyProfile()
            self.extractProfileZip()

    def uploadEmptyProfile(self):
        print("uploadEmptyProfile")
        upload_profile = open(r"./gologin_zeroprofile.zip", "wb")
        source = requests.get(PROFILES_URL + "zero_profile.zip")
        upload_profile.write(source.content)
        upload_profile.close

    def createEmptyProfile(self):
        print("createEmptyProfile")
        empty_profile = "../gologin_zeroprofile.zip"

        if not os.path.exists(empty_profile):
            empty_profile = "gologin_zeroprofile.zip"

        if os.path.exists(empty_profile):
            shutil.copy(empty_profile, self.profile_zip_path)

        if not os.path.exists(empty_profile):
            print("downloading zero profile")
            source = requests.get(PROFILES_URL + "zero_profile.zip")
            with open(self.profile_zip_path, "wb") as profile_zip:
                profile_zip.write(source.content)

    def extractProfileZip(self):
        with zipfile.ZipFile(self.profile_zip_path, "r") as zip_ref:
            zip_ref.extractall(self.profile_path)
        print("profile extracted", self.profile_path)
        # print size profile_path with MB
        print(
            "profile_path size=",
            f"{os.stat(self.profile_path).st_size / (1024 * 1024)} MB",
        )

        os.remove(self.profile_zip_path)

    def getGeolocationParams(self, profileGeolocationParams, tzGeolocationParams):
        if profileGeolocationParams.get("fillBasedOnIp"):
            return {
                "mode": profileGeolocationParams["mode"],
                "latitude": float(tzGeolocationParams["latitude"]),
                "longitude": float(tzGeolocationParams["longitude"]),
                "accuracy": float(tzGeolocationParams["accuracy"]),
            }

        return {
            "mode": profileGeolocationParams["mode"],
            "latitude": profileGeolocationParams["latitude"],
            "longitude": profileGeolocationParams["longitude"],
            "accuracy": profileGeolocationParams["accuracy"],
        }

    def getGologinPreferences(self, profileData):
        os = profileData.get("os", "")
        osSpec = profileData.get("osSpec", "")
        isM1 = profileData.get("isM1", False)
        isArm = (os == "mac" and osSpec and "M" in osSpec) or isM1
        resolution = profileData.get("navigator", {}).get("resolution", "1920x1080")
        screenWidth = int(resolution.split("x")[0])
        screenHeight = int(resolution.split("x")[1])
        langHeader = profileData.get("navigator", {}).get("language", "")
        print("langHeader", langHeader)
        splittedLangs = langHeader.split(",")[0] if langHeader else "en-US"

        startupUrl = profileData.get("startUrl", "").strip().split(",")[0]
        startupUrls = [
            url.strip()
            for url in profileData.get("startUrl", "").split(",")
            if url.strip()
        ]
        self.tz = self.getTimeZone()

        preferences = {
            "profile_id": profileData.get("id"),
            "name": profileData.get("name"),
            "is_m1": isArm,
            "geolocation": profileData.get("geolocation", {}),
            "navigator": {
                "platform": profileData.get("navigator", {}).get("platform", ""),
                "max_touch_points": profileData.get("navigator", {}).get(
                    "maxTouchPoints", 0
                ),
            },
            "dns": profileData.get("dns", {}),
            "proxy": {
                "username": profileData.get("proxy", {}).get("username", ""),
                "password": profileData.get("proxy", {}).get("password", ""),
            },
            "webRTC": profileData.get("webRTC", {}),
            "screenHeight": screenHeight,
            "screenWidth": screenWidth,
            "userAgent": profileData.get("navigator", {}).get("userAgent", ""),
            "webGl": {
                "vendor": profileData.get("webGLMetadata", {}).get("vendor", ""),
                "renderer": profileData.get("webGLMetadata", {}).get("renderer", ""),
                "mode": profileData.get("webGLMetadata", {}).get("mode", "") == "mask",
            },
            "webRTC": profileData.get("webRTC", {}),
            "webgl": {
                "metadata": {
                    "vendor": profileData.get("webGLMetadata", {}).get("vendor", ""),
                    "renderer": profileData.get("webGLMetadata", {}).get(
                        "renderer", ""
                    ),
                    "mode": profileData.get("webGLMetadata", {}).get("mode", "")
                    == "mask",
                },
            },
            "mobile": {
                "enable": profileData.get("os", False) == "android",
                "width": profileData.get("screenWidth", 1920),
                "height": profileData.get("screenHeight", 1080),
                "device_scale_factor": profileData.get("devicePixelRatio", 1),
            },
            "webglParams": profileData.get("webglParams", {}),
            "webGpu": profileData.get("webGpu", {}),
            "webgl_noice_enable": profileData.get("webGL", {}).get("mode") == "noise",
            "webglNoiceEnable": profileData.get("webGL", {}).get("mode") == "noise",
            "webgl_noise_enable": profileData.get("webGL", {}).get("mode") == "noise",
            "webgl_noise_value": profileData.get("webGL", {}).get("noise"),
            "webglNoiseValue": profileData.get("webGL", {}).get("noise"),
            "getClientRectsNoice": profileData.get("clientRects", {}).get("noise")
            or profileData.get("webGL", {}).get("getClientRectsNoise"),
            "client_rects_noise_enable": profileData.get("clientRects", {}).get("mode")
            == "noise",
            "media_devices": {
                "enable": profileData.get("mediaDevices", {}).get(
                    "enableMasking", True
                ),
                "uid": profileData.get("mediaDevices", {}).get("uid", ""),
                "audioInputs": profileData.get("mediaDevices", {}).get(
                    "audioInputs", 1
                ),
                "audioOutputs": profileData.get("mediaDevices", {}).get(
                    "audioOutputs", 1
                ),
                "videoInputs": profileData.get("mediaDevices", {}).get(
                    "videoInputs", 1
                ),
            },
            "doNotTrack": profileData.get("navigator", {}).get("doNotTrack", False),
            "plugins": {
                "all_enable": profileData.get("plugins", {}).get(
                    "enableVulnerable", True
                ),
                "flash_enable": profileData.get("plugins", {}).get("enableFlash", True),
            },
            "storage": {
                "enable": profileData.get("storage", {}).get("local", True),
            },
            "audioContext": {
                "enable": profileData.get("audioContext", {}).get("mode", "off")
                != "off",
                "noiseValue": profileData.get("audioContext", {}).get("noise", ""),
            },
            "canvas": {
                "mode": profileData.get("canvas", {}).get("mode", ""),
            },
            "languages": splittedLangs,
            "langHeader": langHeader,
            "canvasMode": profileData.get("canvas", {}).get("mode", ""),
            "canvasNoise": profileData.get("canvas", {}).get("noise", ""),
            "deviceMemory": profileData.get("navigator", {}).get("deviceMemory", 0),
            "hardwareConcurrency": profileData.get("navigator", {}).get(
                "hardwareConcurrency", 2
            ),
            "deviceMemory": profileData.get("navigator", {}).get("deviceMemory", 2)
            * 1024,
            "startupUrl": startupUrl,
            "startup_urls": startupUrls,
            "geolocation": {
                "mode": profileData.get("geolocation", {}).get("mode", "prompt"),
                "latitude": float(self.tz.get("ll", [0, 0])[0]),
                "longitude": float(self.tz.get("ll", [0, 0])[1]),
                "accuracy": float(self.tz.get("accuracy", 0)),
            },
            "timezone": {
                "id": self.tz.get("timezone", ""),
            },
        }
        self.preferences = preferences

        return preferences

    def updatePreferences(self):
        pref_file = os.path.join(self.profile_path, "Default", "Preferences")
        with open(pref_file, "r", encoding="utf-8") as pfile:
            preferences = json.load(pfile)
        profile = self.profile
        profile["profile_id"] = self.profile_id

        proxy = self.profile.get("proxy")
        # print('proxy=', proxy)
        if proxy and (proxy.get("mode") == "gologin" or proxy.get("mode") == "tor"):
            autoProxyServer = profile.get("autoProxyServer")
            splittedAutoProxyServer = autoProxyServer.split("://")
            splittedProxyAddress = splittedAutoProxyServer[1].split(":")
            port = splittedProxyAddress[1]

            proxy = {
                "mode": "http",
                "host": splittedProxyAddress[0],
                "port": port,
                "username": profile.get("autoProxyUsername"),
                "password": profile.get("autoProxyPassword"),
                "timezone": profile.get("autoProxyTimezone", "us"),
            }

            profile["proxy"]["username"] = profile.get("autoProxyUsername")
            profile["proxy"]["password"] = profile.get("autoProxyPassword")

        if not proxy or proxy.get("mode") == "none":
            print("no proxy")
            proxy = None

        if proxy and proxy.get("mode") == "geolocation":
            proxy["mode"] = "http"

        if proxy and proxy.get("mode") == None:
            proxy["mode"] = "http"

        self.proxy = proxy
        self.profile_name = profile.get("name")
        if self.profile_name == None:
            print("empty profile name")
            print("profile=", profile)
            exit()

        gologin = self.getGologinPreferences(profile)
        if self.credentials_enable_service != None:
            preferences["credentials_enable_service"] = self.credentials_enable_service
        preferences["gologin"] = gologin
        pfile = open(pref_file, "w")
        json.dump(preferences, pfile)

    def createStartup(self):
        print("createStartup", self.profile_path)
        if self.local is False and os.path.exists(self.profile_path):
            try:
                shutil.rmtree(self.profile_path)
            except:
                print("error removing profile", self.profile_path)
        self.profile = self.getProfile()
        if self.local is False:
            self.downloadProfileZip()
        self.updatePreferences()

        print("writeCookiesFromServer", self.writeCookiesFromServer)
        if self.writeCookiesFromServer:
            self.downloadCookies()
            print("cookies downloaded")

        print("profile_path", self.profile_path)
        return self.profile_path

    def downloadCookies(self):
        api_base_url = API_URL
        access_token = self.access_token

        cookiesManagerInst = CookiesManager(
            profile_id=self.profile_id, tmpdir=self.tmpdir
        )

        try:
            response = requests.get(
                f"{api_base_url}/browser/{self.profile_id}/cookies",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "user-agent": "Selenium-API",
                },
            )

            cookies = response.json()
            print("COOKIES LENGTH", len(cookies))
            cookiesManagerInst.write_cookies_to_file(cookies)
        except Exception as e:
            print("downloadCookies exc", e, e.__traceback__.tb_lineno)
            raise e

    def uploadCookies(self, cookies):
        api_base_url = API_URL
        access_token = self.access_token

        try:
            response = requests.post(
                f"{api_base_url}/browser/{self.profile_id}/cookies/?encrypted=true",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "User-Agent": "Selenium-API",
                },
                json=cookies,
            )
            return response
        except Exception as e:
            print("uploadCookies", e)
            return e

    def headers(self):
        return {
            "Authorization": "Bearer " + self.access_token,
            "User-Agent": "Selenium-API",
        }

    def getRandomFingerprint(self, options):
        os_type = options.get("os", "lin")
        return json.loads(
            requests.get(
                API_URL + "/browser/fingerprint?os=" + os_type, headers=self.headers()
            ).content.decode("utf-8")
        )

    def profiles(self):
        return json.loads(
            requests.get(
                API_URL + "/browser/v2", headers=self.headers()
            ).content.decode("utf-8")
        )

    def createProfileRandomFingerprint(self, options={}):
        response = json.loads(
            requests.post(
                API_URL + "/browser/quick", headers=self.headers(), json=options
            ).content.decode("utf-8")
        )
        return response

    def create(self, options={}):
        profile_options = self.getRandomFingerprint(options)
        navigator = options.get("navigator")
        if options.get("navigator"):
            resolution = navigator.get("resolution")
            userAgent = navigator.get("userAgent")
            language = navigator.get("language")
            hardwareConcurrency = navigator.get("hardwareConcurrency")
            deviceMemory = navigator.get("deviceMemory")

            if resolution == "random" or userAgent == "random":
                options.pop("navigator")
            if resolution != "random" and userAgent != "random":
                options.pop("navigator")
            if resolution == "random" and userAgent != "random":
                profile_options["navigator"]["userAgent"] = userAgent
            if userAgent == "random" and resolution != "random":
                profile_options["navigator"]["resolution"] = resolution
            if resolution != "random" and userAgent != "random":
                profile_options["navigator"]["userAgent"] = userAgent
                profile_options["navigator"]["resolution"] = resolution
            if (
                hardwareConcurrency != "random"
                and userAgent != "random"
                and hardwareConcurrency != None
            ):
                profile_options["navigator"]["hardwareConcurrency"] = (
                    hardwareConcurrency
                )
            if (
                deviceMemory != "random"
                and userAgent != "random"
                and deviceMemory != None
            ):
                profile_options["navigator"]["deviceMemory"] = deviceMemory

            profile_options["navigator"]["language"] = language

        logging.debug("fonts", profile_options.get("fonts"))
        profile = {
            "name": "default_name",
            "notes": "auto generated",
            "browserType": "chrome",
            "os": "lin",
            "googleServicesEnabled": True,
            "lockEnabled": False,
            "audioContext": {"mode": "noise"},
            "canvas": {"mode": "noise"},
            "webRTC": {
                "mode": "disabled",
                "enabled": False,
                "customize": True,
                "fillBasedOnIp": True,
            },
            "fonts": {"families": profile_options.get("fonts")},
            "navigator": profile_options.get("navigator", {}),
            "profile": json.dumps(profile_options),
        }

        if options.get("storage"):
            profile["storage"] = options.get("storage")

        for k, v in options.items():
            profile[k] = v

        response = json.loads(
            requests.post(
                API_URL + "/browser", headers=self.headers(), json=profile
            ).content.decode("utf-8")
        )
        if not (response.get("statusCode") is None):
            raise ProtocolException(response)
        return response.get("id")

    def delete(self, profile_id=None):
        profile = self.profile_id if profile_id == None else profile_id
        requests.delete(API_URL + "/browser/" + profile, headers=self.headers())

    def update(self, options):
        self.profile_id = options.get("id")
        profile = self.getProfile()
        # print("profile", profile)
        for k, v in options.items():
            profile[k] = v
        resp = requests.put(
            API_URL + "/browser/" + self.profile_id,
            headers=self.headers(),
            json=profile,
        ).content.decode("utf-8")
        # print("update", resp)
        # return json.loads(resp)

    def waitDebuggingUrl(self, delay_s, remote_orbita_url, try_count=3):
        url = remote_orbita_url + "/json/version"
        wsUrl = ""
        try_number = 1
        while wsUrl == "":
            time.sleep(delay_s)
            try:
                response = json.loads(requests.get(url).content)
                wsUrl = response.get("webSocketDebuggerUrl", "")
            except:
                pass
            if try_number >= try_count:
                return {"status": "failure", "wsUrl": wsUrl}
            try_number += 1

        remote_orbita_url_without_protocol = remote_orbita_url.replace("https://", "")
        wsUrl = wsUrl.replace("ws://", "wss://").replace(
            "127.0.0.1", remote_orbita_url_without_protocol
        )

        return {"status": "success", "wsUrl": wsUrl}

    def startRemote(self, delay_s=3):
        responseJson = requests.post(
            API_URL + "/browser/" + self.profile_id + "/web",
            headers=self.headers(),
            json={
                "isNewCloudBrowser": self.is_new_cloud_browser,
                "isHeadless": self.is_cloud_headless,
            },
        ).content.decode("utf-8")
        response = json.loads(responseJson)
        print("profileResponse", response)

        remote_orbita_url = "https://" + self.profile_id + ".orbita.gologin.com"
        if self.is_new_cloud_browser:
            if not response["remoteOrbitaUrl"]:
                raise Exception("Couldn' start the remote browser")
            remote_orbita_url = response["remoteOrbitaUrl"]

        return self.waitDebuggingUrl(delay_s, remote_orbita_url=remote_orbita_url)

    def stopRemote(self):
        response = requests.delete(
            API_URL + "/browser/" + self.profile_id + "/web",
            headers=self.headers(),
            params={"isNewCloudBrowser": self.is_new_cloud_browser},
        )

    def clearCookies(self, profile_id=None):
        self.cleaningLocalCookies = True

        profile = self.profile_id if profile_id == None else profile_id
        resp = requests.post(
            API_URL + "/browser/" + profile + "/cookies?cleanCookies=true",
            headers=self.headers(),
            json=[],
        )

        if resp.status_code == 204:
            return {"status": "success"}
        else:
            return {"status": "failure"}

    async def normalizePageView(self, page):
        if self.preferences.get("screenWidth") == None:
            self.profile = self.getProfile()
            self.preferences["screenWidth"] = int(
                self.profile.get("navigator").get("resolution").split("x")[0]
            )
            self.preferences["screenHeight"] = int(
                self.profile.get("navigator").get("resolution").split("x")[1]
            )
        width = self.preferences.get("screenWidth")
        height = self.preferences.get("screenHeight")
        await page.setViewport({"width": width, "height": height})


def getRandomPort():
    while True:
        port = random.randint(1000, 35000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", port))
        if result == 0:
            continue
        else:
            return port

        sock.close()
