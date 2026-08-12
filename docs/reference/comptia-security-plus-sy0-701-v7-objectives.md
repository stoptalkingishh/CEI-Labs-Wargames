# CompTIA Security+ SY0-701 V7 Objective Reference

## Source and use

This cleaned Markdown reference is transcribed from the project-provided
`CompTIA Security+ SY0-701 Exam Objectives (7.0).pdf`, Exam Objectives
Document Version 7.0, copyright 2023 CompTIA, Inc. It is retained as the
curriculum source for the planned Sentinel track, not as participant-facing
exam-preparation material. The Sentinel plan summarizes rather than copies
objective language and is not affiliated with or endorsed by CompTIA.

The supplied OCR Markdown was incomplete and had layout artifacts. This file
normalizes the five objective domains and the supplied lab-equipment list.
Consult the source PDF for the official document, including its full acronym
list and legal notices.

## Exam overview

The document describes skills in assessing enterprise security posture,
securing hybrid environments, applying governance/risk/compliance awareness,
and identifying, analyzing, and responding to security events and incidents.

| Domain | Weight |
| --- | --- |
| 1.0 General Security Concepts | 12% |
| 2.0 Threats, Vulnerabilities, and Mitigations | 22% |
| 3.0 Security Architecture | 18% |
| 4.0 Security Operations | 28% |
| 5.0 Security Program Management and Oversight | 20% |

## 1.0 General Security Concepts

### 1.1 Security controls

Compare and contrast security-control categories and types.

- Categories: technical, managerial, operational, and physical.
- Types: preventive, deterrent, detective, corrective, compensating, and
  directive.

### 1.2 Fundamental security concepts

Summarize CIA, non-repudiation, AAA, gap analysis, Zero Trust, physical
security, and deception/disruption technology.

- CIA: confidentiality, integrity, and availability.
- AAA: authenticating people and systems, plus authorization models.
- Zero Trust: adaptive identity, threat-scope reduction, policy-driven access
  control, policy administrator, policy engine, implicit trust zones,
  subject/system, and policy enforcement point.
- Physical controls: bollards, access-control vestibules, fencing, video
  surveillance, guards, badges, lighting, and infrared/pressure/microwave/
  ultrasonic sensors.
- Deception: honeypots, honeynets, honeyfiles, and honeytokens.

### 1.3 Change management

Explain why change-management processes affect security.

- Business process: approval, ownership, stakeholders, impact analysis, test
  results, backout plan, maintenance window, and standard operating procedure.
- Technical implications: allow/deny lists, restricted activity, downtime,
  service and application restarts, legacy applications, and dependencies.
- Documentation and version control: update diagrams and policies/procedures.

### 1.4 Cryptographic solutions

Explain the importance of appropriate cryptographic solutions.

- PKI: public/private keys and key escrow.
- Encryption: full-disk, partition, file, volume, database, and record;
  transport; asymmetric/symmetric methods; key exchange; algorithm and key
  length.
- Tools: TPM, HSM, key-management system, and secure enclave.
- Obfuscation: steganography, tokenization, and data masking.
- Hashing, salting, digital signatures, key stretching, blockchain, and open
  public ledgers.
- Certificates: certificate authorities, CRLs, OCSP, self-signed and
  third-party certificates, root of trust, CSR generation, and wildcards.

## 2.0 Threats, Vulnerabilities, and Mitigations

### 2.1 Threat actors and motivations

Compare and contrast threat actors, their attributes, and motivations.

- Actors: nation-state, unskilled attacker, hacktivist, insider threat,
  organized crime, and shadow IT.
- Attributes: internal/external position, resources/funding, and capability.
- Motivations: exfiltration, espionage, disruption, blackmail, financial gain,
  political/philosophical belief, ethics, revenge, chaos, and war.

### 2.2 Threat vectors and attack surfaces

Explain message, image, file, voice, removable-device, vulnerable-software,
unsupported-system, unsecure-network, exposed-service, default-credential,
supply-chain, and human/social-engineering vectors.

- Message vectors: email, SMS, and instant messaging.
- Network vectors: wireless, wired, Bluetooth, and open service ports.
- Supply chain: managed service providers, vendors, and suppliers.
- Social engineering: phishing, vishing, smishing, misinformation,
  impersonation, business email compromise, pretexting, watering holes, brand
  impersonation, and typosquatting.

### 2.3 Vulnerability types

Explain application, OS, web, hardware, virtualization, cloud, supply-chain,
cryptographic, misconfiguration, mobile, and zero-day vulnerabilities.

- Application: memory injection, buffer overflow, TOC/TOU race conditions,
  and malicious updates.
- Web: SQL injection and XSS.
- Hardware: firmware, end-of-life, and legacy exposure.
- Virtualization: VM escape and resource reuse.
- Mobile: sideloading and jailbreaking.

### 2.4 Indicators of malicious activity

Analyze malicious-activity indicators in a scenario.

- Malware: ransomware, Trojan, worm, spyware, bloatware, virus, keylogger,
  logic bomb, and rootkit.
- Physical: brute force, RFID cloning, and environmental attack.
- Network: DDoS, DNS, wireless, on-path, credential replay, and malicious
  code attacks.
- Application: injection, buffer overflow, replay, privilege escalation,
  forgery, and directory traversal.
- Cryptographic: downgrade, collision, and birthday attacks.
- Password: spraying and brute force.
- Indicators: lockout, concurrent session, blocked content, impossible travel,
  resource consumption/inaccessibility, out-of-cycle logging, published or
  documented indicators, and missing logs.

### 2.5 Enterprise mitigations

Explain the purpose of segmentation, access control/ACLs/permissions,
application allow lists, isolation, patching, encryption, monitoring, least
privilege, configuration enforcement, decommissioning, and hardening.

- Hardening includes encryption, endpoint protection, host firewall, HIPS,
  disabling ports/protocols, changing default passwords, and removing
  unnecessary software.

## 3.0 Security Architecture

### 3.1 Architecture models

Compare and contrast security implications of cloud, IaC, serverless,
microservices, network infrastructure, physical/logical isolation, SDN,
on-premises, centralized/decentralized, containerized, virtualized, IoT,
ICS/SCADA, RTOS, embedded, and high-availability models.

- Cloud topics: responsibility matrix, hybrid considerations, and third-party
  vendors.
- Consider availability, resilience, cost, responsiveness, scalability,
  deployment/recovery ease, risk transference, patch availability, power, and
  compute.

### 3.2 Securing enterprise infrastructure

Apply security principles to infrastructure scenarios.

- Consider device placement, zones, attack surface, connectivity, fail-open
  vs. fail-closed behavior, and active/passive or inline/tap devices.
- Appliances: jump servers, proxies, IDS/IPS, load balancers, and sensors.
- Port security: 802.1X and EAP.
- Firewalls: WAF, UTM, NGFW, layer 4, and layer 7.
- Secure access: VPN, remote access, TLS/IPSec tunneling, SD-WAN, and SASE.

### 3.3 Data protection

Compare and contrast data types, classifications, states, and protection
strategies.

- Types: regulated, trade secret, intellectual property, legal, financial,
  human-readable, and non-human-readable data.
- Classifications: sensitive, confidential, public, restricted, private, and
  critical.
- States: at rest, in transit, and in use; also data sovereignty and
  geolocation.
- Methods: geographic restrictions, encryption, hashing, masking,
  tokenization, obfuscation, segmentation, and permission restrictions.

### 3.4 Resilience and recovery

Explain high availability, site strategy, diversity, continuity, capacity,
testing, backup, and power considerations.

- High availability: load balancing vs. clustering.
- Sites: hot, cold, warm, and geographically dispersed.
- Testing: tabletop exercises, failover, simulation, and parallel processing.
- Backups: onsite/offsite, frequency, encryption, snapshots, recovery,
  replication, and journaling.
- Power: generators and UPS.

## 4.0 Security Operations

### 4.1 Security techniques for computing resources

Apply secure baselines and hardening to mobile devices, workstations,
switches, routers, cloud infrastructure, servers, ICS/SCADA, embedded/RTOS,
models, connection methods, WPA3/AAA/RADIUS, application security,
sandboxing, and monitoring.

### 4.2 Asset management

Explain security implications of acquisition/procurement, assignment and
accounting, ownership/classification, monitoring/inventory/enumeration, and
disposal/decommissioning, including sanitization, destruction, certification,
and retention.

### 4.3 Vulnerability management

Explain identification, analysis, response, validation, and reporting.

- Identify through scans, static/dynamic analysis, package monitoring, threat
  feeds, penetration testing, responsible disclosure, and audits.
- Analyze confirmation, false positives/negatives, prioritization, CVSS/CVE,
  classification, exposure, environment, business impact, and risk tolerance.
- Respond with patching, insurance, segmentation, compensating controls, or
  exceptions; validate through rescanning, audit, and verification.

### 4.4 Alerting and monitoring

Explain systems/application/infrastructure monitoring, aggregation,
alerting, scanning, reporting, archiving, response, quarantine, and tuning.
Tools include SCAP, benchmarks, agent/agentless methods, SIEM, antivirus,
DLP, SNMP traps, NetFlow, and vulnerability scanners.

### 4.5 Enhancing enterprise security

Modify firewall rules/ACLs/ports/screened subnets; IDS/IPS; web filters;
operating-system security; secure protocols; DNS and email security; file
integrity monitoring; DLP; NAC; EDR/XDR; and user-behavior analytics.

### 4.6 Identity and access management

Implement and maintain provisioning/deprovisioning, permissions, identity
proofing, federation, SSO (LDAP/OAuth/SAML), interoperability, attestation,
access-control models, MFA, password practices, and privileged-access tools.

### 4.7 Automation and orchestration

Explain automated provisioning, guard rails, security groups, tickets,
escalation, service/access control, CI/testing, integrations/APIs, benefits,

### 4.8 Incident response

Explain preparation, detection, analysis, containment, eradication, recovery,
hunting, and forensics: legal hold, chain of custody, acquisition, reporting,
preservation, and e-discovery.

### 4.9 Investigation data sources

Use firewall, application, endpoint, OS, IPS/IDS, and network logs plus
metadata, vulnerability scans, automated reports, dashboards, and packet
captures.

## 5.0 Security Program Management and Oversight

### 5.1 Security governance

Summarize guidelines; policies; standards; procedures; legal, regulatory, and
industry considerations; monitoring/revision; governance structures; and
system/data roles including owners, controllers, processors, and custodians.

### 5.2 Risk management

Explain risk identification, assessment, qualitative/quantitative analysis,
SLE/ALE/ARO, probability, likelihood, exposure factor, impact, risk registers,
tolerance/appetite, transfer/accept/avoid/mitigate strategies, reporting, and
business impact analysis with RTO/RPO/MTTR/MTBF.

### 5.3 Third-party risk

Explain vendor assessment and selection, due diligence, conflict of interest,

### 5.4 Security compliance

Summarize compliance reporting and monitoring, consequences of
non-compliance, due care/diligence, attestation, automation, privacy, legal
considerations, data subjects, controller/processor roles, ownership,

### 5.5 Audits and assessments

Explain attestation, internal/external audits, and penetration-testing forms:
physical, offensive, defensive, integrated, known/partially-known/unknown
environments, and passive/active reconnaissance.

### 5.6 Security awareness

Implement phishing awareness and reporting, anomalous behavior recognition,
user guidance/training, password/removable-media/social-engineering/OPSEC
guidance, hybrid-work considerations, and initial/recurring monitoring.

## Supplied lab resources

The source lists these sample resources for lab components.

- Equipment: tablet/laptop, web server, firewall, router, switch, IDS/IPS,
  wireless access point, VMs, email/DNS systems, IoT, hardware tokens, and
  smartphone.
- Tools: Wi-Fi, network-mapping, and NetFlow analyzers.
- Software: Windows/Linux/Kali, packet-capture and testing tools, static and
  dynamic analysis, scanners, emulators, sample code, editor, SIEM,
  keyloggers, MDM, VPN, DHCP, and DNS services.
- Other: cloud access, network documentation/diagrams, and sample logs.
