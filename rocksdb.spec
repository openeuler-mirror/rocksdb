Name:          rocksdb
Version:       6.8.1
Release:       1
Summary:       A Persistent Key-Value Store for Flash and RAM Storage
 
License:       GPLv2 and Apache 2.0 License
URL:           https://github.com/facebook/rocksdb.git
 
BuildRequires: gcc make rpm-build gcc-c++ gtest-devel

# enable debuginfo pacakges by default, then we need gdb package
BuildRequires: gdb

# rocksdb recommend installing some compression libraries
BuildRequires: snappy snappy-devel zlib zlib-devel bzip2 bzip2-devel lz4 lz4-devel zstd zstd-devel gflags gflags-devel

Requires:      snappy snappy-devel zlib zlib-devel bzip2 bzip2-devel lz4 lz4-devel zstd zstd-devel gflags gflags-devel
 
Source0:       https://codeload.github.com/facebook/%{name}/tar.gz/v%{version}
Patch0:        rocksdb-6.8.1-install_path.patch
 
%description
Rocksdb is a library that forms the core building block for a fast key value
server, especially suited for storing data on flash drives. It has a
Log-Structured-Merge-Database (LSM) design with flexible trade offs between
Write-Amplification-Factor (WAF), Read-Amplification-Factor (RAF) and
Space-Amplification-Factor (SAF). It has multithreaded compaction, making it
specially suitable for storing multiple terabytes of data in a single database.

%package devel
Summary:       Development files for rocksdb
Requires:      %{name}%{?_isa} = %{version}-%{release}
 
%description devel
Development files for rocksdb
 
 
%prep
%autosetup

rm -rf third-party/gtest-1.8.1
rm java/benchmark/src/main/java/org/rocksdb/benchmark/DbBenchmark.java
rm build_tools/gnu_parallel
 
%build
export CFLAGS="%{optflags}"
export EXTRA_CXXFLAGS=" -std=c++11 %{optflags}"
make %{?_smp_mflags} shared_lib
 
%install
make install-shared \
         INSTALL_PREFIX=%{buildroot}\
         LIB_INSTALL_DIR=%{_libdir}\
         INCLUDE_INSTALL_DIR=%{_includedir}
 
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
 
 
%files
%{_libdir}/librocksdb.so.6
%{_libdir}/librocksdb.so.6.8
%{_libdir}/librocksdb.so.6.8.1
%license COPYING LICENSE.Apache LICENSE.leveldb

 
%files devel
%{_libdir}/librocksdb.so
%{_includedir}/*
 
%changelog
* Thu May 28 2020 openEuler Buildteam <buildteam@openeuler.org> - 6.8.1-1
- Package init
