from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    tracer_desc_pkg = FindPackageShare('tracer_description').find('tracer_description')
    tracer_urdf = os.path.join(tracer_desc_pkg, 'urdf', 'tracer_v1.xacro')

    return LaunchDescription([
        # Start gzserver
        ExecuteProcess(
            cmd=[
                'gzserver', '--verbose',
                '/opt/ros/humble/share/gazebo_ros/worlds/empty.world',
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so'
            ],
            output='screen'
        ),

        # Start gzclient
        ExecuteProcess(
            cmd=['gzclient'],
            output='screen'
        ),

        # Load joint state publisher, robot state publisher, and RViz
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tracer_desc_pkg, 'launch', 'display_tracer.launch.py')
            )
        ),

        # Spawn robot into Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', 'tracer_v1',
                '-topic', 'robot_description'
            ],
            output='screen'
        )
    ])
