[app]
# الهوية الوطنية الشامخة
title = Ain Mara Geography Library
package.name = amgeoatlas
package.domain = org.belal
source.dir = .
source.include_exts = py,png,jpg,ttf
# شمولية الكتيبة الـ 114 والخرائط والزر العملاق
source.include_patterns = books/*/*, Maps/*, owl.png
version = 1.0
requirements = python3,kivy==2.2.1,pillow,jnius,android
# الضربة القاضية للتدوير المقلوب (وضع الطول فقط)
orientation = portrait
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
# منع ضغط الصور للحفاظ على وضوح "رؤية الصقر"
android.no_compress = .jpg, .png
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
