package main

import (
    "fmt"
)

// Define a struct called "Person"
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

// Define a method called "FullName" for the "Person" struct
func (p Person) FullName() string {
    return p.FirstName + " " + p.LastName
}

type Shape interface {
    Area() float64
}

// Define another struct called "Employee" that embeds "Person"
type Employee struct {
    Person // Embedded "Person" struct
    EmployeeID int
}

// Define a method called "PrintEmployeeInfo" for the "Employee" struct
func (e Employee) PrintEmployeeInfo() {
    fmt.Printf("Employee ID: %d\n", e.EmployeeID)
    fmt.Printf("Full Name: %s\n", e.FullName()) // Accessing the method from the embedded struct
}

func main() {
    // Create an instance of "Employee" and initialize its fields
    employee := Employee{
        Person: Person{
            FirstName: "John",
            LastName:  "Doe",
            Age:       30,
        },
        EmployeeID: 12345,
    }

    // Access methods and fields of the "Employee" struct
    fmt.Println("Employee Information:")
    employee.PrintEmployeeInfo()
}
