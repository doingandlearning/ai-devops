#!/bin/bash
# Build Script for C Dependency
# Generated with Copilot Chat - Example for Part 4 Demo
#
# This script demonstrates:
# - Cloning a C dependency
# - Building with CMake
# - Installing to local directory
# - Setting up environment variables
#
# Usage: ./build-dependency.sh [DEPENDENCY_URL] [INSTALL_PREFIX]

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
DEPENDENCY_URL="${1:-https://github.com/example/dependency.git}"
INSTALL_PREFIX="${2:-${HOME}/local}"
DEPENDENCY_NAME=$(basename "${DEPENDENCY_URL}" .git)
BUILD_DIR="build-${DEPENDENCY_NAME}"
CLONE_DIR="${DEPENDENCY_NAME}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error handling
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    command -v git >/dev/null 2>&1 || error_exit "git is required but not installed"
    command -v cmake >/dev/null 2>&1 || error_exit "cmake is required but not installed"
    command -v make >/dev/null 2>&1 || error_exit "make is required but not installed"
    
    echo -e "${GREEN}Prerequisites OK${NC}"
}

# Clone dependency
clone_dependency() {
    echo -e "${YELLOW}Cloning ${DEPENDENCY_NAME}...${NC}"
    
    if [ -d "${CLONE_DIR}" ]; then
        echo -e "${YELLOW}Directory ${CLONE_DIR} exists, updating...${NC}"
        cd "${CLONE_DIR}"
        git pull || error_exit "Failed to update repository"
        cd ..
    else
        git clone "${DEPENDENCY_URL}" "${CLONE_DIR}" || error_exit "Failed to clone repository"
    fi
    
    echo -e "${GREEN}Clone complete${NC}"
}

# Build dependency
build_dependency() {
    echo -e "${YELLOW}Building ${DEPENDENCY_NAME}...${NC}"
    
    cd "${CLONE_DIR}"
    
    # Create build directory
    mkdir -p "${BUILD_DIR}"
    cd "${BUILD_DIR}"
    
    # Configure with CMake
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX="${INSTALL_PREFIX}" \
        -DCMAKE_C_FLAGS="-Wall -Wextra -Werror" \
        -DCMAKE_CXX_FLAGS="-Wall -Wextra -Werror" \
        || error_exit "CMake configuration failed"
    
    # Build
    make -j$(nproc) || error_exit "Build failed"
    
    echo -e "${GREEN}Build complete${NC}"
}

# Install dependency
install_dependency() {
    echo -e "${YELLOW}Installing ${DEPENDENCY_NAME} to ${INSTALL_PREFIX}...${NC}"
    
    cd "${BUILD_DIR}"
    make install || error_exit "Installation failed"
    
    echo -e "${GREEN}Installation complete${NC}"
}

# Set up environment variables
setup_environment() {
    echo -e "${YELLOW}Setting up environment variables...${NC}"
    
    # Create environment setup script
    ENV_SCRIPT="${INSTALL_PREFIX}/env-setup.sh"
    
    cat > "${ENV_SCRIPT}" <<EOF
# Environment setup for ${DEPENDENCY_NAME}
# Source this file: source ${ENV_SCRIPT}

export PATH="${INSTALL_PREFIX}/bin:\$PATH"
export LD_LIBRARY_PATH="${INSTALL_PREFIX}/lib:\$LD_LIBRARY_PATH"
export PKG_CONFIG_PATH="${INSTALL_PREFIX}/lib/pkgconfig:\$PKG_CONFIG_PATH"
export CMAKE_PREFIX_PATH="${INSTALL_PREFIX}:\$CMAKE_PREFIX_PATH"

echo "Environment configured for ${DEPENDENCY_NAME}"
echo "  PATH: ${INSTALL_PREFIX}/bin"
echo "  LD_LIBRARY_PATH: ${INSTALL_PREFIX}/lib"
echo "  PKG_CONFIG_PATH: ${INSTALL_PREFIX}/lib/pkgconfig"
echo "  CMAKE_PREFIX_PATH: ${INSTALL_PREFIX}"
EOF
    
    chmod +x "${ENV_SCRIPT}"
    
    echo -e "${GREEN}Environment setup script created: ${ENV_SCRIPT}${NC}"
    echo -e "${YELLOW}To use: source ${ENV_SCRIPT}${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}=== Building ${DEPENDENCY_NAME} ===${NC}"
    
    check_prerequisites
    clone_dependency
    build_dependency
    install_dependency
    setup_environment
    
    echo -e "${GREEN}=== Build complete ===${NC}"
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Source the environment: source ${INSTALL_PREFIX}/env-setup.sh"
    echo "  2. Verify installation: which ${DEPENDENCY_NAME}"
    echo "  3. Use in your project: Add to CMakeLists.txt"
}

# Run main function
main "$@"

