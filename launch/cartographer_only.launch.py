import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1. 경로 설정 (패키지명에 맞게 수정 필요)
    pkg_name = 'frontier_ws' 
    
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
    # Cartographer 설정 파일 경로 (.lua 파일)
    cartographer_config_dir = os.path.join(get_package_share_directory(pkg_name), 'config')
    configuration_basename = 'tb3_1_turtlebot3_lds_2d.lua' # 실제 사용하는 lua 파일명

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        # 2. Cartographer 노드 실행
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename],
            remappings=[
                ('/base_scan', '/tb3_1/base_scan'),
                ('/odom', '/tb3_1/odom'),
                ('/scan', '/tb3_1/scan'),
                ('/base_footprint', '/tb3_1/base_footprint')
            ]
        ),

        # 3. Occupancy Grid Node 실행 
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-resolution', '0.05', '-publish_period_sec', '1.0'],
            remappings=[
                ('/map', '/tb3_1/map')
            ]
        ),
    ])