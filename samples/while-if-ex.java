class WhileIFExample {
    public static void main(String[] args) {
        int x;
        x = 5;
        System.out.println(x);
        if (5) {
            System.out.println(1);
        } else {
            System.out.println(0);
        }
        int i;
        i = 0;
        while (5) {
            System.out.println(i);
            i = i + 1;
        }
        return 0;
    }
}