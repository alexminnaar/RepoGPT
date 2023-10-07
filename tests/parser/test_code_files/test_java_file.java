// Using a class declaration
class RectangleClass {
    double length;
    double width;

    RectangleClass(double length, double width) {
        this.length = length;
        this.width = width;
    }

    double calculateArea() {
        return length * width;
    }

    double calculatePerimeter() {
        return 2 * (length + width);
    }
}

// Using a separate function to create an object (Factory function)
class Square {
    double side;

    Square(double side) {
        this.side = side;
    }

    static Square createSquare(double side) {
        return new Square(side);
    }
}

// Using a class with static methods
class CircleStatic {
    double radius;

    CircleStatic(double radius) {
        this.radius = radius;
    }

    static double calculateArea(double radius) {
        return Math.PI * radius * radius;
    }

    static double calculateCircumference(double radius) {
        return 2 * Math.PI * radius;
    }
}

// Using a class with instance methods
class CircleInstance {
    double radius;

    CircleInstance(double radius) {
        this.radius = radius;
    }

    double calculateArea() {
        return Math.PI * radius * radius;
    }

    double calculateCircumference() {
        return 2 * Math.PI * radius;
    }
}

public class Main {
    public static void main(String[] args) {
        // Creating objects and using functions/classes
        RectangleClass rectangle = new RectangleClass(5.0, 3.0);
        Square square = Square.createSquare(4.0);
        CircleStatic circleStatic = new CircleStatic(2.0);
        CircleInstance circleInstance = new CircleInstance(3.0);

        // Calculating and printing results
        System.out.println("Rectangle Area: " + rectangle.calculateArea());
        System.out.println("Square Area: " + calculateSquareArea(square));
        System.out.println("Circle (Static) Area: " + CircleStatic.calculateArea(circleStatic.radius));
        System.out.println("Circle (Instance) Area: " + circleInstance.calculateArea());
    }
}
