# Project Structure

The project consists of a [main repository](https://github.com/RoBorregos/home) and several submodules. The main repository contains the high-level code corresponding to the logic for each of the tasks in the competition. In addition, every repository contains a ROS workspace which contains the code executed during the competition. The submodules are divided according to the internal subteams:

- [HRI](https://github.com/RoBorregos/home-hri/tree/main)
- [Manipulation](https://github.com/RoBorregos/home-manipulation/tree/main)
- [Navigation](https://github.com/RoBorregos/home-navigation/tree/main)
- [Vision](https://github.com/RoBorregos/home-vision/tree/main)

The main idea of this structure is to divide the development into individual areas such that developers only need to build and compile the code in a specific submodule. This allows for faster development and testing of the code.

## Docker

To standarize the development process, we have migrated the development environment to a containerized system. This allows us to have a consistent setup across all team members and ensures that the code runs in the same way on all machines. The containerized system is based on Docker and Docker Compose. 

Each of the repositories contains a `docker/` directory and a `Makefile`. The `Makefile` contains shortcuts for common actions, such as building, running, removing, and entering into the containers. In addition, the `Makefile` ensures consistent naming for containers and images. The build and run commands in the `Makefile` make reference to the scripts in `docker/scripts/`, which add a variety of options when running the containers. In short, the scripts ensure that containers have permissions, mount only the necessary directories, and set up the environment variables.

### Mounted Directories 

For each of the submodules and the main repository, the `Makefile` mounts the `ws` directory into the container. This directory contains the code that is being developed and meant to be runned during the competition. This allows changes in the repository to be reflected in the container and vice versa. Other directories in the repositories contain ad-hoc scripts, research, and test files that aren´t meant to be runned in the competition.

### Docker Compose

At the moment, some of the submodules contain docker compose files that allow for the creation of multiple containers at once. This is useful for running multiple nodes in the same network with few commands. However, currently there are few submodules that use this feature and most rely on the commands specified in `Makefile`. 

### Docker Images

There are 3 types of images that can be built using the `Makefile`:
- cpu: An image that installs the necessary dependencies for the code to run on a CPU. For some of the submodules, this image may not be suitable to run all the code due to heavy computational requirements.
- gpu: An image that installs the necessary dependencies for the code to run on a GPU. This image is suitable for running all the code in the submodules.
- l4t-35.4.1: An image that installs the necessary dependencies for the code to run on a Jetson AGX Xavier. This image is suitable for running all the code in the submodules. Since most development is performed on a laptop or desktop, there may be minor modules that aren't supported yet for this image.
