## panda_gazebo_moveit2

Description:
panda_gazebo_moveit2 is a repository containing code and resources for simulating and controlling a Franka Emika Panda robot in the Gazebo simulator using MoveIt! 2.0. The project aims to provide a ROS-based simulation environment for the Franka Panda robot, integrating Gazebo for physics simulation and MoveIt! for motion planning and control.

Project Overview:
The project utilizes the Gazebo simulator and MoveIt! 2.0 framework to simulate and control the Franka Emika Panda robot. The integration of MoveIt! allows for easy motion planning, kinematic control, and trajectory execution, making it suitable for testing and developing robotic applications.

Features:

    Gazebo simulation environment for Franka Panda robot.
    Integration with MoveIt! 2.0 for motion planning and control.
    ROS packages for simulation setup and control interface.

Project Structure:

    /gazebo: Gazebo simulation files and launch configurations.
    /moveit_config: MoveIt! configuration files for Panda robot.
    /panda_gazebo_control: ROS package for controlling the Panda robot in Gazebo.

Getting Started:

    Clone the repository:

    bash

    git clone https://github.com/Hemanth95/panda_gazebo_moveit2.git
    cd panda_gazebo_moveit2

    Explore the gazebo, moveit_config, and panda_gazebo_control directories for respective files and configurations.

Simulation Instructions:

    Launch Gazebo simulation:

    bash

roslaunch gazebo panda_gazebo.launch

Start MoveIt! for Panda control:

bash

    roslaunch moveit_config moveit_planning_execution.launch

Controlling the Robot:

    Interact with MoveIt! RViz interface to plan and execute robot motions.
    Utilize the panda_gazebo_control package for programmatic control.

Contributing:
Contributions are welcome! If you find a bug or have an enhancement in mind, please open an issue or submit a pull request.

License:
This project is licensed under the MIT License.

Acknowledgments:

    Thanks to the Franka Emika team for providing the Panda robot model.
    Inspiration for this project comes from the need for a comprehensive simulation environment for the Franka Panda robot.

Feel free to explore, modify, and contribute to this project. Happy coding!
