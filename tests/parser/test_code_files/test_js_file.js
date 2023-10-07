// Using a class declaration
class Rectangle {
  constructor(length, width) {
    this.length = length;
    this.width = width;
  }

  calculateArea() {
    return this.length * this.width;
  }

  calculatePerimeter() {
    return 2 * (this.length + this.width);
  }
}