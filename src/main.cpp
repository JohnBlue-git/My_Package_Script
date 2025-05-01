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
