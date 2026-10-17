from pptx import Presentation
from pptx.util import Inches, Pt

def create_presentation():
    prs = Presentation()
    
    # 1. Welcome / Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide1 = prs.slides.add_slide(title_slide_layout)
    title1 = slide1.shapes.title
    subtitle1 = slide1.placeholders[1]
    
    title1.text = "Welcome to GuardianNodes RoadSoS"
    subtitle1.text = "AI-Powered Emergency Road Accident Response System\n\nTeam: Coders\nLeader: Rohit Singh\nTeammate: Shawsti Singh"

    # 2. Problem Statement
    bullet_slide_layout = prs.slide_layouts[1]
    slide2 = prs.slides.add_slide(bullet_slide_layout)
    shapes2 = slide2.shapes
    title2 = shapes2.title
    body2 = shapes2.placeholders[1]
    
    title2.text = "Problem Statement"
    tf2 = body2.text_frame
    tf2.text = "Delayed response times in emergency road accidents."
    p = tf2.add_paragraph()
    p.text = "Lack of coordinated routing for emergency vehicles."
    p = tf2.add_paragraph()
    p.text = "Communication breakdowns in remote areas."
    
    # 3. Our Solution
    slide3 = prs.slides.add_slide(bullet_slide_layout)
    shapes3 = slide3.shapes
    title3 = shapes3.title
    body3 = shapes3.placeholders[1]
    
    title3.text = "Our Solution"
    tf3 = body3.text_frame
    tf3.text = "Advanced AI-powered response system for immediate action."
    p = tf3.add_paragraph()
    p.text = "Intelligent incident triage using AI classification."
    p = tf3.add_paragraph()
    p.text = "Traffic-aware routing to ensure fastest emergency response."

    # 4. Key Features
    slide4 = prs.slides.add_slide(bullet_slide_layout)
    shapes4 = slide4.shapes
    title4 = shapes4.title
    body4 = shapes4.placeholders[1]
    
    title4.text = "Key Features"
    tf4 = body4.text_frame
    tf4.text = "🧠 AI Zero-Shot Classification Triage Engine"
    p = tf4.add_paragraph()
    p.text = "🗺️ NetworkX Dijkstra Traffic-Aware Routing"
    p = tf4.add_paragraph()
    p.text = "📡 BLE/Wi-Fi Mesh Protocol Simulator"
    p = tf4.add_paragraph()
    p.text = "📊 Real-Time Operations Metrics Dashboard"

    # 5. Technology Stack
    slide5 = prs.slides.add_slide(bullet_slide_layout)
    shapes5 = slide5.shapes
    title5 = shapes5.title
    body5 = shapes5.placeholders[1]
    
    title5.text = "Technology Stack"
    tf5 = body5.text_frame
    tf5.text = "Frontend: Streamlit"
    p = tf5.add_paragraph()
    p.text = "Language: Python 3.11+"
    p = tf5.add_paragraph()
    p.text = "AI/ML: HuggingFace Transformers, PyTorch"
    p = tf5.add_paragraph()
    p.text = "Routing & Visualization: NetworkX, Plotly"

    # 6. Future Scope & Impact
    slide6 = prs.slides.add_slide(bullet_slide_layout)
    shapes6 = slide6.shapes
    title6 = shapes6.title
    body6 = shapes6.placeholders[1]
    
    title6.text = "Future Scope & Impact"
    tf6 = body6.text_frame
    tf6.text = "Scalable to national emergency services."
    p = tf6.add_paragraph()
    p.text = "Predictive accident analytics based on historical data."
    p = tf6.add_paragraph()
    p.text = "Saving lives by reducing emergency response times significantly."

    # 7. Thank You Slide
    slide7 = prs.slides.add_slide(title_slide_layout)
    title7 = slide7.shapes.title
    subtitle7 = slide7.placeholders[1]
    
    title7.text = "Thank You!"
    subtitle7.text = "Any Questions?\n\nTeam: Coders\nLeader: Rohit Singh\nTeammate: Shawsti Singh"

    prs.save('Project_Presentation.pptx')
    print("Presentation created successfully as Project_Presentation.pptx")

if __name__ == '__main__':
    create_presentation()
