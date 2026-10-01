# Use-Case Flow Specification

## Use Case: Reserve Surplus Food Batch

**Primary Actor:** Shelter Coordinator

### Preconditions

1. The Shelter Coordinator is registered and logged in.
2. A surplus food batch is available on the platform.
3. The selected food batch has not expired.
4. The selected food batch has not already been reserved.
5. A valid pickup window is available before the food expires.

### Postconditions

1. The selected food batch is marked as reserved.
2. The selected pickup window is recorded.
3. A pickup verification code is generated.
4. The reservation is confirmed for the Shelter Coordinator.
5. The reserved batch is no longer available for other shelters to reserve.

### Main Success Scenario

1. The Shelter Coordinator logs into the platform.
2. The system displays the available surplus food batches.
3. The Shelter Coordinator selects a suitable food batch.
4. The system displays the food batch details, including expiry information and dietary tags.
5. The Shelter Coordinator selects an available pickup window.
6. The Shelter Coordinator confirms the reservation.
7. The system checks that the food batch is still available and has not expired.
8. The system creates the reservation and marks the food batch as reserved.
9. The system generates a unique pickup verification code.
10. The system displays the reservation confirmation and pickup details to the Shelter Coordinator.

### Alternate Flow

**A1 — Food Batch Becomes Unavailable or Expires**

1. At Step 7, the system detects that the selected food batch has expired or has already been reserved.
2. The system rejects the reservation.
3. The system informs the Shelter Coordinator that the food batch is unavailable.
4. The system returns the Shelter Coordinator to the list of available food batches.
