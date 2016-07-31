typedef struct {
    int x;
    int y;
} point;

int main(int argc, char** argv) {
    point a = { 10, 4 } ;
    // expected-return:14
    return a.x + a.y;
}
