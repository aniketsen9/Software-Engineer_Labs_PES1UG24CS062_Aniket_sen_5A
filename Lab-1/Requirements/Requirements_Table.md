# Requirements Table

## Food Bank Surplus Redistribution Platform

### Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| FR-001 | Functional | The system shall allow Donor Partners to post surplus food packages with expiry countdown information and dietary tags. | High | Pass: A donor creates a listing containing food details, expiry information, and dietary tags. Fail: The system allows an incomplete listing without required expiry information. | Helps donors communicate what food is available and prevents expired food from remaining active. |
| FR-002 | Functional | The system shall allow Shelter Coordinators to view available surplus food batches with their expiry information and dietary tags. | High | Pass: A shelter can view active batches and their key details. Fail: Expired or unavailable batches appear as reservable. | Helps shelters quickly identify suitable food before it expires. |
| FR-003 | Functional | The system shall allow Shelter Coordinators to reserve an available food batch and select a pickup window before expiry. | High | Pass: A shelter selects an available batch and pickup window and receives a reservation confirmation. Fail: The system permits reservation of an expired or already reserved batch. | Coordinates redistribution and reduces food wastage. |
| FR-004 | Functional | The system shall generate and provide a pickup verification code after a food batch is successfully reserved. | High | Pass: A successful reservation produces a unique verification code for pickup. Fail: No verification code is generated after a confirmed reservation. | Provides a simple way to verify that the correct shelter is collecting the reserved food. |
| FR-005 | Functional | The system shall notify relevant Shelter Coordinators when a high-quantity perishable food batch is newly listed within the configured local radius. | Medium | Pass: Eligible nearby shelters receive a notification for a qualifying listing. Fail: Eligible shelters receive no notification for a qualifying listing. | Increases the chance that highly perishable surplus food is claimed before expiry. |

### Non-Functional Requirements

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| NFR-001 | Performance & Security | The platform shall dispatch notifications to eligible shelters within a 5 km radius with low latency and maintain appropriate security during peak usage. | High | Pass: Benchmarking under simulated peak load confirms the target notification latency and required security controls. Fail: Tests show unacceptable notification delay or security failures. | Fast, secure notifications are important when food is highly perishable. |
| NFR-002 | Availability & Data Integrity | The platform shall keep food-listing, reservation, expiry, and pickup information consistent and available during normal operating periods. | High | Pass: Reservation and listing tests show no duplicate confirmed reservations and no active listing remains reservable after expiry. Fail: Conflicting reservation or expiry states are observed. | Accurate, available data prevents shelters from arriving for unavailable food and reduces operational confusion. |
