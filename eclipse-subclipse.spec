%define eclipse_name       eclipse
%define eclipse_base       %{_libdir}/%{eclipse_name}
%define install_loc        %{_datadir}/eclipse/dropins
%define javahl_plugin_name org.tigris.subversion.clientadapter.javahl_1.5.4.1

Summary:	Subversion Eclipse plugin
Name:		eclipse-subclipse
Version:	1.4.7
Release:	0.1
License:	EPL and CC-BY
Group:		Development/Tools
URL:		http://subclipse.tigris.org/
Source0:	subclipse-%{version}.tgz
# Source0-md5:	1b291cd89a7c51b343cfcf863fc1793c
Source10:	%{name}.sh
Patch0:		%{name}-dependencies.patch
BuildRequires:	ant
BuildRequires:	coreutils
BuildRequires:	eclipse-gef
BuildRequires:	eclipse-pde
BuildRequires:	eclipse-svnkit >= 1.2.2
BuildRequires:	jpackage-utils >= 0:1.6
BuildRequires:	subversion-javahl >= 1.5
Requires:	eclipse-platform
Requires:	eclipse-svnkit >= 1.2.2
Requires:	subversion-javahl >= 1.5
Obsoletes:	eclipse-subclipse-book < 1.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the
Eclipse IDE.

%package graph
Summary:	Subversion Revision Graph
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	eclipse-gef

%description graph
Subversion Revision Graph for Subclipse.

%prep
%setup -q -n subclipse-%{version}
%patch0 -p1

# remove javahl sources
rm -rf org.tigris.subversion.clientadapter.javahl/src/org/tigris/subversion/javahl
ln -s %{_javadir}/svn-javahl.jar org.tigris.subversion.clientadapter.javahl

# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r//' org.tigris.subversion.subclipse.graph/icons/readme.txt

%build
%{eclipse_base}/buildscripts/pdebuild			\
  -f org.tigris.subversion.clientadapter.feature \
  -o `pwd`/orbitDeps
%{eclipse_base}/buildscripts/pdebuild				   \
  -f org.tigris.subversion.clientadapter.javahl.feature \
  -o `pwd`/orbitDeps
%{eclipse_base}/buildscripts/pdebuild				   \
  -f org.tigris.subversion.clientadapter.svnkit.feature \
  -o `pwd`/orbitDeps									\
  -d svnkit
%{eclipse_base}/buildscripts/pdebuild \
  -f org.tigris.subversion.subclipse  \
  -o `pwd`/orbitDeps
%{eclipse_base}/buildscripts/pdebuild			  \
  -f org.tigris.subversion.subclipse.graph.feature \
  -o `pwd`/orbitDeps							   \
  -d gef

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{install_loc}
installBase=$RPM_BUILD_ROOT%{install_loc}
install -d $installBase

# installing features
install -d $installBase/subclipse-clientadapter
unzip -q -d $installBase/subclipse-clientadapter build/rpmBuild/org.tigris.subversion.clientadapter.feature.zip
install -d $installBase/subclipse-clientadapter-javahl
unzip -q -d $installBase/subclipse-clientadapter-javahl build/rpmBuild/org.tigris.subversion.clientadapter.javahl.feature.zip
install -d $installBase/subclipse-clientadapter-svnkit
unzip -q -d $installBase/subclipse-clientadapter-svnkit build/rpmBuild/org.tigris.subversion.clientadapter.svnkit.feature.zip
install -d $installBase/subclipse
unzip -q -d $installBase/subclipse build/rpmBuild/org.tigris.subversion.subclipse.zip
install -d $installBase/subclipse-graph
unzip -q -d $installBase/subclipse-graph build/rpmBuild/org.tigris.subversion.subclipse.graph.feature.zip

# replacing jar with links to system libraries
rm $installBase/subclipse-clientadapter-javahl/eclipse/plugins/%{javahl_plugin_name}/svn-javahl.jar
ln -s %{_javadir}/svn-javahl.jar $installBase/subclipse-clientadapter-javahl/eclipse/plugins/%{javahl_plugin_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc org.tigris.subversion.subclipse.graph/icons/readme.txt
%{install_loc}/subclipse
%{install_loc}/subclipse-clientadapter*

%files graph
%defattr(644,root,root,755)
%{install_loc}/subclipse-graph
