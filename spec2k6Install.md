# Config and Compile SPEC2006

Author: Yicheng Wang Date: 01/03/2019

## Prepare the spec2k6.tar.gz

```bash
# unzip
tar -xvzf spec2k6.tar.gz
# grant read and write access
sudo chmod -R 755 */
```

## Configure the .cfg file
```bash
cd  spec2k6/config
cp linux64-amd64-gcc41.cfg default.cfg
vim default.cfg
```

### default.cfg modify

* Set the compiler
```bash
# line 54-56 change to
CC           = /usr/bin/gcc
CXX          = /usr/bin/g++
FC           = /usr/bin/gfortran

# line 94-96 change to
COPTIMIZE = -O2 -static
CXXOPTIMIZE = -O2 -static
FOPTIMIZE = -O2 -static
```

## Build benchmarks
```bash
# Make sure Checksums are all okay
cd ~/Research/spec2k6
./install.sh
source shrc

# test build
runspec --config=default.cfg --action=build --tune=base bzip2
# run the benchmark on test data set
runspec --config=default.cfg --size=test --noreportable --tune=base --iterations=1 bzip2
# run the benchmark on full data set
runspec --config=default.cfg --size=ref --noreportable --tune=base --iterations=3 bzip2

# if above three test completed, we are ready to build the whole suite
# we first clean the build and run from the next section
# the iterations number set to 3 in case of faliure
runspec --config=default.cfg --action=build --tune=base all
runspec --config=default.cfg --size=ref --noreportable --tune=base --iterations=3 all
```
Only around 26 benchmarks can be built. It's fine on this stage.

## Remove build and run
```bash
rm -Rf $SPEC/benchspec/C*/*/exe
rm -Rf $SPEC/benchspec/C*/*/run
```