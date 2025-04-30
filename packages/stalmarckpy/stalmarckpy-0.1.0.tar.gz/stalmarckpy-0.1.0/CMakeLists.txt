cmake_minimum_required(VERSION 3.15...3.26)
project(stalmarckpy LANGUAGES CXX)

# Find Python and pybind11
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

# Set source directories
set(STALMARCK_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")

# Build the core library
add_library(stalmarck STATIC
    "${STALMARCK_SOURCE_DIR}/core/formula.cpp"
    "${STALMARCK_SOURCE_DIR}/core/stalmarck.cpp"
    "${STALMARCK_SOURCE_DIR}/parser/parser.cpp"
    "${STALMARCK_SOURCE_DIR}/solver/solver.cpp"
)

target_include_directories(stalmarck PUBLIC 
    "${STALMARCK_SOURCE_DIR}"
)

# Create the Python module
pybind11_add_module(_stalmarckpy stalmarckpy_bindings.cpp)
target_link_libraries(_stalmarckpy PRIVATE stalmarck)

# Set installation paths
install(TARGETS _stalmarckpy 
    DESTINATION stalmarckpy
    COMPONENT python_modules
)

install(FILES stalmarckpy/__init__.py 
    DESTINATION stalmarckpy
    COMPONENT python_modules
)