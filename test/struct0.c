typedef struct {
    int x;
    int y;
} point;

int main(int argc, char** argv) {
    point a;
    a.x = 10;
    a.y = 4;
    // expected-return:14
    return a.x + a.y;
}
