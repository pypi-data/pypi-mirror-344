# MDP for Franka Golf
# Author: Matin Moezzi (matin@aiarena.io)
# Date: 2025-03-17

from __future__ import annotations

from .observations import hole_poses
import torch
from typing import TYPE_CHECKING

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils.math import matrix_from_quat
import omni.log

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def approach_ee_club_grip(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward the robot for reaching the club grip using a steeper function for more responsive rewards."""
    ee_tcp_pos = env.scene["ee_frame"].data.target_pos_w[..., 0, :]
    club_grip_pos = env.scene["club_grip_frame"].data.target_pos_w[..., 0, :]

    # Compute the distance of the end-effector to the handle
    distance = torch.norm(ee_tcp_pos - club_grip_pos, dim=-1, p=2)

    # Use a steeper function for more responsive rewards
    # Scale factor to make rewards more noticeable at smaller distances
    scale_factor = 5.0
    # Use exponential decay for steeper response to distance changes
    reward = torch.exp(-scale_factor * distance)

    return reward

def align_ee_handle(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for aligning the end-effector with the handle.

    The reward is based on the alignment of the gripper with the handle. It is computed as follows:

    .. math::

        reward = 0.5 * (align_z^2 + align_y^2)

    where :math:`align_z` is the dot product of the z direction of the gripper and the -y direction of the handle
    and :math:`align_y` is the dot product of the -y direction of the gripper and the x direction of the handle.
    """
    ee_tcp_quat = env.scene["ee_frame"].data.target_quat_w[..., 0, :]
    handle_quat = env.scene["club_grip_frame"].data.target_quat_w[..., 0, :]

    ee_tcp_rot_mat = matrix_from_quat(ee_tcp_quat)
    handle_mat = matrix_from_quat(handle_quat)

    # get current x and y direction of the handle
    handle_x, handle_y = handle_mat[..., 0], handle_mat[..., 1]
    # get current y and z direction of the gripper
    ee_tcp_y, ee_tcp_z = ee_tcp_rot_mat[..., 1], ee_tcp_rot_mat[..., 2]

    # make sure gripper aligns with the handle
    # in this case, the z direction of the gripper should be close to the -y direction of the handle
    # and the -y direction of the gripper should be close to the x direction of the handle
    align_z = (
        torch.bmm(ee_tcp_z.unsqueeze(1), -handle_y.unsqueeze(-1))
        .squeeze(-1)
        .squeeze(-1)
    )
    align_y = (
        torch.bmm(-ee_tcp_y.unsqueeze(1), handle_x.unsqueeze(-1))
        .squeeze(-1)
        .squeeze(-1)
    )

    reward = torch.sign(align_z) * align_z**2 + torch.sign(align_y) * align_y**2
    return reward


def align_grasp_around_handle(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Bonus for correct hand orientation around the handle.

    The correct hand orientation is when the left finger is to the left of the handle and the right finger is to the right of the handle,
    based on the new orientation where -y of grip is z of ee_tcp and -y of ee_tcp is x of grip.
    """
    # Target object position: (num_envs, 3)
    handle_pos = env.scene["club_grip_frame"].data.target_pos_w[..., 0, :]
    # Fingertips position: (num_envs, n_fingertips, 3)
    ee_fingertips_w = env.scene["ee_frame"].data.target_pos_w[..., 1:, :]
    lfinger_pos = ee_fingertips_w[..., 0, :]
    rfinger_pos = ee_fingertips_w[..., 1, :]

    # Check if hand is in a graspable pose
    # With the new orientation, we check if left finger is to the left of the handle and right finger is to the right
    is_graspable = (rfinger_pos[:, 1] < handle_pos[:, 1]) & (
        lfinger_pos[:, 1] > handle_pos[:, 1]
    )

    # bonus if left finger is to the left of the handle and right finger is to the right
    return is_graspable


def approach_gripper_handle(
    env: ManagerBasedRLEnv, offset: float = 0.04
) -> torch.Tensor:
    """Reward the robot's gripper reaching the club grip with the right pose.

    This function returns the distance of fingertips to the handle when the fingers are in a grasping orientation
    (i.e., the left finger is to the left of the handle and the right finger is to the right of the handle). Otherwise, it returns zero.
    """
    # Target object position: (num_envs, 3)
    handle_pos = env.scene["club_grip_frame"].data.target_pos_w[..., 0, :]
    # Fingertips position: (num_envs, n_fingertips, 3)
    ee_fingertips_w = env.scene["ee_frame"].data.target_pos_w[..., 1:, :]
    lfinger_pos = ee_fingertips_w[..., 0, :]
    rfinger_pos = ee_fingertips_w[..., 1, :]

    # Compute the distance of each finger from the handle
    lfinger_dist = torch.abs(lfinger_pos[:, 1] - handle_pos[:, 1])
    rfinger_dist = torch.abs(rfinger_pos[:, 1] - handle_pos[:, 1])

    # Check if hand is in a graspable pose
    is_graspable = (rfinger_pos[:, 1] < handle_pos[:, 1]) & (
        lfinger_pos[:, 1] > handle_pos[:, 1]
    )

    reward = is_graspable * ((offset - lfinger_dist) + (offset - rfinger_dist))
    return reward


def grasp_handle(
    env: ManagerBasedRLEnv,
    threshold: float,
    open_joint_pos: float,
    asset_cfg: SceneEntityCfg,
) -> torch.Tensor:
    """Reward for closing the fingers when being close to the handle.

    The :attr:`threshold` is the distance from the handle at which the fingers should be closed.
    The :attr:`open_joint_pos` is the joint position when the fingers are open.

    Note:
        It is assumed that zero joint position corresponds to the fingers being closed.
    """
    ee_tcp_pos = env.scene["ee_frame"].data.target_pos_w[..., 0, :][..., :2]
    handle_pos = env.scene["club_grip_frame"].data.target_pos_w[..., 0, :][..., :2]
    gripper_joint_pos = env.scene[asset_cfg.name].data.joint_pos[:, asset_cfg.joint_ids]

    distance = torch.norm(handle_pos - ee_tcp_pos, dim=-1, p=2)
    is_close = distance <= threshold

    reward = is_close * torch.sum(open_joint_pos - gripper_joint_pos, dim=-1)

    return reward


def approach_hitting_point_ball(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for approaching the club grip hitting point to the ball.

    Only rewards approaching the ball when the club is being grasped properly.
    """
    club = env.scene["golf_club"]
    club_grip_pos = env.scene["club_grip_frame"].data.target_pos_w[..., 0, :][..., :2]
    ee_tcp_pos = env.scene["ee_frame"].data.target_pos_w[..., 0, :][..., :2]

    club_hitting_point_idx = club.find_bodies("head_link")[0][0]
    club_hitting_point_pos = club.data.body_pos_w[:, club_hitting_point_idx, :]
    ball_pos = env.scene["golf_ball"].data.root_pos_w
    distance = torch.norm(club_hitting_point_pos - ball_pos, dim=-1, p=2)

    # Distance-based reward (closer is better)
    distance_reward = torch.exp(-5.0 * distance)

    is_close = torch.norm(club_grip_pos - ee_tcp_pos, dim=-1, p=2) <= 0.03

    # Scale reward smoothly based on quality of grasp, but only when actually held
    reward = distance_reward * is_close.float()
    return reward


def approach_ball_hole(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for approaching the ball to the hole."""
    ball_pos = env.scene["golf_ball"].data.root_pos_w
    hole_pos = hole_poses(env)
    distance = torch.norm(ball_pos - hole_pos, dim=-1, p=2)

    # The original was fine, just keeping for completeness
    reward = torch.exp(-5.0 * distance)
    omni.log.info(f"reward: {reward}")
    return reward
