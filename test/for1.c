int main(int argc, char** argv) {
    int j = 0;
    for(int i = 0; i < 10; i++) {
        j += i;
    }
    // expected-return:45
    return j;
}
