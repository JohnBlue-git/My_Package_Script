## package.sh
./package.sh
```console
./package.sh
Usage: ./package.sh
 --mode [create|extract]
 --format [gzip]
 --folder <folder the files be extracted to>
 --tarball <input tarball / output tarball>
 --files array<files to be compressed>

Example:
./package.sh --mode create --tarball ./code.tar --files ./main.cpp
./package.sh --mode create --format gzip --tarball ./code.tar.gz --files ./main.cpp
./package.sh --mode extract --tarball ./code.tar --folder ./tmp
./package.sh --mode extract --format gzip --tarball ./code.tar.gz --folder ./tmp

exit code:
 0: success
 1: hit how to use / invalid usage / other fail
 2: tarball or file or follder does not exist
 3: fail to tar command (or is not tarball)
```
how_to_use()
```bash
how_to_use()
{
  echo "Usage: $0"
  echo " --mode [create|extract]"
  echo " --format [gzip]"
  echo " --folder <folder the files be extracted to>"
  echo " --tarball <input tarball / output tarball>"
  echo " --files array<files to be compressed>"
  echo ""
  echo "Example:"
  echo "$0 --mode create --tarball ./code.tar --files ./main.cpp"
  echo "$0 --mode create --format gzip --tarball ./code.tar.gz --files ./main.cpp"
  echo "$0 --mode extract --tarball ./code.tar --folder ./tmp"
  echo "$0 --mode extract --format gzip --tarball ./code.tar.gz --folder ./tmp"
  echo ""
  echo "exit code:"
  echo " 0: success"
  echo " 1: hit how to use / invalid usage / other fail"
  echo " 2: tarball or file or follder does not exist"
  echo " 3: fail to tar command (or is not tarball)"
  exit 1
}
```

## main.cpp
How to work with script in C.
```C++
#include <iostream>
#include <cstdlib>  // for system()

int main() {
    int exit_code = system("./package.sh --mode create --tarball /tmp/code.tar --files ./main.cpp");

    if (exit_code == -1) {
        std::cerr << "Failed to run script." << std::endl;
        return 1;
    }

    // Extract actual exit status from system()
    int status = WEXITSTATUS(exit_code);
    std::cout << "Script exited with code: " << status << std::endl;

    switch (status)
    {
    case 0:
        std::cout << "Pacakge success" << std::endl;
        break;
    case 1:
        std::cerr << "Package fail: hit how to use / invalid usage / other fail" << std::endl;
        break;
    case 2:
        std::cerr << "Package fail: tarball or file or follder does not exist" << std::endl;
        break;
    case 3:
        std::cerr << "Package fail: fail to tar command (or is not tarball)" << std::endl;
        break;
    }
  
    return 0;
}
```
How to build
```console
cd src
g++ main.cpp
./a.ouut
```

## Tests

### Test via pytest
We have provide e2e tests via python scripts (please refer to the follwing README.md and navigate to tests folder)
\
[tests/README.md](tests/README.md)

### Look deeper in my tests desgin
Here, we have two kinds of tests
- tests/test_script_service.py
    - this test the functions of package.sh
- tests/test_script_exitcode.py
    - this test whether the exitcode followed the rules
