# ADR-001: Selection of Primary Vector Storage for New-Hire Onboarding Tool (NHOT)

## Status
Proposed

## Context
The New-Hire Onboarding Tool (NHOT) requires a data platform capable of storing structured user profiles, onboarding progress tracking, compliance artifacts, and vector embeddings for semantic search and personalized recommendations. The system must support both transactional operations with strong consistency and low-latency vector similarity search (~200ms p95) while maintaining 99.95% availability and horizontal scalability to 10× current forecast.

Two primary architectural approaches are under consideration:
1. PostgreSQL 15 with pgvector extension via managed services (AWS RDS/Aurora, GCP AlloyDB)
2. Specialized vector databases (ChromaDB, FAISS) deployed on managed Kubernetes with separate transactional storage

## Decision
We will adopt **PostgreSQL 15 with pgvector extension** deployed on a managed cloud service (AWS Aurora PostgreSQL or GCP AlloyDB) as our primary data platform for NHOT.

## Rationale

### Evaluation Criteria Analysis

**Strong Consistency & ACID Compliance:**
PostgreSQL provides full ACID guarantees with MVCC for concurrent access, essential for onboarding workflow state and compliance data integrity. Specialized vector databases typically offer eventual consistency models that introduce complexity for transactional workflows.

**Operational Complexity:**
A unified PostgreSQL solution eliminates the need for cross-database synchronization, reduces monitoring surface area, and leverages existing team PostgreSQL expertise. The dual-database approach introduces data consistency challenges, additional failure modes, and operational overhead despite Kubernetes management.

**Performance Requirements:**
pgvector supports HNSW (Hierarchical Navigable Small World) indexing, delivering sub-200ms vector search performance for our expected dataset sizes. While specialized vector databases may offer marginal performance advantages, the difference is insufficient to justify architectural complexity for our use case.

**Scalability & Availability:**
Managed PostgreSQL services (Aurora, AlloyDB) provide automated failover, read replicas, and horizontal scaling capabilities meeting our 99.95% SLO. Aurora's multi-AZ deployment and AlloyDB's intelligent scaling align with our growth projections.

**Cost & Maintenance:**
Single-platform approach reduces licensing complexity, simplifies backup/disaster recovery, and minimizes operational overhead. Managed services provide automated patching, monitoring, and scaling without dedicated vector database expertise requirements.

## Consequences

### Positive
- **Simplified Architecture:** Single database eliminates data synchronization complexity and reduces failure points
- **Strong Consistency:** ACID compliance ensures data integrity across all onboarding workflows
- **Operational Efficiency:** Leverages existing PostgreSQL expertise and tooling
- **Cost Effectiveness:** Unified platform reduces infrastructure and operational costs
- **Proven Reliability:** Mature ecosystem with extensive monitoring and backup solutions

### Negative
- **Vector Performance Ceiling:** May not achieve optimal vector search performance compared to specialized solutions
- **Feature Limitations:** pgvector ecosystem less mature than dedicated vector database features
- **Scaling Constraints:** PostgreSQL scaling patterns may require more planning than purpose-built vector solutions

### Mitigation Strategies
- Implement proper HNSW index tuning and query optimization for vector operations
- Monitor vector search performance metrics and establish scaling triggers
- Maintain architectural flexibility to introduce dedicated vector storage if performance requirements exceed PostgreSQL capabilities
- Establish clear performance baselines and automated alerting for degradation

## Compliance & Security Considerations
PostgreSQL's mature security model, encryption at rest/transit, and compliance certifications (SOC 2, GDPR) align with HR data requirements. Managed services provide automated security patching and audit logging capabilities essential for compliance workflows.