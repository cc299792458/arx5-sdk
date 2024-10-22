from typing import Tuple, overload
import numpy as np
import numpy.typing as npt
from enum import Enum

JOINT_POS_MIN: npt.NDArray[np.float64]
JOINT_POS_MAX: npt.NDArray[np.float64]
DEFAULT_KP: npt.NDArray[np.float64]
DEFAULT_KD: npt.NDArray[np.float64]
DEFAULT_GRIPPER_KP: float
DEFAULT_GRIPPER_KD: float
JOINT_VEL_MAX: npt.NDArray[np.float64]
GRIPPER_VEL_MAX: float
GRIPPER_WIDTH: float
CTRL_DT: float

class LogLevel:
    DEBUG: "LogLevel"
    INFO: "LogLevel"
    WARNING: "LogLevel"
    ERROR: "LogLevel"

class Gain:
    def kp(self) -> npt.NDArray[np.float64]: ...
    def kd(self) -> npt.NDArray[np.float64]: ...
    gripper_kp: float
    gripper_kd: float
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        kp: npt.NDArray[np.float64],
        kd: npt.NDArray[np.float64],
        gripper_kp: float,
        gripper_kd: float,
    ) -> None: ...
    def __add__(self, other: Gain) -> Gain: ...
    def __mul__(self, scalar: float) -> Gain: ...

class LowState:
    timestamp: float
    gripper_pos: float
    gripper_vel: float
    gripper_torque: float
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self,
        pos: npt.NDArray[np.float64],
        vel: npt.NDArray[np.float64],
        torque: npt.NDArray[np.float64],
        gripper_pos: float,
    ) -> None: ...
    def __add__(self, other: LowState) -> LowState: ...
    def __mul__(self, scalar: float) -> LowState: ...
    def pos(self) -> npt.NDArray[np.float64]: ...
    def vel(self) -> npt.NDArray[np.float64]: ...
    def torque(self) -> npt.NDArray[np.float64]: ...

class Arx5LowLevel:
    JOINT_POS_MIN: npt.NDArray[np.float64]
    JOINT_POS_MAX: npt.NDArray[np.float64]
    DEFAULT_KP: npt.NDArray[np.float64]
    DEFAULT_KD: npt.NDArray[np.float64]
    CTRL_DT: float
    TORQUE_LIM: float
    DEFAULT_GRIPPER_KP: float
    DEFAULT_GRIPPER_KD: float

    def __init__(self) -> None: ...
    def send_recv_once(self) -> None: ...
    def enable_background_send_recv(self) -> None: ...
    def disable_background_send_recv(self) -> None: ...
    def set_low_cmd(self, cmd: LowState) -> None: ...
    def get_low_cmd(self) -> LowState: ...
    def get_timestamp(self) -> float: ...
    def get_state(self) -> LowState: ...
    def set_gain(self, gain: Gain) -> None: ...
    def get_gain(self) -> Gain: ...
    def clip_joint_pos(
        self, pos: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]: ...
    def reset_to_home(self) -> None: ...
    def set_to_damping(self) -> None: ...
    def calibrate_gripper(self) -> None: ...
    def set_log_level(self, log_level: LogLevel) -> None: ...

class HighState:
    timestamp: float
    gripper_pos: float
    gripper_vel: float
    gripper_torque: float
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(
        self, pose_6d: npt.NDArray[np.float64], gripper_pos: float
    ) -> None: ...
    def __add__(self, other: HighState) -> HighState: ...
    def __mul__(self, scalar: float) -> HighState: ...
    def pose_6d(self) -> npt.NDArray[np.float64]: ...

class Arx5HighLevel:
    def __init__(self) -> None: ...
    def set_high_cmd(self, cmd: HighState) -> None: ...
    def get_high_cmd(self) -> HighState: ...
    def get_high_state(self) -> HighState: ...
    def get_low_state(self) -> LowState: ...
    def get_timestamp(self) -> float: ...
    def reset_to_home(self) -> None: ...
    def set_to_damping(self) -> None: ...
    def set_log_level(self, log_level: LogLevel) -> None: ...
    def set_gain(self, gain: Gain) -> None: ...
    def get_gain(self) -> Gain: ...

class Arx5Solver:
    def __init__(self) -> None: ...
    def init_solver(self, urdf_file: str) -> None: ...
    def inverse_dynamics(
        self,
        joint_pos: npt.NDArray[np.float64],
        joint_vel: npt.NDArray[np.float64],
        joint_acc: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]: ...
    def inverse_kinematics(
        self,
        target_pose_6d: npt.NDArray[np.float64],
        current_joint_pos: npt.NDArray[np.float64],
    ) -> Tuple[bool, npt.NDArray[np.float64]]: ...
    def forward_kinematics(
        self, joint_pos: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]: ...
