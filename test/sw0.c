int main(int argc, char** argv) {
    int input = 3;
    int result;
    // adder switch
    switch(input) {
        case 0:
            result = 1;
            break;
        case 1:
            result = 2;
            break;
        case 2:
            result = 3;
            break;
        case 3:
            result = 4;
            break;
        default:
            result = -1;
    }
    // expected-return:4
    return result;
}
