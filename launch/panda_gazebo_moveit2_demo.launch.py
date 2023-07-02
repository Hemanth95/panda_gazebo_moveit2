from ament_index_python.packages import get_package_share_directory
import launch
from launch.substitutions import Command, LaunchConfiguration, TextSubstitution
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros
import os

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzserver.launch.py")
        ),
        launch_arguments={"verbose": "true"}.items(), # "extra_gazebo_args": "-s libgazebo_ros_p3d.so"
    )
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gzclient.launch.py")
        ),
        launch_arguments={"verbose": "true"}.items(),
    )
    pkg_share = launch_ros.substitutions.FindPackageShare(package='panda_gazebo_moveit2').find('panda_gazebo_moveit2')
    
    urdf_file = os.path.join(pkg_share, 'description/panda.urdf')
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    spawn_entity = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "panda"],
        output="screen",
    )
    spawn_joint_state_broadcaster = launch_ros.actions.Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-type", "joint_state_broadcaster/JointStateBroadcaster"],
        output="screen",
    )
    effort_controller_config = os.path.join(
        get_package_share_directory("panda_gazebo_moveit2"), "config", "ros_control.yaml"
    )
    spawn_controller_arm = launch_ros.actions.Node(
        package="controller_manager",
        executable="spawner",
        arguments=["panda_arm_controller", "--param-file", effort_controller_config, "--controller-type", "joint_trajectory_controller/JointTrajectoryController"],
        output="screen",
    )
    spawn_controller_hand = launch_ros.actions.Node(
        package="controller_manager",
        executable="spawner",
        arguments=["hand_controller", "--param-file", effort_controller_config, "--controller-type", "position_controllers/GripperActionController"],
        output="screen",
    )
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=urdf_file,
                        description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='gui', default_value='false',
                        description='Flag to enable joint_state_publisher_gui'),
        
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=spawn_entity,
                on_exit=[spawn_joint_state_broadcaster],
                ),
        ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action = spawn_joint_state_broadcaster,
                on_exit=[spawn_controller_arm],
                ),
        ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action = spawn_joint_state_broadcaster,
                on_exit=[spawn_controller_hand],
                ),
        ),
        robot_state_publisher_node,
        gzclient,
        gzserver,
        spawn_entity,
    ])