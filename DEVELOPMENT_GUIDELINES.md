# DEVELOPMENT_GUIDELINES.md

## Development Philosophy

This project follows professional software engineering practices with a focus on learning and understanding. Every component will be built step-by-step with clear explanations of design decisions and architectural choices.

## Code Quality Standards

### Writing Style
- No excessive print statements or debug output in production code
- No emojis in code, comments, or documentation
- Avoid "AI-like" syntax or overly clever constructs
- Write code as if for a professional production environment
- Use clear, descriptive variable and function names

### Architecture Principles
- **Single Responsibility**: Each module, class, and function has one clear purpose
- **Separation of Concerns**: Business logic, API layer, and data access are clearly separated
- **Dependency Injection**: Avoid tight coupling between components
- **Interface Segregation**: Define clear contracts between components
- **Open/Closed Principle**: Components should be extensible without modification

### Code Structure
- **Modularity**: Break functionality into focused, reusable components
- **Type Safety**: Use Python type hints consistently throughout
- **Error Handling**: Implement proper exception handling without cluttering code
- **Documentation**: Write clear docstrings for all public functions and classes
- **Testing**: Each component should be easily testable in isolation

## Development Process

### Step-by-Step Approach
1. **Planning Phase**: Discuss what we're building and why it's needed
2. **Design Phase**: Define component interfaces and data flow
3. **Implementation Phase**: Write clean, well-structured code
4. **Testing Phase**: Validate functionality with appropriate tests
5. **Integration Phase**: Connect new components with existing system
6. **Review Phase**: Discuss implementation and extract learning points

### Learning Focus
- Explain the reasoning behind each architectural decision
- Discuss alternative approaches and trade-offs considered
- Show how industry patterns and best practices are applied
- Connect theoretical concepts to practical implementation
- Highlight how components work together in the larger system

### Code Review Standards
- Every piece of code should be self-explanatory
- Complex logic should be broken down into smaller, understandable parts
- Use meaningful names that convey intent and purpose
- Keep functions focused and under 20-30 lines when possible
- Group related functionality into coherent modules

## Technical Standards

### Python Style
- Follow PEP 8 style guidelines strictly
- Use black for code formatting
- Maximum line length: 88 characters
- Use meaningful imports (avoid wildcard imports)
- Order imports: standard library, third-party, local imports

### Dependencies
- Minimize external dependencies
- Choose well-maintained, popular libraries
- Document why each dependency is necessary
- Pin dependency versions for reproducibility

### Error Handling
- Use specific exception types rather than generic Exception
- Handle errors at appropriate abstraction levels
- Provide meaningful error messages
- Log errors appropriately without cluttering output

### Performance Considerations
- Write clear code first, optimize later if needed
- Use appropriate data structures for the task
- Consider memory usage for large data processing
- Profile code when performance is critical

## Project Organization

### File Structure
- Keep related functionality together in modules
- Use clear, descriptive directory names
- Separate configuration from implementation
- Keep test files organized parallel to source structure

### Documentation
- README should always be up-to-date with current functionality
- Include docstrings for all public interfaces
- Document complex algorithms and business logic
- Maintain API documentation as code evolves

### Version Control
- Make small, focused commits with clear messages
- Use descriptive commit messages explaining the "why"
- Keep the commit history clean and meaningful

## Learning Objectives

### Understanding Goals
- Learn modern Python development practices
- Understand RESTful API design principles
- Master modular software architecture
- Practice professional code organization
- Learn industry-standard testing approaches

### Skill Development
- Build production-quality Python applications
- Work with modern development tools (FastAPI, UV, Docker)
- Implement clean architecture patterns
- Practice test-driven development
- Learn deployment and containerization

## Quality Gates

### Before Moving Forward
- Code passes all linting and type checking
- All tests pass and provide meaningful coverage
- Code is properly documented
- Component interfaces are clearly defined
- Integration points work as expected

### Code Review Checklist
- Is the code easy to understand and maintain?
- Are the naming conventions clear and consistent?
- Is error handling appropriate and comprehensive?
- Are the components properly isolated and testable?
- Does the implementation match the stated requirements?

This document serves as our north star for building a professional, maintainable, and educational CV evaluation system. Every decision should align with these principles, ensuring we create both a high-quality product and a valuable learning experience.