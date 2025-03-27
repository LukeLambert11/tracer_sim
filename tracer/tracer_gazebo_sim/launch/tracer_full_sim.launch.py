from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
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

        # Start Gazebo client (GUI)
        ExecuteProcess(
            cmd=['gzclient', '--verbose'],
            output='screen'
        ),

        # Robot state publisher and RViz
        Node(
            package='tracer_description',
            executable='display_tracer.launch.py',
            name='display_tracer',
            output='screen',
        ),

        # Spawn the robot
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'tracer_v1', '-topic', 'robot_description'],
            output='screen',
        ),
    ])
