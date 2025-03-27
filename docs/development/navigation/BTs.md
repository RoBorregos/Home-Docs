# Behavior Trees in ROS2 

## 1. Behavior Tree Fundamentals

### Leaf Nodes (Executable Behaviors)
- **Definition**: 
  - Leaf nodes are the executable behaviors where the BT connects with the lowest-level code in the application
  - They represent concrete actions or conditions
  - Each leaf node is a class that returns one of three states:
    - `SUCCESS`
    - `FAILURE`
    - `RUNNING` (for asynchronous operations)

- **Key Characteristics**:
  - Framework-independent (can be used without ROS2)
  - Implement the actual functionality of the behavior tree
  - Typically inherit from `BT::ActionNodeBase` or similar base classes

### XML Tree Definition
Behavior trees are typically defined in XML files that specify:
- The logical structure (sequence, fallback, parallel, etc.)
- Node connections
- Parameters

```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <Sequence name="main_sequence">
      <Action1/>
      <Action2/>
    </Sequence>
  </BehaviorTree>
</root>
```

## 2. Control Flow Nodes

### Reactive Sequence
- **Behavior**:
  - All children must return SUCCESS for the sequence to succeed
  - Children are ticked asynchronously
  - If a running child returns FAILURE, it's halted immediately

- **Use Case**: 
  - When you need to monitor conditions while executing actions
  - For reactive behaviors that might need to be interrupted

### Other Common Control Nodes

| Node Type       | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| Sequence        | Ticks children sequentially until one fails                                 |
| Fallback        | Ticks children sequentially until one succeeds                              |
| Decorator       | Modifies the behavior of a single child node                                |

## 3. ROS2 Integration Architecture

### System Design Recommendations

- **Task Planner**:
  - Centralized coordinator node
  - Responsible for BT execution
  - Implemented using BT.CPP

- **Service-Oriented Components**:
  - Delegate decision-making to Task Planner
  - Implement specific capabilities as services
  - Should not contain complex business logic

## 4. Asynchronous Action Nodes

### Using rclcpp Action Clients
BT.CPP provides asynchronous action nodes that:
- Don't require manual thread management
- Support abortion (implements `TreeNode::halt()`)
- Are reactive to state changes

#### Fibonacci Action Example

```cpp
#include <behaviortree_ros2/bt_action_node.hpp>

using namespace BT;

class FibonacciAction: public RosActionNode<Fibonacci>
{
public:
 FibonacciAction(const std::string& name,
 const NodeConfig& conf,
 const RosNodeParams& params)
 : RosActionNode<Fibonacci>(name, conf, params)
 {}

 // The specific ports of this Derived class
 // should be merged with the ports of the base class,
 // using RosActionNode::providedBasicPorts()
 static PortsList providedPorts()
 {
 return providedBasicPorts({InputPort<unsigned>("order")});
 }

 // This is called when the TreeNode is ticked and it should
 // send the request to the action server
 bool setGoal(RosActionNode::Goal& goal) override 
{
 // get "order" from the Input port
 getInput("order", goal.order);
 // return true, if we were able to set the goal correctly.
 return true;
 }
 
// Callback executed when the reply is received.
 // Based on the reply you may decide to return SUCCESS or FAILURE.
 NodeStatus onResultReceived(const WrappedResult& wr) override
 {
 std::stringstream ss;
 ss << "Result received: ";
 for (auto number : wr.result->sequence) {
 ss << number << " ";
 }
 RCLCPP_INFO(node_->get_logger(), ss.str().c_str());
 return NodeStatus::SUCCESS;
 }

 // Callback invoked when there was an error at the level
 // of the communication between client and server.
 // This will set the status of the TreeNode to either SUCCESS or FAILURE,
 // based on the return value.
 // If not overridden, it will return FAILURE by default.
 virtual NodeStatus onFailure(ActionNodeErrorCode error) override
 {
 RCLCPP_ERROR(node_->get_logger(), "Error: %d", error);
 return NodeStatus::FAILURE;
 }

 // we also support a callback for the feedback, as in
 // the original tutorial.
 // Usually, this callback should return RUNNING, but you
 // might decide, based on the value of the feedback, to abort
 // the action, and consider the TreeNode completed.
 // In that case, return SUCCESS or FAILURE.
 // The Cancel request will be send automatically to the server.
 NodeStatus onFeedback(const std::shared_ptr<const Feedback> feedback)
 {
 std::stringstream ss;
 ss << "Next number in sequence received: ";
 for (auto number : feedback->partial_sequence) {
 ss << number << " ";
 }
 RCLCPP_INFO(node_->get_logger(), ss.str().c_str());
 return NodeStatus::RUNNING;
 }
};

```

#### Registration in Main

```cpp
  BehaviorTreeFactory factory;

  auto node = std::make_shared<rclcpp::Node>("fibonacci_action_client");
  // provide the ROS node and the name of the action service
  RosNodeParams params; 
 params.nh = node;
  params.default_port_value = "fibonacci";
  factory.registerNodeType<FibonacciAction>("Fibonacci", params);

```

## 5. Service Client Nodes

### Using rclcpp Service Clients
Similar to action nodes but for ROS services:

#### AddTwoInts Service Example

```cpp
#include <behaviortree_ros2/bt_service_node.hpp>

using AddTwoInts = example_interfaces::srv::AddTwoInts;
using namespace BT;


class AddTwoIntsNode: public RosServiceNode<AddTwoInts>
{
  public:

  AddTwoIntsNode(const std::string& name,
                  const NodeConfig& conf,
                  const RosNodeParams& params)
    : RosServiceNode<AddTwoInts>(name, conf, params)
  {}

  // The specific ports of this Derived class
  // should be merged with the ports of the base class,
  // using RosServiceNode::providedBasicPorts()
  static PortsList providedPorts()
  {
    return providedBasicPorts({
        InputPort<unsigned>("A"),
        InputPort<unsigned>("B")});
  }

  // This is called when the TreeNode is ticked and it should
  // send the request to the service provider
  bool setRequest(Request::SharedPtr& request) override
  {
    // use input ports to set A and B
    getInput("A", request->a);
    getInput("B", request->b);
    // must return true if we are ready to send the request
    return true;
  }

  // Callback invoked when the answer is received.
  // It must return SUCCESS or FAILURE
  NodeStatus onResponseReceived(const Response::SharedPtr& response) override
  {
    RCLCPP_INFO(node_->get_logger(), "Sum: %ld", response->sum);
    return NodeStatus::SUCCESS;
  }

  // Callback invoked when there was an error at the level
  // of the communication between client and server.
  // This will set the status of the TreeNode to either SUCCESS or FAILURE,
  // based on the return value.
  // If not overridden, it will return FAILURE by default.
  virtual NodeStatus onFailure(ServiceNodeErrorCode error) override
  {
    RCLCPP_ERROR(node_->get_logger(), "Error: %d", error);
    return NodeStatus::FAILURE;
  }
};

```

## 6. Practical Example: Simple Navigator

### Behavior Tree XML

```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <PipelineSequence name="NavigateWithReplanning">
      <DistanceController distance="1.0">
        <ComputePathToPose goal="{goal}" path="{path}"/>
      </DistanceController>
      <FollowPath path="{path}"/>
    </PipelineSequence>
  </BehaviorTree>
</root>
```

### Explanation
1. **PipelineSequence**: Special sequence node where children are executed in parallel but with ordered conditions
2. **DistanceController**: Controls when path replanning should occur
3. **ComputePathToPose**: Generates a path to the goal pose
4. **FollowPath**: Executes the path following behavior

## 7. Best Practices

### Node Implementation
- Keep leaf nodes focused on single responsibilities
- Use proper error handling in all callbacks
- Make nodes configurable through input ports

### System Design
- Keep business logic in the behavior tree
- Make components service-oriented
- Use asynchronous patterns for long-running actions

### Performance Considerations
- Minimize blocking operations in leaf nodes
- Use reactive sequences for time-critical behaviors
- Consider using dedicated executors for complex trees

# Advanced Nodes and Patterns

## 1. Action Nodes

### Common Navigation Action Nodes
| Node | Type | Description |
|------|------|-------------|
| `ComputePathToPose` | Action Server Client | Planner interface for path computation |
| `FollowPath` | Action Server Client | Controller interface for path following |
| `Spin`, `Wait`, `Backup` | Behavior Actions | Basic navigation behaviors |
| `ClearCostmapService` | Service Client | Clears costmaps when called |

## 2. Condition Nodes

### Essential Condition Nodes
| Node | Description | ROS Interface |
|------|-------------|---------------|
| `GoalUpdated` | Checks if goal on topic has been updated | Subscribes to goal topic |
| `GoalReached` | Verifies if goal pose is reached | Checks robot state |
| `InitialPoseReceived` | Checks for initial pose | Subscribes to initial_pose topic |
| `isBatteryLow` | Monitors battery level | Subscribes to battery topic |

### Key Usage Pattern
```xml
<ReactiveFallback>
    <GoalUpdated/>
    <ComputePathToPose/>
</ReactiveFallback>
```
- **Purpose**: Implements "If goal updated, then replan" logic
- **Behavior**: Asynchronously checks GoalUpdated while ComputePathToPose runs

## 3. Decorator Nodes

### Common Decorators
| Decorator | Functionality | Parameters |
|-----------|---------------|------------|
| `DistanceController` | Ticks child after robot travels specified distance | `distance` (meters) |
| `RateController` | Controls tick frequency | `hz` (frequency) |
| `GoalUpdater` | Updates child node's goal via ports | Input/output ports |
| `SingleTrigger` | Only ticks child once | - |
| `SpeedController` | Tick rate proportional to robot speed | - |

## 4. PipelineSequence Control Node

### Behavior Comparison
| Scenario | Traditional Sequence | PipelineSequence |
|----------|----------------------|------------------|
| Child returns RUNNING | Only ticks running child | Re-ticks all previous successful children |
| Child returns FAILURE | Fails entire sequence | Fails entire sequence |
| Last child SUCCESS | Sequence succeeds | Sequence succeeds |

### Example Usage
```xml
<root main_tree_to_execute="MainTree">
    <BehaviorTree ID="MainTree">
        <PipelineSequence>
            <Action_A/>
            <Action_B/>
            <Action_C/>
        </PipelineSequence>
    </BehaviorTree>
</root>
```

## 5. Recovery Control Node

### Behavior Logic
1. Ticks first child (main behavior)
2. If first child FAILS:
   - Ticks second child (recovery behavior)
   - Repeats until:
     - First child SUCCEEDS (returns SUCCESS)
     - Second child FAILS (returns FAILURE)
     - `number_of_retries` exceeded

### XML Example
```xml
<Recovery number_of_retries="3">
    <MainBehavior/>
    <RecoveryBehavior/>
</Recovery>
```

## 6. RoundRobin Control Node

### Behavior Characteristics
- Ticks children in circular order
- Returns SUCCESS if any child succeeds
- Returns FAILURE if all children fail
- Maintains internal pointer to last ticked child

### Comparison with Sequence
| Feature | Sequence | RoundRobin |
|---------|----------|------------|
| Start point | Always first child | Last ticked child |
| Success condition | All succeed | Any succeeds |
| Failure condition | Any fails | All fail |

## 7. Algorithm Selectors

### Dynamic Algorithm Selection
| Selector | Purpose | Default Algorithm | ROS Topic |
|----------|---------|-------------------|-----------|
| `PlannerSelector` | Switch planners | GridBased | `/planner_selector/set_planner` |
| `ControllerSelector` | Switch controllers | FollowPath | `/controller_selector/set_controller` |
| `GoalCheckerSelector` | Switch goal checkers | - | `/goal_checker_selector/set_checker` |

### Example Configuration
```xml
<ControllerSelector selected_controller="{selected_controller}" default_controller="FollowPath" topic_name="controller_selector"/>
<PlannerSelector selected_planner="{selected_planner}" default_planner="GridBased" topic_name="planner_selector"/>
```

## 8. Advanced Navigation Patterns

## ComputePathThroughPoses
- Accepts multiple intermediate waypoints
- Replans every 3 seconds
- Uses `RemovePassedGoals` (discards waypoints within 0.5m)

## MonitorAndFollowPath (Obstacle Handling)

A specialized monitoring system that runs alongside normal navigation to handle obstacles near the destination. It uses a reactive approach to dynamically adjust the robot's behavior when blocked paths are detected.

### 1. Obstacle Detection Phase
- **Path Length Check**: Constantly compares the current path length to the expected distance
- **Trigger Condition**: Activates when the path becomes significantly longer (typically >20% longer)
- **Normal Operation**: If path length is normal, navigation continues uninterrupted

### 2. Recovery Activation
When obstacles are detected:
1. **Immediate Stop**: 
   - Halts all robot movement as a safety precaution
   - Prevents collision with nearby obstacles

2. **Waiting Period**:
   - Pauses for a configurable duration (typically 5-10 seconds)
   - Allows temporary obstacles (like people) to move away
   - Continues monitoring during the entire wait

3. **Path Reevaluation**:
   - **If clear**: Resumes navigation using the original optimal path
   - **If still blocked**: 
     - Switches to the longer alternative route
     - May repeat the recovery sequence if configured

### Typical Use Cases
- Handling crowded delivery destinations
- Navigating through dynamic doorways
- Recovering from mapping errors near goals
- Managing temporary obstructions in final approach

## Advantages
1. **Safety**: Prevents forced navigation through blocked areas
2. **Efficiency**: Minimizes unnecessary path recomputations
3. **Flexibility**: Adapts to both permanent and temporary obstacles
4. **Predictability**: Provides consistent recovery behavior
   
```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <RecoveryNode number_of_retries="6" name="NavigateRecovery">
      <PipelineSequence name="NavigateWithReplanning">
        <ControllerSelector selected_controller="{selected_controller}" default_controller="FollowPath" topic_name="controller_selector"/>
        <PlannerSelector selected_planner="{selected_planner}" default_planner="GridBased" topic_name="planner_selector"/>
        <RateController hz="1.0">
          <RecoveryNode number_of_retries="1" name="ComputePathToPose">
            <ComputePathToPose goal="{goal}" path="{path}" planner_id="{selected_planner}" error_code_id="{compute_path_error_code}" error_msg="{compute_path_error_msg}"/>
            <ClearEntireCostmap name="ClearGlobalCostmap-Context" service_name="global_costmap/clear_entirely_global_costmap"/>
          </RecoveryNode>
        </RateController>
        <ReactiveSequence name="MonitorAndFollowPath">
          <PathLongerOnApproach path="{path}" prox_len="3.0" length_factor="2.0">
            <RetryUntilSuccessful num_attempts="1">
              <SequenceWithMemory name="CancelingControlAndWait">
                <CancelControl name="ControlCancel"/>
                <Wait wait_duration="5.0"/>
              </SequenceWithMemory>
            </RetryUntilSuccessful>
          </PathLongerOnApproach>
          <RecoveryNode number_of_retries="1" name="FollowPath">
            <FollowPath path="{path}" controller_id="{selected_controller}" error_code_id="{follow_path_error_code}" error_msg="{follow_path_error_msg}"/>
            <ClearEntireCostmap name="ClearLocalCostmap-Context" service_name="local_costmap/clear_entirely_local_costmap"/>
          </RecoveryNode>
        </ReactiveSequence>
      </PipelineSequence>
      <ReactiveFallback name="RecoveryFallback">
        <GoalUpdated/>
        <RoundRobin name="RecoveryActions">
          <Sequence name="ClearingActions">
            <ClearEntireCostmap name="ClearLocalCostmap-Subtree" service_name="local_costmap/clear_entirely_local_costmap"/>
            <ClearEntireCostmap name="ClearGlobalCostmap-Subtree" service_name="global_costmap/clear_entirely_global_costmap"/>
          </Sequence>
          <Spin spin_dist="1.57" error_code_id="{spin_error_code}" error_msg="{spin_error_msg}"/>
          <Wait wait_duration="5.0"/>
          <BackUp backup_dist="0.30" backup_speed="0.05" error_code_id="{backup_error_code}" error_msg="{backup_error_msg}"/>
        </RoundRobin>
      </ReactiveFallback>
    </RecoveryNode>
  </BehaviorTree>
</root>
```

## 9. Follow Dynamic Point Pattern

### Node Structure
| Node | Function | Parameters |
|------|----------|------------|
| `GoalUpdater` | Updates dynamic goal | ROS topic input |
| `ComputePathToPose` | Path calculation | 1Hz (RateController) |
| `TruncatePath` | Shortens path | `distance=1.0m` |
| `FollowPath` | Path execution | Continuous |

### Complete Example
```xml
<root main_tree_to_execute="MainTree"> 
  <BehaviorTree ID="MainTree"> 
    <PipelineSequence name="NavigateWithReplanning"> 
      <ControllerSelector selected_controller="{selected_controller}" default_controller="FollowPath" topic_name="controller_selector"/> 
      <PlannerSelector selected_planner="{selected_planner}" default_planner="GridBased" topic_name="planner_selector"/> 
      <RateController hz="1.0"> 
        <Sequence> 
          <GoalUpdater input_goal="{goal}" output_goal="{updated_goal}"> 
            <ComputePathToPose goal="{updated_goal}" path="{path}" planner_id="{selected_planner}" error_code_id="{compute_path_error_code}" error_msg="{compute_path_error_msg}"/> 
          </GoalUpdater> 
        <TruncatePath distance="1.0" input_path="{path}" output_path="{truncated_path}"/> 
        </Sequence> 
      </RateController> 
      <KeepRunningUntilFailure> 
        <FollowPath path="{truncated_path}" controller_id="{selected_controller}" error_code_id="{follow_path_error_code}" error_msg="{follow_path_error_msg}"/> 
      </KeepRunningUntilFailure> 
    </PipelineSequence> 
  </BehaviorTree> 
</root> 
```

## 10. Odometry Calibration

### Square Test Pattern
- 3 counter-clockwise squares (12 segments)
- Low speed (0.2 m/s) for precision
- Measures closure error (final vs initial pose)

### Implementation
```xml
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <Repeat num_cycles="3">
      <Sequence name="Drive in a square">
        <DriveOnHeading dist_to_travel="2.0" speed="0.2" time_allowance="12"/>
        <Spin spin_dist="1.570796" is_recovery="false"/>
        <DriveOnHeading dist_to_travel="2.0" speed="0.2" time_allowance="12"/>
        <Spin spin_dist="1.570796" is_recovery="false"/>
        <DriveOnHeading dist_to_travel="2.0" speed="0.2" time_allowance="12"/>
        <Spin spin_dist="1.570796" is_recovery="false"/>
        <DriveOnHeading dist_to_travel="2.0" speed="0.2" time_allowance="12"/>
        <Spin spin_dist="1.570796" is_recovery="false"/>
      </Sequence>
    </Repeat>
  </BehaviorTree>
</root>
```

## 11. Node Base Classes

### Node Type Selection Guide
| Node Type | Base Class | When to Use |
|-----------|------------|-------------|
| ROS Action | `BtActionNode` | Needs ROS action server |
| Decorator | `BT::DecoratorNode` | Modifies child behavior |
| Control | `BT::ControlNode` | Manages flow (Sequence, etc.) |
| Condition | `BT::ConditionNode` | Boolean checks |
| Simple Action | `BT::ActionNodeBase` | Non-ROS actions |

### BehaviorTree.CPP Node Methods Overview

| Method                | Required | Description | Typical Use Cases |
|-----------------------|----------|-------------|-------------------|
| **Constructor**       | Yes      | Initializes the node with:<br>- XML tag name for plugin matching<br>- ROS 2 action server name<br>- BT.CPP configurations | Registering the node in the factory<br>Setting default values |
| **providedPorts()**   | Yes      | Defines input/output ports for:<br>- Parameter configuration<br>- Data flow between nodes | Declaring node parameters<br>Connecting to blackboard variables |
| **on_tick()**         | No       | Called when node is executed by the tree:<br>- First method called during tick<br>- Runs before action is sent | Updating dynamic parameters<br>Resetting node state<br>Input validation |
| **on_wait_for_result()** | No | Called while waiting for action server response | Progress monitoring<br>Timeout checks<br>Preemption conditions |
| **on_success()**      | No       | Handles successful action completion | Processing result data<br>Updating blackboard<br>Cleanup operations |
| **on_aborted()**      | No       | Handles action server abortion | Error recovery<br>Failure logging<br>Status reporting |
| **on_cancelled()**    | No       | Handles action cancellation | Resource cleanup<br>Interruption handling |

## Key Notes:
1. **Required Methods** must be implemented for basic functionality
2. **Optional Methods** provide advanced control when implemented


## 12. Groot: Behavior Tree Visualization and Editing Tool

### Overview
**Groot** is the official graphical editor for Behavior Trees. It provides:

- Visual tree creation and modification
- Real-time monitoring of tree execution (with ROS2 Humble logger is recommended)
- Integration with ROS2 through BehaviorTree.CPP

### Key Features

| Feature | Description |
|---------|-------------|
| **Drag-and-Drop Interface** | Visually construct trees using node palettes |
| **XML Import/Export** | Seamless integration with ROS2 BT implementations |
| **Node Customization** | Edit ports, parameters, and metadata |
| **Plugin System** | Extend with custom node types |

### Installation
https://github.com/BehaviorTree/Groot

1. **Create Tree**:
   - Drag nodes from palette
   - Connect with edges
   - Configure node parameters


### Custom Nodes Integration
https://docs.nav2.org/plugin_tutorials/docs/writing_new_bt_plugin.html#writing-new-nbt-plugin
```cpp
BT_REGISTER_NODES(factory)
{
  BT::NodeBuilder builder =
    [](const std::string & name, const BT::NodeConfiguration & config)
    {
      return std::make_unique<nav2_behavior_tree::WaitAction>(name, "wait", config);
    };

  factory.registerBuilder<nav2_behavior_tree::WaitAction>("Wait", builder);
}
```

