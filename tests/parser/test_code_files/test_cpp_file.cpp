#include <iostream>
#include <cmath>

// Using a class declaration
class RectangleClass {
private:
    double length;
    double width;

public:
    RectangleClass(double len, double wid) : length(len), width(wid) {}

    double calculateArea() {
        return length * width;
    }

    double calculatePerimeter() {
        return 2 * (length + width);
    }
};

// Using a separate function to create an object (Factory function)
class Square {
private:
    double side;

public:
    Square(double s) : side(s) {}

    static Square createSquare(double side) {
        return Square(side);
    }
};

double calculateSquareArea(const Square& square) {
    return square.side * square.side;
}

double calculateSquarePerimeter(const Square& square) {
    return 4 * square.side;
}

// Using a class with static member functions
class CircleStatic {
private:
    double radius;

public:
    CircleStatic(double r) : radius(r) {}

    static double calculateArea(double radius) {
        return 3.14159 * radius * radius;
    }

    static double calculateCircumference(double radius) {
        return 2 * 3.14159 * radius;
    }
};

// Using a class with instance member functions
class CircleInstance {
private:
    double radius;

public:
    CircleInstance(double r) : radius(r) {}

    double calculateArea() {
        return 3.14159 * radius * radius;
    }

    double calculateCircumference() {
        return 2 * 3.14159 * radius;
    }
};

int main() {
    // Creating objects and using functions/classes
    RectangleClass rectangle(5.0, 3.0);
    Square square = Square::createSquare(4.0);
    CircleStatic circleStatic(2.0);
    CircleInstance circleInstance(3.0);

    // Calculating and printing results
    std::cout << "Rectangle Area: " << rectangle.calculateArea() << std::endl;
    std::cout << "Square Area: " << calculateSquareArea(square) << std::endl;
    std::cout << "Circle (Static) Area: " << CircleStatic::calculateArea(circleStatic) << std::endl;
    std::cout << "Circle (Instance) Area: " << circleInstance.calculateArea() << std::endl;

    return 0;
}