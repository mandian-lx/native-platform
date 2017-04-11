%{?_javapackages_macros:%_javapackages_macros}
%global debug_package %{nil}

%global namedreltag %{nil}
%global namedversion %{version}%{?namedreltag}

Name:          native-platform
Version:       0.10
Release:       9%{?dist}
Summary:       Java bindings for various native APIs
License:       ASL 2.0
Group:         Development/Java
URL:           https://github.com/adammurdoch/native-platform
Source0:       https://github.com/adammurdoch/native-platform/archive/%{namedversion}.tar.gz
# From Debian
Source4:       %{name}-0.7-Makefile
# Try to load native library from /usr/lib*/native-platform
# instead of extractDir or classpath.
Patch0:        %{name}-0.10-NativeLibraryLocator.patch
# Use generate libraries without arch references
# Add support for arm and other x64 arches
Patch1:        %{name}-0.10-native-libraries-name.patch

# build tools and deps
BuildRequires: java-devel
BuildRequires: javapackages-local
BuildRequires: ncurses-devel
BuildRequires: jopt-simple

%description
A collection of cross-platform Java APIs
for various native APIs.

These APIs support Java 5 and later. Some
of these APIs overlap with APIs available
in later Java versions.

%package javadoc
Summary:       Javadoc for %{name}
BuildArch:     noarch

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
find .  -name "*.jar" -delete
find .  -name "*.class" -delete

%patch0 -p0
%patch1 -p0

cp -p %{SOURCE4} Makefile

chmod 644 readme.md
sed -i 's/\r//' readme.md

# TODO
mv src/curses/cpp/*.cpp src/main/cpp
mv src/shared/cpp/* src/main/cpp

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CPPFLAGS="${CPPFLAGS:-%optflags}" ; export CPPFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
LDFLAGS="${LDFLAGS:-%{ldflags}}"; export LDFLAGS;
%make JAVA_HOME=%{_jvmdir}/java

%mvn_artifact net.rubygrapefruit:%{name}:%{version} build/%{name}.jar
%mvn_file : %{name}

%install
%mvn_install -J build/docs/javadoc
mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm 0755 build/binaries/libnative-platform-curses.so %{buildroot}%{_libdir}/%{name}/
install -pm 0755 build/binaries/libnative-platform.so %{buildroot}%{_libdir}/%{name}/

%files -f .mfiles
%{_libdir}/%{name}
%doc readme.md
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.10-6
- Rebuilt for GCC 5 C++11 ABI change

* Tue Feb 10 2015 gil cattaneo <puntogil@libero.it> 0.10-5
- introduce license macro

* Tue Oct 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-4
- Don't install JAR with embedded DSO
- Include unix_strings.o in DSO

* Tue Oct 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-3
- Restore DSO installed in libdir

* Tue Oct 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-2
- Avoid needles Makefile patching

* Tue Oct 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.10-1
- Fix build
- Re-enable javadoc package
- Fix artifact installation for non-x86 architechures

* Fri Oct 17 2014 gil cattaneo <puntogil@libero.it> 0.10-1
- update to 0.10

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.6.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.3-0.4.rc2
- Use Requires: java-headless rebuild (#1067528)

* Tue Oct 15 2013 gil cattaneo <puntogil@libero.it> 0.3-0.3.rc2
- fix for rhbz#992323
- use make as buildsystem to avoid circular dependencies
- removed arch references from installed native jar

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 gil cattaneo <puntogil@libero.it> 0.3-0.2.rc2
- removed unnecessary references to jpackage-utils and gcc-c++

* Tue Apr 30 2013 gil cattaneo <puntogil@libero.it> 0.3-0.1.rc2
- update to 0.3-rc-2

* Thu Dec 13 2012 gil cattaneo <puntogil@libero.it> 0.2-1
- initial rpm
