Summary:	Easy-to-use 3-in-1 software tailor-made for Snapmaker machines
Name:		snapmaker-luban
Version:	3.4.2
Release:	1
License:	AGPL v3
Group:		Applications
Source0:	https://github.com/Snapmaker/Luban/releases/download/v%{version}/%{name}-%{version}-linux-x64.tar.gz
# Source0-md5:	edebbd32e4b3f2f2d3736cabbe8e8967
Source2:	%{name}.desktop
Source3:	%{name}.png
URL:		https://snapmaker.com/
BuildRequires:	ImageMagick
Obsoletes:	snapmakerjs
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

%prep
%setup -q -T -b0 -n %{name}-%{version}-linux-x64

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/%{name},%{_bindir},%{_desktopdir}} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

cp -a * $RPM_BUILD_ROOT%{_libdir}/%{name}
ln -s %{_libdir}/%{name}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

for i in 16 24 32 48 64 96 128 ; do
  install -d $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps
  convert -geometry ${i}x${i} %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/${i}x${i}/apps/%{name}.png
done

cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/256x256/apps

# _install_post_check_shebangs can't cope with filenames with spaces
find $RPM_BUILD_ROOT -name "Apache License.txt" -print0 | xargs -0 %{__rm}

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
%{_libdir}/%{name}/locales/fake-bidi.pak
%{_libdir}/%{name}/locales/fil.pak
%dir %{_libdir}/%{name}/resources
%{_libdir}/%{name}/resources/electron.asar
%dir %{_libdir}/%{name}/resources/app
%{_libdir}/%{name}/resources/app/app
%{_libdir}/%{name}/resources/app/electron-app
%{_libdir}/%{name}/resources/app/node_modules
%{_libdir}/%{name}/resources/app/*.js
%{_libdir}/%{name}/resources/app/*.json
%dir %{_libdir}/%{name}/resources/app/resources
%{_libdir}/%{name}/resources/app/resources/fonts
%dir %{_libdir}/%{name}/resources/app/resources/CuraEngine
%{_libdir}/%{name}/resources/app/resources/CuraEngine/Config
%dir %{_libdir}/%{name}/resources/app/resources/CuraEngine/3.6
%dir %{_libdir}/%{name}/resources/app/resources/CuraEngine/3.6/Linux
%attr(755,root,root) %{_libdir}/%{name}/resources/app/resources/CuraEngine/3.6/Linux/CuraEngine
%{_libdir}/%{name}/resources/app/resources/user-case
%dir %{_libdir}/%{name}/resources/app/server
%{_libdir}/%{name}/resources/app/server/index.js
%dir %{_libdir}/%{name}/resources/app/server/i18n
%lang(cs) %{_libdir}/%{name}/resources/app/server/i18n/cs
%lang(de) %{_libdir}/%{name}/resources/app/server/i18n/de
%lang(en) %{_libdir}/%{name}/resources/app/server/i18n/en
%lang(es) %{_libdir}/%{name}/resources/app/server/i18n/es
%lang(fr) %{_libdir}/%{name}/resources/app/server/i18n/fr
%lang(hu) %{_libdir}/%{name}/resources/app/server/i18n/hu
%lang(it) %{_libdir}/%{name}/resources/app/server/i18n/it
%lang(ja) %{_libdir}/%{name}/resources/app/server/i18n/ja
%lang(pt_BR) %{_libdir}/%{name}/resources/app/server/i18n/pt-br
%lang(ru) %{_libdir}/%{name}/resources/app/server/i18n/ru
%lang(zh_CN) %{_libdir}/%{name}/resources/app/server/i18n/zh-cn
%lang(zh_TW) %{_libdir}/%{name}/resources/app/server/i18n/zh-tw
%{_libdir}/%{name}/resources/app/server/views
%{_libdir}/%{name}/*.dat
%{_libdir}/%{name}/*.bin
%{_libdir}/%{name}/*.pak
%attr(755,root,root) %{_libdir}/%{name}/libffmpeg.so
%attr(755,root,root) %{_libdir}/%{name}/libnode.so
%attr(755,root,root) %{_libdir}/%{name}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*x*/apps/%{name}.png

