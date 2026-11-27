from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Project Documentation: GuardianNodes RoadSoS', border=0, ln=1, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_document():
    pdf = PDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "GuardianNodes RoadSoS", ln=True, align='C')
    pdf.set_font("Arial", "I", 14)
    pdf.cell(0, 10, "AI-Powered Emergency Road Accident Response System", ln=True, align='C')
    pdf.ln(10)
    
    # Team Info
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Team Name: Coders", ln=True)
    pdf.cell(0, 8, "Team Leader: Rohit Singh", ln=True)
    pdf.cell(0, 8, "Teammate: Shawsti Singh", ln=True)
    pdf.ln(10)
    
    # Project Overview
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "1. Project Overview", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "GuardianNodes RoadSoS is an advanced, production-grade emergency response dashboard built with Streamlit. It leverages artificial intelligence to rapidly assess accident severity and dynamically coordinates emergency vehicles using traffic-aware routing and simulated mesh communications.")
    pdf.ln(5)
    
    # Key Modules
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "2. Key Modules", ln=True)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "A. Intelligent Triage Engine", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "Uses a Zero-Shot Classification model (DistilBERT via HuggingFace) to analyze incoming incident reports in natural language. It extracts key entities (casualties, vehicles, hazards) and calculates an urgency score to prioritize emergency response.")
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "B. Graph Routing Engine", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "Utilizes NetworkX to build a road network graph. It applies Dijkstra's algorithm to calculate the optimal route for emergency vehicles (ambulances, fire engines, police, hazmat), factoring in real-time simulated traffic conditions.")
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "C. Mesh Protocol Simulator", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "Simulates a robust BLE/Wi-Fi Direct mesh network. It ensures that critical data packets reach the centralized dashboard even in remote areas or during communication breakdowns by hopping through intermediary nodes with CRC validation.")
    pdf.ln(5)

    # Technology Stack
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "3. Technology Stack", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "- Frontend: Streamlit (Python)", ln=True)
    pdf.cell(0, 8, "- Machine Learning: HuggingFace Transformers, PyTorch", ln=True)
    pdf.cell(0, 8, "- Data Structures & Routing: NetworkX", ln=True)
    pdf.cell(0, 8, "- Visualization: Plotly Express, Plotly Graph Objects", ln=True)
    pdf.cell(0, 8, "- Data Manipulation: Pandas, NumPy", ln=True)
    pdf.ln(5)

    # Future Scope
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "4. Future Scope & Impact", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "This system has the potential to be scaled nationally across all emergency control rooms. By dramatically reducing emergency response times and optimizing vehicle dispatch through predictive analytics, RoadSoS can save countless lives on the road.")

    pdf.output("RoadSoS_Project_Document.pdf")
    print("PDF created successfully as RoadSoS_Project_Document.pdf")

if __name__ == '__main__':
    create_document()
