typedef struct {
    int x;
    int y;
    char* s;
} point;

int atoi(char* s) {
    return 3;
}

int main(int argc, char** argv) {
    point b = { 1, 2, "3" };
    // expected-return:6
    return b.x + b.y + atoi(b.s);
}
