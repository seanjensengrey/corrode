int main(int argc, char** argv) {
    int j = 4;
    int k = 0;
    for(int i=0; i<10; i++) {
        k = j * i;
    }
    // expected-return:36
    return k;
}
