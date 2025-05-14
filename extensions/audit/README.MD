# Indirect Node Counts in Ansible Collections

## Overview

In the context of Ansible automation, **indirect node counts** refer to the practice of calculating or verifying the capacity or availability of computing nodes **through external systems or controllers**, rather than directly querying the nodes themselves. This approach is especially useful in complex, public cloud, or on prem environments .

This file explains:
- What indirect node counts are
- Why they are required
- What they enable
- Their value

## What Are Indirect Node Counts?

Rather than connecting directly to each node to assess its state  of automation(e.g., Service, DB, VM, etc), **indirect node counts** leverage tools like ** APIs**, or other management layers to obtain usage information.

In an Ansible role or collection, this might involve:
- Querying a cloud service for the list of DBs or VMs and their status of if they are being automated

## Why Are They Required?

Directly connecting to every node:
- Is **inefficient** in large-scale environments
- May be **prohibited** due to security, network segmentation, or policy
- **Doesn't scale** across multiple clusters or providers
- Often leads to **incomplete or stale data**

Using indirect node counts via cluster managers:
- Enables **centralized insight** into resource usage
- Works well in **managed or disconnected environments**
- Allows **non-invasive** assessment (e.g., read-only API access)

## What Does It Do?

In practical terms, using indirect node counts in an Ansible collection:
- Enables **guardrails** to verify into knowing what you are automating
- Reduces operational risk and improves **predictability** of automation workflows

## Why This Is a Good Practice

| Benefit | Description |
|--------|-------------|
| ✅ Scalable | Works across many clusters and environments |
| ✅ Secure | Limits direct access to sensitive nodes |
| ✅ Efficient | Avoids per-node polling, uses cached or aggregated data |
| ✅ Integrated | Leverages our existing Certified and Validated collections |
| ✅ Reliable | Provides consistent data source for automation decisions |
