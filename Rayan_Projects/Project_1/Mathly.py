#The way I call the web application is by giving the location of the file at the terminal first
#Then I use streamlit run Mathly.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq, solve
from numpy import sin, cos, tan, exp, log, sqrt

#1. Solve equations
def solve_equations(equation):
    try:
        equation = equation.replace("^", "**")
        equation = equation.replace(" ", "")
        equation = equation.replace("x", "*x").replace("*x*", "x*")
        for i in range(10):
            equation = equation.replace(f"{i}x", f"{i}*x")  # Implicit multiplication
        if "=" not in equation:
            return "Error: The equation must contain an '=' sign."
        lhs, rhs = equation.split("=")
        x = symbols('x')
        eqn = Eq(eval(lhs), eval(rhs))
        soln = solve(eqn, x)
        return f"Solution: {soln}"
    except Exception as e:
        return f"Error: {e}"

#2. Matrix operations
def matrix_operations(m1, m2=None, operation=None):
    try:
        if operation == "multiply":
            if m2 is None:
                return "Error: You need two matrices for multiplication."
            result = np.dot(m1, m2)
            return result
        elif operation == "determinant":
            if m1.shape[0] != m1.shape[1]:
                return "Error: Determinants require square matrices."
            det = np.linalg.det(m1)
            return det
        elif operation == "inverse":
            if m1.shape[0] != m1.shape[1]:
                return "Error: Inversion requires square matrices."
            inverse = np.linalg.inv(m1)
            return inverse
        else:
            return "Invalid operation. Choose 'multiply', 'determinant', or 'inverse'."
    except Exception as e:
        return f"Error: {e}"

#3. Statistical operations
def statistics_operations(data):
    try:
        data = list(map(float, data.split()))
        mean = np.mean(data)
        median = np.median(data)
        std_dev = np.std(data)

        # Plot histogram
        fig, ax = plt.subplots()
        ax.hist(data, bins=10, edgecolor='black')
        ax.set_title("Data Distribution")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        return f"Mean: {mean}, Median: {median}, Standard Deviation: {std_dev}"
    except Exception as e:
        return f"Error: {e}"

#4. Plot Mathematical Functions
def plot_function(equation):
    try:
        x = np.linspace(-10, 10, 400)
        y = eval(equation)

        # Plot the function
        fig, ax = plt.subplots()
        ax.plot(x, y, label=f"y = {equation}")
        ax.set_title("Graph of the Function")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
        return "Graph plotted successfully."
    except Exception as e:
        return f"Error: {e}"

# Streamlit Application
st.title("Mathly")
st.sidebar.title("Mathly Features")
menu = st.sidebar.radio(
    "Choose a Feature",
    ["Solve Equation", "Plot Function", "Statistics", "Matrix Operations"]
)

if menu == "Solve Equation":
    st.header("Solve a Mathematical Equation")
    equation = st.text_input("Enter an equation:")
    if st.button("Solve"):
        result = solve_equations(equation)
        if "Error" in result:
            st.error(result)
        else:
            st.success(result)

elif menu == "Plot Function":
    st.header("Plot a Mathematical Function")
    function = st.text_input("Enter a function of x:")
    if st.button("Plot"):
        result = plot_function(function)
        if "Error" in result:
            st.error(result)
        else:
            st.success(result)

elif menu == "Statistics":
    st.header("Perform Statistical Operations")
    data = st.text_input("Enter numbers separated by spaces:")
    if st.button("Analyze"):
        result = statistics_operations(data)
        if "Error" in result:
            st.error(result)
        else:
            st.success(result)

elif menu == "Matrix Operations":
    st.header("Matrix Operations")
    st.write("Enter values for a 2x2 matrix (Matrix 1):")
    matrix1 = [
        [st.number_input("Matrix 1: Row 1 Col 1", value=0.0), st.number_input("Matrix 1: Row 1 Col 2", value=0.0)],
        [st.number_input("Matrix 1: Row 2 Col 1", value=0.0), st.number_input("Matrix 1: Row 2 Col 2", value=0.0)]
    ]
    operation = st.selectbox("Choose an operation", ["multiply", "determinant", "inverse"])
    matrix2 = None
    if operation == "multiply":
        st.write("Enter values for another 2x2 matrix (Matrix 2):")
        matrix2 = [
            [st.number_input("Matrix 2: Row 1 Col 1", value=0.0), st.number_input("Matrix 2: Row 1 Col 2", value=0.0)],
            [st.number_input("Matrix 2: Row 2 Col 1", value=0.0), st.number_input("Matrix 2: Row 2 Col 2", value=0.0)]
        ]
    if st.button("Calculate"):
        result = matrix_operations(np.array(matrix1), np.array(matrix2) if matrix2 else None, operation)
        if isinstance(result, str) and "Error" in result:
            st.error(result)
        elif operation == "determinant" or operation == "inverse":
            st.success(f"Result: {result}")
        else:
            st.write("Result:")
            st.dataframe(result)