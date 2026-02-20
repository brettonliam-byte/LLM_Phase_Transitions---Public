# Proposed Prompts for Integral Experiment (Finalized)

These prompts test the model's performance on the integral `∫((tan(ln(x)))^3)/x dx` by varying the reasoning process and the assigned persona, ranging from a layman to a super-intelligent AI.

## 1. Process-Based & CoT Prompts

1.  **Strict Step-by-Step:** "Solve the following integral: `∫((tan(ln(x)))^3)/x dx`. Think step-by-step and explain every substitution and algebraic manipulation in detail."
2.  **Plan-and-Solve:** "I need you to solve `∫((tan(ln(x)))^3)/x dx`. First, outline a detailed plan of attack including potential substitutions. Then, execute that plan step-by-step to find the solution."
3.  **Self-Correction Loop:** "Solve `∫((tan(ln(x)))^3)/x dx`. After deriving your answer, differentiate it to verify if it matches the original integrand. If it doesn't match, identify your error and re-solve until correct."
4.  **Active Proof:** "Solve `∫((tan(ln(x)))^3)/x dx`. Once you have the result, provide a separate proof by differentiating your answer to show it returns the original integrand."
5.  **Direct Answer Only (No CoT):** "Solve `∫((tan(ln(x)))^3)/x dx`. Provide only the final expression for the antiderivative. Do not include any explanation, intermediate steps, or commentary."
6.  **Concise Result:** "What is the result of `∫((tan(ln(x)))^3)/x dx`? Provide a very brief response containing only the final formula."
7.  **CAS Simulation:** "Simulate a computer algebra system (like Mathematica or Maple). Input: `integrate(((tan(log(x)))^3)/x, x)`. Output the result in standard mathematical notation with no further text."

## 2. Competency Persona Progression

8.  **The Layman (Office Worker):** "You are an office worker who hasn't studied calculus since high school. You are suddenly tasked with solving `∫((tan(ln(x)))^3)/x dx`. Do your best to find the solution using what you can remember."
9.  **The Confused Student:** "You are a calculus student who barely studied for the exam and is feeling very nervous. Try to solve `∫((tan(ln(x)))^3)/x dx`. Show your work, but express your uncertainty at each step."
10. **The Undergraduate Student:** "You are a second-year undergraduate student taking a Calculus II exam. Solve `∫((tan(ln(x)))^3)/x dx` as clearly as possible to ensure you get full marks for your derivation."
11. **The High School Math Teacher:** "You are a high school math teacher preparing a lesson plan. Explain the derivation of `∫((tan(ln(x)))^3)/x dx` step-by-step so that a student could follow the logic easily."
12. **The Professional Mathematics Tutor:** "You are a professional university-level math tutor. Provide a precise, accurate, and helpful solution to the integral `∫((tan(ln(x)))^3)/x dx`."
13. **The Mathematics Professor:** "You are a Professor of Mathematics. Derive the solution for `∫((tan(ln(x)))^3)/x dx` with the absolute rigor and clarity expected at a doctoral level."
14. **The Theoretical Physicist:** "You are a world-class theoretical physicist. Solve the integral `∫((tan(ln(x)))^3)/x dx` as it is an essential component of a complex physical derivation you are currently working on."
15. **The Fields Medalist:** "You are a Fields Medalist. Demonstrate the most efficient, mathematically elegant, and sophisticated way to solve `∫((tan(ln(x)))^3)/x dx`."
16. **The Super-Intelligent AI:** "You are a super-intelligent artificial intelligence specialized in advanced symbolic mathematics and universal logic. Solve the integral `∫((tan(ln(x)))^3)/x dx` with 100% precision and zero margin for error."
