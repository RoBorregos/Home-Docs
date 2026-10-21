# Omnibase Setup

Hardware list, wiring, configuration and bring-up of FRIDA's omnidirectional base. For the design and the firmware architecture see the [Omnibase Overview](overview.md). Firmware and configuration backups live in [RoBorregos/home-custom-base](https://github.com/RoBorregos/home-custom-base); the ROS 2 driver used on the robot lives in [home2](https://github.com/RoBorregos/home2) (`navigation/packages/omnidriver`).

## Hardware List

| Component | Part | Notes |
|---|---|---|
| Wheels | 4× mecanum | ~15 cm diameter |
| Motors | 4× EaglePower LA8308 90KV | Brushless, 20 pole pairs, 9:1 gearbox |
| Motor drivers | 4× ODrive S1 | CAN, onboard encoder, 2 Ω brake resistor |
| Main controller | STM32H755 (NUCLEO-H755ZI-Q) | FreeRTOS on the Cortex-M7 core |
| CAN transceiver | TJA1051 | FDCAN1, 500 kbps |
| IMU | BNO085 | I2C1, game rotation vector at 50 Hz |
| Wireless teleop | ESP32 | Bluetooth bridge for a PS5 / DualShock 4 controller |
| Lidars | 2× RPLIDAR C1 | Opposite corners, merged into one 360° `/scan` |
| Battery | 8× LiFePO4 3.2 V 25 Ah in series + Daly BMS | 25.6 V nominal, 640 Wh; powers the whole robot |
| Emergency stop | Normally-closed button | Wired to PE2 |
| Chassis | 4040 aluminum profiles + MDF covers | 64 × 50 cm footprint with wheels |

## Wiring

### STM32 Pinout

| Pin | Function | Connected to |
|---|---|---|
| PD0 / PD1 | FDCAN1_RX / FDCAN1_TX | TJA1051 → CAN bus to the 4 ODrives |
| PB6 / PB7 | I2C1_SCL / I2C1_SDA | BNO085 |
| PD5 / PD6 | USART2_TX / USART2_RX | ESP32 (115200 baud) |
| PD8 / PD9 | USART3_TX / USART3_RX | ROS computer through the ST-LINK USB port (230400 baud) |
| PE2 | GPIO input, internal pull-up | E-stop button (NC to GND) |

The ST-LINK USB port shows up on the computer as `/dev/ttyACM*`. On the Orin, `docker/navigation/setup-USB.sh` in home2 installs udev rules that create stable names: `/dev/ttyOmniSTM32` for the STM32 and `/dev/ttyOmniLidar1` / `/dev/ttyOmniLidar2` for the lidars.

### CAN Bus

The four ODrives are daisy-chained on a single CAN bus (connectors J16/J17 on each S1). Connect CAN_H and CAN_L to the bus, terminate both ends with 120 Ω and tie the CAN ground to the system ground at **one** point only.

<p align="center">
  <img src="/assets/development/omnibase/odrive_can_io.png" alt="ODrive S1 CAN IO connector pinout">
</p>
<p align="center" style="font-size:small"><i>ODrive S1 CAN IO connector (J16, J17). Source: ODrive S1 datasheet</i></p>

| Wheel | CAN node ID |
|---|---|
| Front-Left | 36 |
| Front-Right | 34 |
| Rear-Left | 33 |
| Rear-Right | 40 |

The node IDs are assigned in the firmware at boot, before CAN reception is enabled.

## ODrive Configuration

The ODrives are configured from the [ODrive GUI](https://gui.odriverobotics.com/configuration) over USB. The current configuration of each drive is backed up in `odrive_config/odrive_node<ID>.json` in home-custom-base, so a replaced drive can be restored from there.

| Parameter | Value |
|---|---|
| DC bus overvoltage / undervoltage trip | 29 V / 10.5 V |
| DC max positive / negative current | 15 A / −0.01 A |
| Brake resistor | Enabled, 2 Ω |
| Motor | 20 pole pairs, 90 KV |
| Current soft / hard max | 20 A / 23 A |
| Encoder | Onboard |
| Control mode | Velocity control, ramped input (`VEL_RAMP`) |
| Velocity ramp rate / limit | 40 turns/s² / 25 turns/s |
| CAN | 500 kbps, heartbeat every 100 ms, encoder feedback every 10 ms |

After changing the configuration, run the steps of the GUI's **Apply & Calibrate** page in order: *Erase & Reboot*, *Apply*, *Save & Reboot*, *Run Calibration Sequence*, *Save & Reboot*. Calibration only works with the drive powered from the DC bus and the wheel free to spin.

Single parameters can also be written over CAN from the dashboard's "Advanced param (RxSdo)" box; `odrive_config/flat_endpoints.json` lists the endpoint IDs for ODrive firmware v0.6.12.

## Firmware

The STM32 project is `firmware/STM32H7_OMNIBASE_CAN_BNO085` in home-custom-base. Open it in STM32CubeIDE, build the CM7 project and flash it through the board's ST-LINK USB port.

Compile-time switches in the firmware:

- `IMU_ENABLED`: disables the BNO085 task when the IMU is not connected.
- `EKF_TRUST_IMU`: set to `0` to run the EKF on wheel odometry only.

!!! warning
    Power the ODrives (10.5 V to 29 V) before booting the STM32. If the drives are off when the firmware starts, CAN transmission times out.

## Bring-up

### On the Robot (home2)

From the home2 repository on the Orin:

```bash
./run.sh navigation --move   # base driver + lidars + teleop only
```

`--move` runs `nav_main/launch/omni_setup/omni_basics.launch.py`, which starts the `odrive_dashboard` node (from the `omnidriver` package) and the two lidars. The dashboard is the only publisher of the `odom → base_link` transform: it takes the pose and covariance from the on-MCU EKF, so `robot_localization` is not launched. For mapping and navigation use `./run.sh navigation --mapping` or `./run.sh navigation --gpsr`; see the [home2 navigation README](https://github.com/RoBorregos/home2/tree/main/navigation) for the full workflow.

The web dashboard is served at `http://<robot-ip>:5000`. It shows odometry, IMU, ODrive axis states, the link status of the ESP32 and the ROS computer, and the firmware error log.

Main ROS 2 interface of `odrive_dashboard`:

| Topic | Type | Direction |
|---|---|---|
| `cmd_vel` | `geometry_msgs/TwistStamped` (Nav2) or `Twist` | Subscribed |
| `odrive/odom` | `nav_msgs/Odometry` (EKF pose, body-frame twist) | Published |
| `odrive/imu` | `sensor_msgs/Imu` (BNO085 yaw and yaw rate) | Published |
| `odrive/axis_states`, `odrive/axis_errors`, `odrive/bus_voltage` | Diagnostics | Published |
| TF `odom → base_link` | | Published |

### Standalone (home-custom-base)

To test the base without the rest of the robot, use the dashboard in home-custom-base:

```bash
cd omnibase_ws
colcon build --packages-select odrive_comm
source install/setup.bash
ros2 run odrive_comm odrive_dashboard
```

The dashboard is then served at `http://localhost:5000`.

## Debugging the CAN Bus with a CANable

A CANable adapter lets a Linux computer listen to the CAN bus directly:

```bash
sudo apt install can-utils
ls /dev/ttyACM* /dev/ttyUSB*                 # find the CANable port
sudo slcand -o -c -s6 /dev/ttyACM1 can0      # -s6 = 500 kbps
sudo ip link set up can0 txqueuelen 1000

candump can0                # dump all traffic
cansniffer can0             # live view grouped by ID
canbusload can0@500000      # bus load
```

More information in the [CANable getting started guide](https://canable.io/getting-started.html).

## Troubleshooting

- **I2C init errors at boot, or nothing works:** usually a FreeRTOS task ran out of stack. Increase the stack size of the task that fails; the firmware also reports stack overflows through its error log.
- **An ODrive stays in `INITIALIZING`:** expected for 1 to 3 seconds after power-up or after changing a parameter such as `current_hard_max`; longer than that, it cannot be cleared with "clear errors". The only fix found so far is to power everything off, wait a few seconds and power on again. It happened at RoboCup 2026.
- **Repeated CAN bus-off, axis faults or arm timeouts:** check the CAN connectors, the termination resistors and the single CAN ground tie before suspecting the firmware.
- **Heading drifts and the IMU looks dead:** there is no IMU staleness watchdog yet. If the BNO085 stops sending samples, the EKF silently falls back to wheel-only odometry.

## References

- [ODrive S1 datasheet](https://docs.odriverobotics.com/v/latest/hardware/s1-datasheet.html) and [CAN protocol](https://docs.odriverobotics.com/v/latest/manual/can-protocol.html)
- [STM32H755 datasheet](https://www.st.com/resource/en/datasheet/stm32h755bi.pdf) and [reference manual RM0399](https://www.st.com/resource/en/reference_manual/rm0399-stm32h745755-and-stm32h747757-advanced-armbased-32bit-mcus-stmicroelectronics.pdf)
- K. M. Lynch and F. C. Park, [*Modern Robotics*](https://hades.mech.northwestern.edu/images/7/7f/MR.pdf), ch. 13 (wheeled mobile robots)
- [ODrive-STM32-CAN-Driver](https://github.com/siddarthiyer/ODrive-STM32-CAN-Driver), base of the firmware's ODrive CAN functions
