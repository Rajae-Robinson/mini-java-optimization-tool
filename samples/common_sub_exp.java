class CommonSubexpressionEliminationExample {
    public static void main(String[] args) {
        int a = 5 * 3;
        int b = 2 + 5 * 3;
        int c = a * 2 + 5 * 3;
        System.out.println(c);
        
        int d = a * 2 + 5 * 3;
        System.out.println(d);
    }
}

