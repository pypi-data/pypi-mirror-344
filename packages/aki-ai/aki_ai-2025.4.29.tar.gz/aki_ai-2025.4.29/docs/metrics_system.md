# Project migrated to AMZN_AKI
# Check docs under https://code.amazon.com/packages/AMZN_AKI/blobs/mainline/--/docs/ for the latest version

# Aki Metrics System

This document provides an overview of Aki's metrics collection system, which tracks user activities, model usage, and tool interactions to improve the platform.

## Overview

Aki's metrics system is designed to collect anonymous usage data that helps:

- Understand how users interact with the platform
- Monitor model performance and resource utilization
- Identify popular tools and features
- Guide future development priorities

All metrics are:
- Anonymous (tied to a randomized user ID rather than personal information)
- Aggregated (individual interactions are not exposed)
- Configurable (can be disabled in production deployments)

## Metrics Categories

### User Metrics

| Metric Name | Description | Dimensions | Unit |
|-------------|-------------|------------|------|
| `active_user` | Tracks active user engagement | `user_id`, `version_id` | Count |
| `user_action` | Tracks specific user actions | `action_type`, `profile_name` | Count |

#### Action Types:
- `message`: User sent a message
- `stop`: User stopped a conversation
- `resume`: User resumed a conversation
- `app_startup`: Application was started
- `app_shutdown`: Application was shut down

### Model Usage Metrics

| Metric Name | Description | Dimensions | Unit |
|-------------|-------------|------------|------|
| `token_input` | Number of input tokens used | `model_id` | Count |
| `token_output` | Number of output tokens generated | `model_id` | Count |
| `execution_time` | Time taken for model execution | `model_id` | Milliseconds |
| `model_usage` | Counts usage of specific model | `model_id` | Count |

### Tool Usage Metrics

| Metric Name | Description | Dimensions | Unit |
|-------------|-------------|------------|------|
| `tool_usage` | Tracks usage of specific tools | `tool_name` | Count |

## Dimensions

Dimensions provide context for metric interpretation:

| Dimension Name | Description | Example Values |
|----------------|-------------|---------------|
| `user_id` | Identifier for the user | Username (from OS environment) |
| `version_id` | Version of the application | "1.2.0" |
| `model_id` | Identifier for the LLM model | "anthropic.claude-3-sonnet-20240229-v1:0" |
| `tool_name` | Name of the tool being used | "read_file", "shell_command" |
| `action_type` | Type of user action | "message", "stop", "resume" |
| `profile_name` | Name of the active profile | "Aki - Ask me anything" |

## Development Guidelines

When adding new features, follow these guidelines for metrics integration:

1. **Use helper methods** instead of direct metric recording
2. **Add new dimensions** when introducing categorizable values
3. **Maintain consistency** with existing naming conventions
4. **Document new metrics** in this guide

### Adding New Metrics

To add a new metric type:

1. Add the metric name to `MetricNames` class in `constants.py`
2. Create a helper method in `UsageMetrics` class
3. Update this documentation

Example:

```python
# In constants.py
class MetricNames:
    # Existing metrics...
    NEW_METRIC = "new_metric"

# In usage_metrics.py
def record_new_metric(self, value, dimension_value):
    self.record_metric(
        MetricNames.NEW_METRIC,
        value,
        dimensions={
            DimensionNames.SOME_DIMENSION: dimension_value
        }
    )
```

