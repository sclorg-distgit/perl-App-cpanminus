%{?scl:%scl_package perl-App-cpanminus}

Name:           %{?scl_prefix}perl-App-cpanminus
Version:        1.7042
Release:        2%{?dist}
Summary:        Get, unpack, build and install CPAN modules
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/App-cpanminus/
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/App-cpanminus-%{version}.tar.gz
Source1:        fatunpack
BuildArch:      noarch
BuildRequires:  %{_bindir}/podselect
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  %{?scl_prefix}perl(File::Path)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(Getopt::Long)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(warnings)
# Run-time:
# Nothing special. The tests are very poor. But we run perl -c at built-time
# to check for correct unpacking. So we need non-optional run-time
# dependencies at build-time too:
BuildRequires:  %{?scl_prefix}perl(Config)
BuildRequires:  %{?scl_prefix}perl(constant)
# CPAN::DistnameInfo not needed for compilation
# CPAN::Meta not needed for copmilation
# CPAN::Meta::Check not needed for compilation
BuildRequires:  %{?scl_prefix}perl(CPAN::Meta::Requirements)
# CPAN::Meta::YAML not needed for compilation
BuildRequires:  %{?scl_prefix}perl(Cwd)
# Digest::SHA not needed for compilation
# ExtUtils::Manifest not needed for compilation
BuildRequires:  %{?scl_prefix}perl(File::Basename)
BuildRequires:  %{?scl_prefix}perl(File::Copy)
BuildRequires:  %{?scl_prefix}perl(File::Find)
# File::HomeDir not needed for compilation
# File::pushd not needed for compilation
BuildRequires:  %{?scl_prefix}perl(File::Temp)
# HTTP::Tiny not needed for compilation
# JSON::PP not needed for compilation
# local::lib not needed for compilation
# LWP::Protocol::https not needed for compilation
# LWP::UserAgent not needed for compilation
# Module::CoreList not needed for compilation
# Module::CPANfile not needed for compilation
# Module::Metadata not needed for compilation
# Module::Signature not needed for compilation
# Parse::PMFile not needed for compilation
# Safe not needed for compilation
BuildRequires:  %{?scl_prefix}perl(String::ShellQuote)
BuildRequires:  %{?scl_prefix}perl(Symbol)
BuildRequires:  %{?scl_prefix}perl(version)
# version::vpp not needed
# Win32 not used
# YAML not needed for compilation
# Tests:
BuildRequires:  %{?scl_prefix}perl(Test::More)
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
# Current dependency generator cannot parse compressed code. Use PPI to find
# them, and list them manually:
# Archive::Tar is optional
# Archive::Zip is optional
# Compress::Zlib is optional
Requires:       %{?scl_prefix}perl(CPAN::DistnameInfo)
Requires:       %{?scl_prefix}perl(CPAN::Meta)
Requires:       %{?scl_prefix}perl(CPAN::Meta::Check)
Requires:       %{?scl_prefix}perl(CPAN::Meta::YAML)
Requires:       %{?scl_prefix}perl(Digest::SHA)
Requires:       %{?scl_prefix}perl(ExtUtils::Install) >= 1.46
Requires:       %{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.58
Requires:       %{?scl_prefix}perl(ExtUtils::Manifest)
# File::HomeDir is optional
Requires:       %{?scl_prefix}perl(File::pushd)
# HTTP getter by LWP::UserAgent or wget or curl or HTTP::Tiny
Requires:       %{?scl_prefix}perl(HTTP::Tiny)
Requires:       %{?scl_prefix}perl(local::lib)
# LWP::Protocol::https is optional
# LWP::UserAgent is optional
Requires:       %{?scl_prefix}perl(Module::Build) >= 0.38
Requires:       %{?scl_prefix}perl(Module::CoreList)
Requires:       %{?scl_prefix}perl(Module::CPANfile)
Requires:       %{?scl_prefix}perl(Module::Metadata)
# Module::Signature is optional
Requires:       %{?scl_prefix}perl(Parse::PMFile)
Requires:       %{?scl_prefix}perl(Safe)
# version::vpp not used
# Win32 not used
Requires:       %{?scl_prefix}perl(YAML)
# XXX: Keep Provides: cpanminus to allow `yum install cpanminus' instead of
# longer `yum install perl-App-cpanminus'.
Provides:       %{?scl_prefix}cpanminus = %{version}-%{release}
Obsoletes:      %{?scl_prefix}cpanminus <= 1.2002

%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
# Filter under-specified dependencies
%filter_from_provides /^%{?scl_prefix}perl(App::cpanminus)$/d
# Filter private modules
%filter_from_provides /^%{?scl_prefix}perl(ModuleBuildSkipMan)/d
%?perl_default_filter
}
%else
# RPM 4.9 style
# Filter under-specified dependencies
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^%{?scl_prefix}perl\\(App::cpanminus\\)$
# Filter private modules
%global __provides_exclude %{__provides_exclude}|^%{?scl_prefix}perl\\(ModuleBuildSkipMan\\)
%endif

%description
Why? It's dependency free, requires zero configuration, and stands alone 
but it's maintainable and extensible with plug-ins and friendly to shell 
scripting. When running, it requires only 10 MB of RAM.

%prep
%setup -q -n App-cpanminus-%{version}
# Unbundle fat-packed modules
%{?scl:scl enable %{scl} '}podselect lib/App/cpanminus.pm > lib/App/cpanminus.pod%{?scl:'}

for F in bin/cpanm lib/App/cpanminus/fatscript.pm; do
    %{?scl:scl enable %{scl} '}%{SOURCE1} --libdir lib --filter %{?scl:'"}'%{?scl:"'}^App/cpanminus%{?scl:'"}'%{?scl:"'} %{?scl:'}"$F"%{?scl:'} > %{?scl:'}"${F}.stripped"%{?scl:'}%{?scl:'}
    %{?scl:scl enable %{scl} '}perl -c -Ilib %{?scl:'}"${F}.stripped"%{?scl:'}%{?scl:'}
    mv "${F}.stripped" "$F"
done

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_mandir}/man1/*
%{_bindir}/cpanm

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 1.7042-2
- SCL

* Tue Jun 07 2016 Petr Pisar <ppisar@redhat.com> - 1.7042-1
- 1.7042 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.7041-2
- Perl 5.24 rebuild

* Tue May 10 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.7041-1
- 1.7041 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7040-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.7040-1
- 1.7040 bump

* Mon Jun 29 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7039-1
- 1.7039 bump

* Wed Jun 24 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7038-1
- 1.7038 bump

* Fri Jun 19 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7037-1
- 1.7037 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7036-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7036-2
- Perl 5.22 rebuild

* Wed Jun 10 2015 Petr Pisar <ppisar@redhat.com> - 1.7036-1
- 1.7036 bump

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7034-2
- Perl 5.22 rebuild

* Mon May 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7034-1
- 1.7034 bump

* Thu Apr 23 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7031-1
- 1.7031 bump

* Mon Apr 20 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7030-1
- 1.7030 bump

* Tue Feb 17 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.7027-1
- 1.7027 bump

* Mon Feb 09 2015 Petr Pisar <ppisar@redhat.com> - 1.7025-1
- 1.7025 bump

* Tue Dec 16 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7022-1
- 1.7022 bump

* Thu Dec 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7020-1
- 1.7020 bump; README was removed

* Mon Dec 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7019-1
- 1.7019 bump

* Wed Dec 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7018-1
- 1.7018 bump

* Tue Nov 18 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7016-1
- 1.7016 bump

* Wed Oct 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7014-1
- 1.7014 bump

* Mon Sep 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7012-1
- 1.7012 bump

* Tue Sep 23 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7011-1
- 1.7011 bump

* Wed Sep 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7009-1
- 1.7009 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7004-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7004-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.7004-1
- 1.7004 bump
- Updated the script fatunpack (ppisar)

* Wed Sep 11 2013 Petr Pisar <ppisar@redhat.com> - 1.7001-1
- 1.7001 bump

* Wed Sep 11 2013 Petr Pisar <ppisar@redhat.com> - 1.6927-3
- Unbundle all modules (bug #907464)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6927-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.6927-1
- 1.6927 bump

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.6922-2
- Perl 5.18 rebuild

* Fri Jun 21 2013 Petr Pisar <ppisar@redhat.com> - 1.6922-1
- 1.6922 bump

* Thu Jun 20 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.6921-1
- 1.6921 bump

* Thu Jun 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.6918-1
- 1.6918 bump

* Thu May 16 2013 Petr Pisar <ppisar@redhat.com> - 1.6915-1
- 1.6915 bump

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 1.6914-1
- 1.6914 bump

* Mon May 13 2013 Petr Pisar <ppisar@redhat.com> - 1.6913-1
- 1.6913 bump

* Tue May 07 2013 Petr Pisar <ppisar@redhat.com> - 1.6912-1
- 1.6912 bump

* Mon May 06 2013 Petr Pisar <ppisar@redhat.com> - 1.6911-1
- 1.6911 bump

* Thu May 02 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.6909-1
- 1.6909 bump

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 1.6907-1
- 1.6907 bump

* Mon Apr 22 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.6902-1
- 1.6902 bump

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 1.6108-1
- 1.6108 bump

* Mon Apr 08 2013 Petr Pisar <ppisar@redhat.com> - 1.6107-1
- 1.6107 bump

* Mon Apr 08 2013 Petr Pisar <ppisar@redhat.com> - 1.6105-1
- 1.6105 bump

* Wed Apr 03 2013 Petr Pisar <ppisar@redhat.com> - 1.6104-1
- 1.6104 bump

* Thu Mar 28 2013 Petr Pisar <ppisar@redhat.com> - 1.6102-1
- 1.6102 bump

* Tue Mar 26 2013 Petr Pisar <ppisar@redhat.com> - 1.6101-1
- 1.6101 bump

* Wed Mar 20 2013 Petr Pisar <ppisar@redhat.com> - 1.6008-1
- 1.6008 bump

* Thu Mar 14 2013 Petr Pisar <ppisar@redhat.com> - 1.6006-1
- 1.6006 bump

* Mon Mar 11 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.6005-1
- 1.6005 bump

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 1.6002-1
- 1.6002 bump

* Mon Feb  4 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.5021-1
- 1.5021 bump

* Wed Jan 02 2013 Petr Pisar <ppisar@redhat.com> - 1.5019-1
- 1.5019 bump

* Wed Sep 19 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.5018-1
- 1.5018 bump

* Fri Jul 20 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.5017-1
- 1.5017 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.5015-2
- Perl 5.16 rebuild

* Mon Jun 25 2012 Petr Šabata <contyk@redhat.com> - 1.5015-1
- 1.5015 bump

* Wed Jun 13 2012 Petr Šabata <contyk@redhat.com> - 1.5014-1
- 1.5014 bump
- Drop command macros

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.5013-2
- Perl 5.16 rebuild

* Mon May 14 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.5013-1
- 1.5013 bump

* Fri Apr 13 2012 Petr Šabata <contyk@redhat.com> - 1.5011-1
- 1.5011 bump

* Tue Apr 03 2012 Petr Šabata <contyk@redhat.com> - 1.5010-1
- 1.5010 bump

* Mon Mar 19 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.5008-1
- bump to 1.5008

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.5007-1
- 1.5007 bump

* Wed Nov 30 2011 Petr Šabata <contyk@redhat.com> - 1.5006-1
- 1.5006 bump

* Wed Nov 23 2011 Petr Šabata <contyk@redhat.com> - 1.5005-1
- 1.5005 bump
- defattr removed

* Wed Nov 09 2011 Petr Sabata <contyk@redhat.com> - 1.5004-1
- 1.5004 bump

* Wed Oct 19 2011 Petr Sabata <contyk@redhat.com> - 1.5003-1
- 1.5003 bump

* Tue Oct 18 2011 Petr Sabata <contyk@redhat.com> - 1.5002-1
- 1.5002 bump

* Fri Oct 14 2011 Petr Sabata <contyk@redhat.com> - 1.5001-1
- 1.5001 bump

* Thu Oct 13 2011 Petr Sabata <contyk@redhat.com> - 1.5000-1
- 1.5000 bump

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 1.4008-3
- RPM 4.9 dependency filtering added

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4008-2
- Perl mass rebuild

* Thu Jun 16 2011 Petr Pisar <ppisar@redhat.com> - 1.4008-1
- 1.4008 bump

* Wed May 18 2011 Petr Pisar <ppisar@redhat.com> - 1.4007-1
- 1.4007 bump
- LWP is optional since this package bundles HTTP::Tiny. Upstream recognized
  LWP being heavy. Follow upstream decision in RPM package dependencies.

* Tue May 17 2011 Petr Pisar <ppisar@redhat.com> - 1.4006-1
- 1.4006 bump
- Fix obsoleted version string

* Thu May 12 2011 Petr Sabata <psabata@redhat.com> - 1.4005-1
- 1.4005 bump

* Fri Mar 11 2011 Petr Sabata <psabata@redhat.com> - 1.4004-1
- 1.4004 bump

* Thu Mar 10 2011 Petr Pisar <ppisar@redhat.com> - 1.4003-1
- 1.4003 bump

* Tue Mar 08 2011 Petr Pisar <ppisar@redhat.com> - 1.4000-1
- 1.4000 bump

* Fri Mar 04 2011 Petr Pisar <ppisar@redhat.com> - 1.3001-1
- 1.3001 bump

* Thu Mar 03 2011 Petr Pisar <ppisar@redhat.com> - 1.3000-1
- 1.3000 bump
- Clean up spec file
- Require modules needed by cpanm
- Merge cpanminus into main package as cpanminus required main package and
  main package did not contain any code (i.e. was useless).

* Thu Feb 17 2011 Petr Sabata <psabata@redhat.com> - 1.2001-1
- 1.2001 bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> - 1.1008-1
- 1.1008 bump

* Mon Jan 24 2011 Petr Pisar <ppisar@redhat.com> - 1.1007-1
- 1.1007 bump

* Mon Jan  3 2011 Petr Sabata <psabata@redhat.com> - 1.1006-1
- 1.1006 bump

* Thu Dec  2 2010 Petr Sabata <psabata@redhat.com> - 1.1004-1
- 1.1004 bump

* Fri Nov 19 2010 Petr Pisar <ppisar@redhat.com> - 1.1002-1
- 1.1002 bump

* Mon Sep 27 2010 Petr Pisar <ppisar@redhat.com> - 1.0015-1
- 1.0015 bump

* Thu Sep 23 2010 Petr Pisar <ppisar@redhat.com> - 1.0014-1
- 1.0014 bump

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> - 1.0013-1
- 1.0013 bump
- Correct description spelling

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.9935-3
- Mass rebuild with perl-5.12.0

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9935-2
- filter unwanted requires

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9935-1
- update

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9923-1
- update
- create sub-package

* Tue Mar  2 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9911-1
- new version & fix description

* Tue Feb 23 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.09-1
- Specfile autogenerated by cpanspec 1.78.
