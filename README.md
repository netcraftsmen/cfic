# Cisco Federal Innovation Challenge

Cisco Federal Innovation Challenge - APR 24 2023 - MAY 24 2023

Cisco is sponsoring a Federal Innovation Challenge to bring together ideas to accelerate modernization across the federal and defense landscape.

## Event Management Site

<https://www.federalinnovationchallenge.com/event/cfic>

## Abstract

Which use case(s) are you planning on addressing with your solution?*
*Select all that apply*

 * Accelerate Modernization- _Using the pipeline to migrate from legacy infrastructure to modernized infrastructure. For example, harvesting data from a simulated IOS device and replacing it with a Catalyst 8Kv with minimal downtime. Additional Integration with available APIs (no logging into devices with CLI) and simulating a typical customer journey from purchase to deployment is preferable._

 * Model-Driven Telemetry- _Using data configured and generated by the network to visualize changes executed using the pipeline. Critical is to show that the requested or necessary change had the outcome on the network intended. OpenSource visualization tools are preferable (TIG, ELK stacks)._

 * Software Lifecycle Management- _Integrating Software Image Management into the network pipeline by automating upgrades based on external events. For example, using the OpenVuln PSIRT API, a workflow is instantiated that upgrades software based on a published security vulnerability - This includes executing tests post-upgrade and report generation. OpenSource tooling is preferable (PyATS, Batfish, TextFSM). Additional points if reporting can map to federal standards such as RMF._

 * **Closed Loop Automation**- _Using telemetry generated from the network and data visualization to execute pipeline workflows. Example use cases are traffic flow optimization, Cyber-attack simulation, etc. Additional points for integration into AI or ML tooling such as ChatGPT, Bard, etc._


**Why did you choose to address this use case (or use cases)?**

The network infrastructure is a distributed system containing abundant information regarding network devices' operational state, configuration, capacity, interconnections, and the devices it supports. 

A forward-thinking approach is to view the network as an Event-Driven System. Lightweight containerized agents act as event publishers of telemetry, the change in state in the network links, their configuration, and attached devices.

This approach aligns with a microservice architecture / service-oriented architecture structural style, where large applications are built as small, independent components which are highly extensible.

The use of telemetry is an increased focus in IT operations providing raw data to the Machine Learning / Artificial Intelligence (ML/AI) algorithms for AIOps (Artificial Intelligence for IT Operations) and Security Orchestration, Automation, and Response Solution (SOAR) solutions.

While there are open-source tools to receive telemetry data, store it, visualize, and alert; how should the network operator provide access to infrastructure telemetry and events, in real-time, at scale, to current and future technology stakeholders? 

**What specific customer problem(s) do you plan to address?**

The goal of any solution should be to provide an extensible architectural framework that addresses the specific customer problem and is readily extended to additional or unforeseen use cases.

The customer is a regulated business quickly deploying thousands of teleworker call center agents with Meraki Z3 devices. The security policy permits attaching corporate laptops. However, 'spouse and child' devices often appear on the remote network. A point solution was developed in the SOAR platform using the Meraki API to apply a 'quarantine' network until the offense could be remedied. Alerting and generating a ticket in the SOAR platform relied on log analysis by the SOC team.

**Please provide a description of your proposed idea:**

The solution demonstrates how previously developed network and security automation software ("semaphore", published on Cisco DevNet Code Exchange by BlueAlly NetCraftsmen, LLC) is integrated as an extensible system leveraging cloud-managed services, open-source software, and OEM product offerings.

Network telemetry is published to Apache Kafka in Confluent Cloud. Apache Kafka is an event streaming service enabling access to network telemetry across the organization for functions including security alerting and auditing of clients accessing the network, and traditional uses like uplink and wireless utilization. 

A rulebook using Event-Driven Ansible by Red Hat is used to consume events from Apache Kafka and generate incidents in the SOAR platform. Other ITSM systems (ServiceNow) can easily be integrated using Certified Content Collections.

The publisher component of the solution can readably be extended to other controller-managed Cisco networks (ACI, DNAC) and traditional route/switch networks. Using Ansible playbooks and Content Collections, additional data sinks can include visibility, logging, and management systems. 

**How does your idea relate to the use case(s) you selected above?**

The solution adopts a service-oriented approach to the publishing and consumption of network telemetry data. While the solution can be extended to Cisco networking (routers, switches, firewalls), the implementation leverages the Meraki API to publish clients observed on a Meraki network (and network uplink statistics) to a Kafka event streaming service. Utilizing Event-Driven Ansible, IT management systems, and SOAR implementations consume the telemetry for auditing, alerting, and remediation.

## Notes

Initial network automation approaches focused on the integrations of systems in a client/server architecture using Application Programming Interfaces (APIs). Just as software applications have evolved to a service orientated, loosely coupled architecture, so should how modern networks are managed and audited.

## Author

Joel W. King @joelwking