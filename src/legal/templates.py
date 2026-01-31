from typing import List, Dict, Any

TEMPLATES = [
    {
        "id": "employment_sme",
        "name": "Standard SME Employment Agreement",
        "type": "Employment Agreement",
        "description": "A balanced employment contract designed for Indian SMEs with clear terms for salary, probation, and confidentiality.",
        "content": """EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into on [Date] by and between:

[Company Name], a company incorporated under the laws of India, having its registered office at [Address] (hereinafter referred to as the "Employer").

AND

[Employee Name], residing at [Address] (hereinafter referred to as the "Employee").

1. POSITION AND COMMENCEMENT
1.1 The Employee is appointed as [Position Name].
1.2 The employment shall commence on [Start Date].
1.3 The first [Number] months shall be a probationary period.

2. COMPENSATION AND BENEFITS
2.1 The Employee shall receive a gross annual salary of INR [Amount], payable in monthly installments.
2.2 Statutory benefits such as EPF and ESI shall be provided as per applicable Indian laws.

3. WORKING HOURS AND LEAVE
3.1 Standard working hours are [Start Time] to [End Time], Monday to [Friday/Saturday].
3.2 The Employee is entitled to [Number] days of paid annual leave.

4. CONFIDENTIALITY
The Employee agrees to maintain the strict confidentiality of all business secrets, client data, and proprietary information during and after the term of employment.

5. TERMINATION
5.1 During probation, either party may terminate with [Number] days' notice.
5.2 Post-probation, the notice period shall be [Number] days or salary in lieu thereof.

6. GOVERNING LAW
This Agreement shall be governed by the laws of India and subject to the jurisdiction of the courts in [City].

IN WITNESS WHEREOF, the parties have signed this Agreement on the date first mentioned above.

__________________________          __________________________
Employer Authorized Signatory       Employee
"""
    },
    {
        "id": "vendor_sme",
        "name": "SME-Friendly Vendor Service Agreement",
        "type": "Vendor Contract",
        "description": "A simplified service agreement for hiring vendors or consultants, focusing on clear deliverables and milestones.",
        "content": """SERVICE AGREEMENT (VENDOR)

This Service Agreement is made on [Date] between:

[SME Name] (hereinafter referred to as the "Client")
AND
[Vendor Name/Company] (hereinafter referred to as the "Service Provider")

1. SCOPE OF SERVICES
The Service Provider agrees to provide the following services: [Detailed description of services].

2. FEES AND PAYMENT
2.1 The total fee for the services shall be INR [Amount].
2.2 Payment shall be made as per the following milestones:
    - [Percentage]% on commencement.
    - [Percentage]% on [Milestone 1 Description].
    - [Percentage]% on completion and acceptance.
2.3 Client shall pay invoices within 15 days of receipt.

3. TERM AND TERMINATION
3.1 This agreement is valid from [Start Date] to [End Date].
3.2 Either party may terminate this agreement with 15 days' written notice.

4. INTELLECTUAL PROPERTY
Upon full payment, all intellectual property created as part of the services shall belong to the Client.

5. LIMITATION OF LIABILITY
Neither party shall be liable for any indirect or consequential damages. The total liability of either party shall not exceed the total fees paid under this agreement.

6. DISPUTE RESOLUTION
Any disputes shall be resolved through mutual discussion, failing which, via arbitration in [City], India.

__________________________          __________________________
Client Signature                    Service Provider Signature
"""
    },
    {
        "id": "lease_commercial_sme",
        "name": "SME Commercial Lease Agreement",
        "type": "Lease Agreement",
        "description": "Standard 11-month commercial lease format commonly used in India for office or shop spaces.",
        "content": """COMMERCIAL LEASE AGREEMENT (11 MONTHS)

This Lease Agreement is made on [Date] between:

[Lessor Name], residing at [Address] (hereinafter called the "Lessor")
AND
[SME/Lessee Name], represented by [Name], having office at [Address] (hereinafter called the "Lessee")

1. PREMISES
The Lessor hereby leases to the Lessee the premises located at [Shop/Office Full Address] (the "Premises").

2. TERM
The lease is for a fixed term of 11 months commencing from [Start Date].

3. RENT AND DEPOSIT
3.1 The monthly rent shall be INR [Amount], payable by the 5th of every month.
3.2 The Lessee has paid a security deposit of INR [Amount] (equivalent to [Number] months' rent).

4. USAGE
The Premises shall be used only for commercial purposes, specifically for [Nature of Business].

5. UTILITIES AND MAINTENANCE
5.1 Electricity and water charges shall be paid by the Lessee as per actual meter readings.
5.2 Routine maintenance shall be the responsibility of the Lessee. Major structural repairs shall be done by the Lessor.

6. TERMINATION
Either party may terminate the lease by giving one month's notice in writing.

7. STAMP DUTY AND REGISTRATION
The cost of stamp duty and registration of this agreement shall be borne equally by both parties.

__________________________          __________________________
Lessor Signature                    Lessee Signature
"""
    }
]
