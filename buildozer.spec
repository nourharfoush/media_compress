[app]
# (str) Title of your application
title = Harfoush Media Compressor

# (str) Package name
package.name = harfoushcompressor

# (str) Package domain (needed for android/ios packaging)
package.domain = com.harfoush.compressor

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,kivymd,plyer

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (list) Architectures
android.archs = arm64-v8a

# (bool) Enable AndroidX
android.androidx = True

# (bool) Auto accept SDK license
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
