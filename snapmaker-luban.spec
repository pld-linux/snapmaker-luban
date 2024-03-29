# TODO: try not to use prebuilt binaries
Summary:	Easy-to-use 3-in-1 software tailor-made for Snapmaker machines
Summary(pl.UTF-8):	Łatwe w użyciu oprogramowanie "trzy w jednym do obrabiarek Snapmaker
Name:		snapmaker-luban
Version:	4.10.2
Release:	3
License:	AGPL v3
Group:		Applications/Engineering
Source0:	https://github.com/Snapmaker/Luban/releases/download/v%{version}/%{name}-%{version}-linux-x64.tar.gz
# Source0-md5:	327125f188ac897333ac5eb814c17012
Source2:	%{name}.desktop
Source3:	%{name}.png
URL:		https://snapmaker.com/
BuildRequires:	ImageMagick
BuildRequires:	rpmbuild(macros) >= 1.747
Obsoletes:	snapmakerjs < 3
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		no_install_post_check_shebangs	1
%define		_enable_debug_packages	0

%description
Snapmaker Luban is an easy-to-use 3-in-1 software tailor-made for
Snapmaker machines. You can customize the printer settings and control
the machine using the command panel in Luban anytime with ease.
The software also provides G-code generation support for 3D models,
laser engraving / cutting, and CNC milling.

%description -l pl.UTF-8
Snapmaker Luban to łatwe w użyciu oprogramowanie "trzy w jednym"
skrojone pod obrabiarki Snapmaker. Pozwala łatwo, w dowolnej chwili
dostosowywać ustawienia drukarki i sterować obrabiarką z panelu
poleceń Luban. Oprogramowanie zapewnia także generowanie G-kodu do
modeli 3D, laserowe rzeźbienie i cięcie oraz frezowanie CNC.

%prep
%setup -q -T -b0 -n %{name}-%{version}-linux-x64

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_bindir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

cp -a * $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -sr $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

for i in 16 24 32 48 64 96 128 ; do
  install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
  convert -geometry ${i}x${i} %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/%{name}.png
done

# Remove nodejs junk
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/resources/app/node_modules/@serialport/bindings-cpp/prebuilds/{android,darwin,win32}-*
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/resources/app/node_modules/@serialport/bindings-cpp/prebuilds/*-arm*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/resources/app/node_modules/@serialport/bindings-cpp/prebuilds/*/node.napi.musl.node

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

ls -1 locales | \
	%{__sed} -e 's,^\([a-z][a-z]\)\.pak,%lang(\1) %{_libdir}/%{name}/locales/\1.pak,' \
		 -e 's,^\(zh\|pt\)\(-\)\([A-Z][A-Z]\)\.pak,%lang(\1_\3) %{_libdir}/%{name}/locales/\1-\3.pak,' \
		 | grep '%lang' > %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENSE.electron.txt LICENSES.chromium.html
%attr(755,root,root) %{_bindir}/%{name}*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/locales
%{_libdir}/%{name}/locales/en-GB.pak
%{_libdir}/%{name}/locales/en-US.pak
%lang(es) %{_libdir}/%{name}/locales/es-419.pak
%{_libdir}/%{name}/locales/fil.pak
%dir %{_libdir}/%{name}/resources
%dir %{_libdir}/%{name}/resources/app
%dir %{_libdir}/%{name}/resources/app/node_modules
%{_libdir}/%{name}/resources/app/node_modules/@[a-rt-z]*
%{_libdir}/%{name}/resources/app/node_modules/@serialport
%{_libdir}/%{name}/resources/app/node_modules/@socket.io
%dir %{_libdir}/%{name}/resources/app/node_modules/@snapmaker
%dir %{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar
%dir %{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/engine
%dir %{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/engine/Linux
%attr(755,root,root) %{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/engine/Linux/Lunar*
%{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-sacp-sdk
%{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/src
%{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/LICENSE
%{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/package.json
%{_libdir}/%{name}/resources/app/node_modules/@snapmaker/snapmaker-lunar/postinstall.js
%{_libdir}/%{name}/resources/app/node_modules/[a-rt-z]*
%{_libdir}/%{name}/resources/app/node_modules/s[a-mo-z]*
%dir %{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine
%dir %{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/engine
%dir %{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/engine/Linux
%attr(755,root,root) %{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/engine/Linux/LubanEngine
%{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/lib
%{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/LICENSE
%{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/package.json
%{_libdir}/%{name}/resources/app/node_modules/snapmaker-luban-engine/postinstall.js
%{_libdir}/%{name}/resources/app/resources
%{_libdir}/%{name}/resources/app/src
%{_libdir}/%{name}/resources/app/*.json
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.json
%{_libdir}/%{name}/*.pak
%attr(755,root,root) %{_libdir}/%{name}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/chrome_crashpad_handler
%attr(755,root,root) %{_libdir}/%{name}/chrome-sandbox
%attr(755,root,root) %{_libdir}/%{name}/libEGL.so
%attr(755,root,root) %{_libdir}/%{name}/libffmpeg.so
%attr(755,root,root) %{_libdir}/%{name}/libGLESv2.so
%attr(755,root,root) %{_libdir}/%{name}/libvk_swiftshader.so
%attr(755,root,root) %{_libdir}/%{name}/libvulkan.so.1
%dir %{_libdir}/%{name}/swiftshader
%attr(755,root,root) %{_libdir}/%{name}/swiftshader/libEGL.so
%attr(755,root,root) %{_libdir}/%{name}/swiftshader/libGLESv2.so
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/%{name}.png
