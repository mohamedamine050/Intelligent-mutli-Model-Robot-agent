#!/usr/bin/env python3
"""
robot_brain_bridge.orion_bridge_node

- Polls Orion (Context Broker) for Mission:Current entity.
- When mission.status == "pending", extracts target coordinates and sends Nav2 goal.
- Subscribes to /amcl_pose and upserts Robot entity in Orion.
- Uses environment variables ORION_HOST and ROBOT_ID (defaults provided).
"""

import os
import json
import time
import threading

import requests
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
from nav2_msgs.action import NavigateToPose

DEFAULT_ORION = os.getenv("ORION_HOST", "http://172.23.48.1:1026")
ROBOT_ENTITY_ID = os.getenv("ROBOT_ID", "Robot:R2D2")
MISSION_ENTITY_ID = os.getenv("MISSION_ID", "Mission:Current")
POLL_PERIOD = float(os.getenv("ORION_POLL_PERIOD", "0.5"))  # seconds


class OrionBridge(Node):
    def __init__(self):
        super().__init__("orion_bridge_node")
        self.orion_host = DEFAULT_ORION.rstrip("/")
        self.robot_entity = ROBOT_ENTITY_ID
        self.mission_entity = MISSION_ENTITY_ID

        self.get_logger().info(f"OrionBridge starting. ORION_HOST={self.orion_host}")
        self.get_logger().info(f"Robot entity: {self.robot_entity}, Mission entity: {self.mission_entity}")

        # Nav2 action client
        self.nav_client = ActionClient(self, NavigateToPose, "navigate_to_pose")

        # Subscribe to robot pose (/amcl_pose)
        self.create_subscription(PoseWithCovarianceStamped, "/amcl_pose", self.odom_cb, 10)

        # Start polling loop in separate thread so rclpy.spin is not blocked
        self._stop = False
        self._poll_thread = threading.Thread(target=self._poll_orion_loop, daemon=True)
        self._poll_thread.start()

    # ---------------------
    # ROS callbacks
    # ---------------------
    def odom_cb(self, msg: PoseWithCovarianceStamped):
        """Called on /amcl_pose - update robot entity in Orion"""
        try:
            pose = msg.pose.pose
            payload = {
                "id": self.robot_entity,
                "type": "Robot",
                "pose": {
                    "type": "StructuredValue",
                    "value": {"x": pose.position.x, "y": pose.position.y, "z": pose.position.z}
                },
                "orientation": {
                    "type": "StructuredValue",
                    "value": {
                        "x": pose.orientation.x,
                        "y": pose.orientation.y,
                        "z": pose.orientation.z,
                        "w": pose.orientation.w
                    }
                },
                "timestamp": {"type": "Text", "value": str(self.get_clock().now().to_msg())}
            }
            # Try creating entity (POST) - if exists, PATCH attributes
            url = f"{self.orion_host}/v2/entities"
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=2)
            if resp.status_code == 201:
                self.get_logger().debug("Created robot entity in Orion")
            else:
                attr_url = f"{self.orion_host}/v2/entities/{self.robot_entity}/attrs"
                attrs = {
                    "pose": payload["pose"],
                    "orientation": payload["orientation"],
                    "timestamp": payload["timestamp"]
                }
                requests.patch(attr_url, json=attrs, headers={"Content-Type": "application/json"}, timeout=2)
                self.get_logger().debug("Updated robot entity in Orion")
        except Exception as e:
            self.get_logger().warn(f"Failed to push pose to Orion: {e}")

    # ---------------------
    # Orion poll loop
    # ---------------------
    def _poll_orion_loop(self):
        while not self._stop and rclpy.ok():
            try:
                url = f"{self.orion_host}/v2/entities/{self.mission_entity}"
                resp = requests.get(url, timeout=2)
                if resp.status_code == 200:
                    mission = resp.json()
                    status = mission.get("status", {}).get("value", "")
                    if status == "pending":
                        self.get_logger().info("Detected mission: pending")
                        self.handle_mission(mission)
                # else: entity not found or other states
            except Exception as e:
                self.get_logger().debug(f"Orion poll error: {e}")
            time.sleep(POLL_PERIOD)

    # ---------------------
    # Mission handling
    # ---------------------
    def handle_mission(self, mission: dict):
        try:
            target = mission.get("target", {}).get("value", {})
            if not target:
                self.get_logger().warn("Mission has no target")
                self.update_mission_status("failed")
                return

            x = float(target.get("x", 0.0))
            y = float(target.get("y", 0.0))
            frame = mission.get("target", {}).get("frame", {}).get("value", "map") or "map"
            self.get_logger().info(f"Mission target -> x:{x} y:{y} frame:{frame}")

            # Build NavigateToPose goal
            goal_msg = NavigateToPose.Goal()
            goal_msg.pose = PoseStamped()
            goal_msg.pose.header.frame_id = frame
            goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
            goal_msg.pose.pose.position.x = x
            goal_msg.pose.pose.position.y = y
            goal_msg.pose.pose.orientation.w = 1.0

            # Update mission to in_progress
            self.update_mission_status("in_progress")

            # Send goal
            self.nav_client.wait_for_server(timeout_sec=10.0)
            send_goal_future = self.nav_client.send_goal_async(goal_msg)
            send_goal_future.add_done_callback(self.goal_response_cb)
            self.get_logger().info("Sent goal to Nav2")
        except Exception as e:
            self.get_logger().error(f"Error handling mission: {e}")
            self.update_mission_status("failed")

    def goal_response_cb(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error("Nav2 rejected the goal")
                self.update_mission_status("failed")
                return
            self.get_logger().info("Nav2 accepted goal")
            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.goal_result_cb)
        except Exception as e:
            self.get_logger().error(f"goal_response_cb exception: {e}")
            self.update_mission_status("failed")

    def goal_result_cb(self, future):
        try:
            result = future.result().result
            self.get_logger().info("Navigation result received")
            self.update_mission_status("completed")
        except Exception as e:
            self.get_logger().error(f"goal_result_cb exception: {e}")
            self.update_mission_status("failed")

    # ---------------------
    # Orion helpers
    # ---------------------
    def update_mission_status(self, status: str):
        try:
            url = f"{self.orion_host}/v2/entities/{self.mission_entity}/attrs"
            payload = {
                "status": {"value": status, "type": "Text"},
                "last_update": {"value": str(self.get_clock().now().to_msg()), "type": "Text"}
            }
            resp = requests.patch(url, json=payload, headers={"Content-Type": "application/json"}, timeout=3)
            if resp.status_code in (204, 201):
                self.get_logger().info(f"Updated mission status -> {status}")
            else:
                self.get_logger().warn(f"Failed to update mission status ({resp.status_code}): {resp.text}")
        except Exception as e:
            self.get_logger().warn(f"Exception updating mission status: {e}")

    # ---------------------
    # Shutdown
    # ---------------------
    def destroy_node(self):
        self._stop = True
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = OrionBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutdown requested")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()