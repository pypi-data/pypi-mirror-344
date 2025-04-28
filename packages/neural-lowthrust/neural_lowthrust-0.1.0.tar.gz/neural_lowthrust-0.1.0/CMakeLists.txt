cmake_minimum_required(VERSION 3.18)
project(nn_lowthrust LANGUAGES CXX)

# ───────────────────── compiler settings ─────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
endif()

if(MSVC)
    add_compile_options(/O2 /Oi /Ot /fp:fast /bigobj /arch:AVX2)
else()
    add_compile_options(-O3 -ffast-math -funroll-loops -march=native -mtune=native)
endif()

# ───────────────────── dependencies ──────────────────────────
# 1) pybind11 – locate it either via add_subdirectory (in-tree) or find_package (system)
if(EXISTS "${PROJECT_SOURCE_DIR}/pybind11/CMakeLists.txt")
    message(STATUS "Using in-tree pybind11")
    add_subdirectory(pybind11)          # after this, targets like pybind11::headers exist
else()
    message(STATUS "Using system pybind11")
    find_package(pybind11 CONFIG REQUIRED)
endif()

# 2) Eigen – header-only copy you placed under src/eigen_nn_lowthrust/Eigen
set(EIGEN_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/src/eigen_nn_lowthrust/Eigen")

# ───────────────────── sources ───────────────────────────────
file(GLOB_RECURSE ALL_CPP CONFIGURE_DEPENDS "src/*.cpp")
list(FILTER ALL_CPP EXCLUDE REGEX "bindings\\.cpp$")
set(CORE_CPP  ${ALL_CPP})
set(PYBIND_CPP src/bindings.cpp)

# ───────────────────── static library ────────────────────────
#add_library(eigen_nn STATIC ${CORE_CPP})
#target_include_directories(eigen_nn
 #   PUBLIC
 #       ${PROJECT_SOURCE_DIR}/src
 #       ${PROJECT_SOURCE_DIR}/src/eigen_nn_lowthrust
#        ${EIGEN_INCLUDE_DIR}
#)

# ---------- C++ header-only core ----------
add_library(eigen_nn INTERFACE)

# Tell whoever links eigen_nn where to find the headers
target_include_directories(eigen_nn INTERFACE
    ${PROJECT_SOURCE_DIR}/src
    ${PROJECT_SOURCE_DIR}/src/eigen_nn_lowthrust
    ${EIGEN_INCLUDE_DIR}
)


# ───────────────────── python extension ──────────────────────
pybind11_add_module(nn_lowthrust ${PYBIND_CPP})

target_link_libraries(nn_lowthrust  PRIVATE eigen_nn)

target_include_directories(nn_lowthrust  PRIVATE
        ${PROJECT_SOURCE_DIR}/src
        ${PROJECT_SOURCE_DIR}/src/eigen_nn_lowthrust
        ${EIGEN_INCLUDE_DIR}
)

# ───────────────────── install (optional) ────────────────────
install(TARGETS nn_lowthrust 
        LIBRARY DESTINATION neural_lowthrust
        RUNTIME DESTINATION neural_lowthrust
        ARCHIVE DESTINATION neural_lowthrust
)
