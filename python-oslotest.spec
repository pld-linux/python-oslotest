#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Oslo test framework
Summary(pl.UTF-8):	Szkielet testów Oslo
Name:		python-oslotest
# keep 3.x here for python2 support
Version:	3.9.0
Release:	3
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/oslotest/
Source0:	https://files.pythonhosted.org/packages/source/o/oslotest/oslotest-%{version}.tar.gz
# Source0-md5:	b32b2287080f9ff75ba4b20ca68c4c59
Patch0:		oslotest-mock.patch
URL:		https://pypi.org/project/oslotest/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-pbr >= 2.0.0
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-debtcollector >= 1.2.0
BuildRequires:	python-fixtures >= 3.0.0
BuildRequires:	python-mock >= 2.0.0
BuildRequires:	python-mox3 >= 0.20.0
BuildRequires:	python-os-client-config >= 1.28.0
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-stestr >= 2.0.0
BuildRequires:	python-subunit >= 1.0.0
BuildRequires:	python-testtools >= 2.2.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-pbr >= 2.0.0
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-debtcollector >= 1.2.0
BuildRequires:	python3-fixtures >= 3.0.0
BuildRequires:	python3-mox3 >= 0.20.0
BuildRequires:	python3-os-client-config >= 1.28.0
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-stestr >= 2.0.0
BuildRequires:	python3-subunit >= 1.0.0
BuildRequires:	python3-testtools >= 2.2.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-openstackdocstheme >= 1.18.1
BuildRequires:	python3-reno >= 2.5.0
BuildRequires:	sphinx-pdg-2 >= 1.7.0
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Oslo Test framework provides common fixtures, support for
debugging, and better support for mocking results.

%description -l pl.UTF-8
Szkielet testów Oslo dostarcza wspólne wyposażenie, obsługę śledzenia
oraz lepsze wsparcie atrap wyników.

%package -n python3-oslotest
Summary:	Oslo test framework
Summary(pl.UTF-8):	Szkielet testów Oslo
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-oslotest
The Oslo Test framework provides common fixtures, support for
debugging, and better support for mocking results.

%description -n python3-oslotest -l pl.UTF-8
Szkielet testów Oslo dostarcza wspólne wyposażenie, obsługę śledzenia
oraz lepsze wsparcie atrap wyników.

%package apidocs
Summary:	API documentation for Python oslotest module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona oslotest
Group:		Documentation

%description apidocs
API documentation for Python oslotest module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona oslotest.

%prep
%setup -q -n oslotest-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
stestr-2 run
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
stestr-3 run
%endif
%endif

%if %{with doc}
sphinx-build-2 -b html doc/source doc/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/oslotest/tests

for f in oslo_debug_helper oslo_run_cross_tests oslo_run_pre_release_tests ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-2
done
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/oslotest/tests

for f in oslo_debug_helper oslo_run_cross_tests oslo_run_pre_release_tests ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_bindir}/${f}-3
	ln -sf $f-3 $RPM_BUILD_ROOT%{_bindir}/${f}
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/oslo_debug_helper-2
%attr(755,root,root) %{_bindir}/oslo_run_cross_tests-2
%attr(755,root,root) %{_bindir}/oslo_run_pre_release_tests-2
%{py_sitescriptdir}/oslotest
%{py_sitescriptdir}/oslotest-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-oslotest
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/oslo_debug_helper
%attr(755,root,root) %{_bindir}/oslo_debug_helper-3
%attr(755,root,root) %{_bindir}/oslo_run_cross_tests
%attr(755,root,root) %{_bindir}/oslo_run_cross_tests-3
%attr(755,root,root) %{_bindir}/oslo_run_pre_release_tests
%attr(755,root,root) %{_bindir}/oslo_run_pre_release_tests-3
%{py3_sitescriptdir}/oslotest
%{py3_sitescriptdir}/oslotest-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,contributor,install,reference,user,*.html,*.js}
%endif
