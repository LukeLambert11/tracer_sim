from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    tracer_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('tracer_description'),
                'launch',
                'display_tracer.launch.py'
            )
        )
    )

    return LaunchDescription([
        # Start Gazebo server
        ExecuteProcess(
            cmd=[
                'gzserver',
                '/opt/ros/humble/share/gazebo_ros/worlds/empty.world',
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so'
            ],
            output='screen'
        ),

        # Start Gazebo client
        ExecuteProcess(
            cmd=['gzclient', '--verbose'],
            output='screen'
        ),

        # Include RViz + robot state publisher
        tracer_description_launch,

        # Spawn the robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'tracer_v1', '-topic', 'robot_description'],
            output='screen',
        ),
    ])
