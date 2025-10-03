# ADR-01: Primary Data Store for Vector & Relational Workloads

## Status

Proposed

## Context

SmartHire ATS is a mission-critical applicant tracking system requiring a robust data architecture that supports both traditional relational workloads and emerging AI-powered features. The system must handle:

**Performance Requirements:**
- 1,000 concurrent users with sub-3-second response times
- Search queries and profile loads must complete within 3 seconds
- Support for >100,000 candidate records with rapid growth expected

**Availability and Consistency:**
- 99.9% uptime requirement (8.76 hours downtime/year maximum)
- Strong data consistency for hiring decisions and audit logs (legally binding)
- Automated backup and disaster recovery capabilities

**Functional Requirements:**
- Traditional CRUD operations for candidate profiles, job postings, and application workflows
- Complex relational queries for reporting and analytics
- Future AI features including résumé parsing and vector-based candidate similarity search
- ACID compliance for transactional integrity

**Scalability Considerations:**
- Horizontal scalability to accommodate user and data growth
- Ability to handle mixed workloads (OLTP and vector similarity searches)
- Cost-effective scaling as the platform grows

Two primary architectural approaches have been identified for evaluation:

### Option 1: PostgreSQL with pgvector Extension

| Pros | Cons |
|------|------|
| Single database system reduces operational complexity | pgvector performance may not match specialized vector databases |
| ACID compliance and strong consistency guarantees | Vector operations can impact OLTP performance |
| Mature ecosystem with extensive tooling and expertise | Limited vector indexing algorithms compared to specialized solutions |
| Cost-effective for mixed workloads | Scaling vector operations requires careful resource management |
| Proven high availability with streaming replication | Vector search optimization requires specialized PostgreSQL tuning |

### Option 2: Specialized Vector Database (ChromaDB/FAISS-backed)

| Pros | Cons |
|------|------|
| Optimized vector search performance and indexing | Introduces operational complexity with multiple database systems |
| Advanced similarity search algorithms | Potential data consistency challenges across systems |
| Purpose-built for AI/ML workloads | Additional infrastructure costs and maintenance overhead |
| Horizontal scaling designed for vector operations | Limited ACID guarantees for transactional data |
| Faster development of AI features | Requires expertise in multiple database technologies |

## Decision

**Selected Architecture: PostgreSQL with pgvector extension deployed on Amazon RDS Multi-AZ with read replicas**

**Deployment Topology:**
- Primary: RDS PostgreSQL 15+ Multi-AZ deployment with pgvector extension
- Read Replicas: 2-3 read replicas across availability zones for query distribution
- Backup Strategy: Automated daily snapshots with 30-day retention, cross-region replication
- Monitoring: CloudWatch integration with custom metrics for vector operation performance

**Rationale:**

PostgreSQL with pgvector emerges as the optimal choice for SmartHire's current requirements and growth trajectory. This decision prioritizes operational simplicity, data consistency, and cost-effectiveness while providing a clear path for AI feature development.

The unified data platform approach eliminates the complexity of managing multiple database systems and ensures ACID compliance across all operations. PostgreSQL's mature high availability features, combined with AWS RDS Multi-AZ deployment, directly address the 99.9% uptime requirement with proven disaster recovery capabilities.

For SmartHire's scale (100,000+ records, 1,000 concurrent users), pgvector's performance characteristics are sufficient for the planned AI features. The extension supports approximate nearest neighbor search with HNSW indexing, which provides adequate performance for candidate similarity matching while maintaining the benefits of a single, consistent data store.

The decision also considers SmartHire's growth phase. A PostgreSQL-first approach reduces operational overhead, allows the team to leverage existing database expertise, and provides flexibility to evolve the architecture as AI requirements mature.

## Consequences

### Positive Outcomes

- **Operational Simplicity:** Single database system reduces monitoring, backup, and maintenance complexity
- **Data Consistency:** ACID guarantees across all operations eliminate synchronization issues between relational and vector data
- **Cost Efficiency:** Unified platform reduces infrastructure costs compared to multiple specialized databases
- **Team Productivity:** Leverages existing PostgreSQL expertise, reducing learning curve and time-to-market
- **Proven Reliability:** PostgreSQL's mature replication and backup features directly support 99.9% uptime requirements
- **Compliance Ready:** Strong consistency and audit trail capabilities support legal and regulatory requirements

### Negative Outcomes

- **Vector Performance Limitations:** pgvector may not achieve the same performance as specialized vector databases for complex similarity searches
- **Resource Contention:** Vector operations may impact OLTP performance during peak usage periods
- **Scaling Constraints:** Vector workloads may require vertical scaling before horizontal scaling becomes effective
- **Feature Limitations:** Advanced vector search capabilities may be limited compared to purpose-built solutions

### Mitigation Strategies

1. **Performance Optimization:**
   - Implement dedicated connection pools for vector operations
   - Use read replicas specifically for vector-heavy queries
   - Establish performance baselines and monitoring for vector operations

2. **Scaling Preparation:**
   - Design application architecture to support database sharding if needed
   - Implement caching layers (Redis) for frequently accessed vector results
   - Plan for potential migration to hybrid architecture if vector requirements exceed PostgreSQL capabilities

3. **Monitoring and Alerting:**
   - Implement custom CloudWatch metrics for vector operation latency
   - Set up alerts for resource contention between OLTP and vector workloads
   - Establish performance benchmarks for future architecture decisions

4. **Future Architecture Evolution:**
   - Design data access layers to abstract vector operations, enabling future migration to specialized vector databases
   - Plan quarterly architecture reviews to assess vector performance requirements
   - Maintain proof-of-concept implementations of specialized vector solutions for rapid migration if needed

This architectural decision provides SmartHire with a solid foundation for current requirements while maintaining flexibility for future AI-driven features and scale requirements.