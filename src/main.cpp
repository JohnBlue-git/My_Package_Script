#include <iostream>
#include <cstdlib>  // for system()
using namespace std;

int main() {
    int exit_code = system("./pacakge.sh ... not yet complete");

    if (exit_code == -1) {
        cerr << "Failed to run script." << endl;
        return 1;
    }

    // Extract actual exit status from system()
    int status = WEXITSTATUS(exit_code);
    cout << "Script exited with code: " << status << endl;

    if (status != 0) {
        cerr << "Script failed with non-zero exit code." << endl;
        return status;
    }

    cout << "Script ran successfully." << endl;
    return 0;
}
