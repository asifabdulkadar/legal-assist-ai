import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_pdf(filename, title, content):
    os.makedirs('samples', exist_ok=True)
    c = canvas.Canvas(f"samples/{filename}", pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 50, title)
    
    # Content
    c.setFont("Helvetica", 11)
    y = height - 100
    for line in content.split('\n'):
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        
        # Check if line is a header
        if line.strip().isupper() or line.strip().startswith('Section') or line.strip().startswith('Article'):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, line)
            c.setFont("Helvetica", 11)
        else:
            c.drawString(50, y, line)
        y -= 15
        
    c.save()

# 1. Employment Agreement (English)
employment_content = """EMPLOYMENT AGREEMENT

This Agreement is made on January 1, 2026, between ABC Solutions Pvt Ltd (Employer) and Rajesh Kumar (Employee).

1. POSITION AND DUTIES
The Employee is hired as a Senior Software Engineer. The Employee agrees to perform duties as assigned by the Employer.

2. COMPENSATION
The Employee shall receive a monthly salary of INR 80,000. 

3. CONFIDENTIALITY
The Employee shall not disclose any proprietary information of the Employer to any third party during or after the term of employment.

4. NON-COMPETE
The Employee agrees not to work for any competitor of the Employer for a period of 12 months after termination of employment within India.

5. TERMINATION
Either party may terminate this agreement by providing a notice period of 90 days. The Employer reserves the right to terminate the Employee immediately in case of gross misconduct without any notice or penalty.

6. INDEMNITY
The Employee agrees to indemnify and hold the Employer harmless against any losses caused by the Employee's negligence.

7. GOVERNING LAW
This agreement shall be governed by the laws of India and subject to the jurisdiction of courts in Bangalore.
"""

# 2. Vendor Agreement (Risk Sample)
vendor_content = """VENDOR SERVICE AGREEMENT

This agreement is entered into by Global Supplies Inc. (Client) and FastLogistics India (Vendor).

SECTION 1: SERVICES
Vendor shall provide logistics and warehousing services as described in Annexure A.

SECTION 2: PAYMENT
Client shall pay Vendor within 30 days of invoice receipt. Late payments will incur a penalty of 5% per month.

SECTION 3: LIABILITY
Vendor's liability for any loss or damage to goods is limited to INR 5,000 only, regardless of the actual value of goods.

SECTION 4: INDEMNIFICATION
Vendor shall indemnify Client against all claims, damages, and expenses arising out of Vendor's performance of services.

SECTION 5: TERMINATION
Client may terminate this agreement at any time without cause by giving 7 days written notice. Vendor must provide 60 days notice for termination.

SECTION 6: RESOLUTION OF DISPUTES
Any disputes shall be settled by arbitration in London, UK, under ICC rules.
"""

# 3. Simple Hindi Agreement
hindi_content = """किराया अनुबंध (LEASE AGREEMENT)

यह अनुबंध १ जनवरी २०२६ को श्री अमित शर्मा (मकान मालिक) और श्री विजय वर्मा (किरायेदार) के बीच किया गया है।

१. संपत्ति का विवरण
मकान नंबर १२३, शांति नगर, दिल्ली।

२. किराया
किरायेदार हर महीने की ५ तारीख तक १५,००० रुपये का किराया देगा।

३. सुरक्षा जमा (SECURITY DEPOSIT)
किरायेदार ५०,००० रुपये सुरक्षा जमा के रूप में देगा जो कि खाली करते समय वापस कर दिया जाएगा।

४. अवधि
यह अनुबंध ११ महीने की अवधि के लिए है।

५. बिजली और पानी
बिजली और पानी का बिल किरायेदार द्वारा अलग से दिया जाएगा।

६. क्षेत्राधिकार
किसी भी कानूनी विवाद का निपटारा दिल्ली की अदालतों में किया जाएगा।
"""

if __name__ == "__main__":
    print("Generating sample PDFs...")
    create_pdf("employment_sample.pdf", "Employment Agreement", employment_content)
    create_pdf("vendor_sample.pdf", "Vendor Agreement", vendor_content)
    # Note: ReportLab basic fonts don't support Hindi well without registering a TrueType font.
    # For simplicity, I'll provide a .txt and .docx version for Hindi if needed, 
    # but I'll create an English version of the Lease for the PDF demo.
    lease_en = """LEASE AGREEMENT

This Lease Agreement is made on January 1, 2026, between Mr. Amit Sharma (Lessor) and Mr. Vijay Verma (Lessee).

1. PREMISES
House No. 123, Shanti Nagar, Delhi.

2. RENT
The Lessee shall pay a monthly rent of INR 15,000.

3. SECURITY DEPOSIT
The Lessee shall deposit INR 50,000 as security, refundable at the end of the lease.

4. TERM
The lease is for a period of 11 months.

5. UTILITIES
Electricity and water bills shall be paid by the Lessee.

6. JURISDICTION
Any legal disputes shall be settled in the courts of Delhi.
"""
    create_pdf("lease_sample.pdf", "Lease Agreement", lease_en)
    
    # Write Hindi to text file for testing multilingual
    with open('samples/hindi_lease_sample.txt', 'w', encoding='utf-8') as f:
        f.write(hindi_content)
        
    print("Samples generated in 'samples/' directory.")
