# TODO
# - build from source (see r1.1 of the spec)
Summary:	Subversion Eclipse plugin
Name:		eclipse-subclipse
Version:	1.4.8
Release:	0.1
License:	EPL and CC-BY
Group:		Development/Tools
URL:		http://subclipse.tigris.org/
Source0:	http://subclipse.tigris.org/files/documents/906/45156/site-%{version}.zip
# Source0-md5:	b98324f5669956c7e79422de8c2447b8
Source10:	%{name}.sh
Requires:	eclipse >= 3.3.1.1
#Requires:	eclipse-svnkit >= 1.2.2
#Requires:	subversion-javahl >= 1.5
Obsoletes:	eclipse-subclipse-book < 1.4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		eclipsedir	%{_datadir}/eclipse

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
%setup -qc

rm -f plugins/org.tigris.subversion.clientadapter.javahl.win32*.jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{eclipsedir}/{features,plugins}
cp -a features/* $RPM_BUILD_ROOT%{eclipsedir}/features
cp -a plugins/* $RPM_BUILD_ROOT%{eclipsedir}/plugins

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{eclipsedir}/features/org.tigris.subversion.*
%{eclipsedir}/plugins/org.tigris.subversion.*
# ext deps?
%{eclipsedir}/features/com.sun.jna*.jar
%{eclipsedir}/features/org.tmatesoft.svnkit*.jar
%{eclipsedir}/plugins/com.sun.jna*.jar
%{eclipsedir}/plugins/org.tmatesoft.svnkit*.jar

%if 0
%files graph
%defattr(644,root,root,755)
%{install_loc}/subclipse-graph
%endif
