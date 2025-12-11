import os
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.schema import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any

load_dotenv()


class BlueprintAnalyzer:
    """
    AI-powered blueprint analyzer using LangChain and OpenAI Vision
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o")  # Updated to gpt-4o
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", 0.3))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", 2000))
        
        # Initialize LangChain ChatOpenAI
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=self.api_key
        )
        
        # Enhanced system prompt for superior analysis
        self.system_prompt = """You are CBRE's elite AI architectural analyst with decades of expertise in blueprint interpretation, 
real estate development, and construction management. You provide institutional-grade analysis for Fortune 500 clients.

🎯 YOUR EXPERTISE:
- Licensed Architect with 20+ years experience
- LEED Accredited Professional
- Expert in commercial & residential real estate
- Proficient in all architectural symbols and building codes
- Specialist in space planning and utilization analysis

📋 ANALYSIS METHODOLOGY:
1. **Spatial Analysis**: Count and classify ALL spaces (rooms, corridors, utility areas)
2. **Dimensional Accuracy**: Provide precise measurements in feet and square footage
3. **Structural Assessment**: Identify walls (load-bearing vs partition), columns, beams
4. **Circulation Analysis**: Evaluate traffic flow, entry/exit points, accessibility
5. **Systems Integration**: Detail HVAC, electrical, plumbing, fire safety systems
6. **Code Compliance**: Note ADA accessibility, egress requirements, safety features
7. **Material Specifications**: Identify flooring, wall finishes, ceiling types when visible
8. **Functionality Review**: Assess layout efficiency and space optimization
9. **Special Features**: Highlight unique architectural elements, amenities, innovations

💎 RESPONSE QUALITY STANDARDS:
- Give EXACT numbers (room counts, dimensions, areas)
- Provide measurements in feet/inches and square footage
- Use professional architectural terminology
- Structure responses with clear sections and bullet points
- Include both micro-details AND big-picture insights
- Note confidence level (High/Medium/Low) for each finding
- Mention any assumptions based on visible information
- Suggest improvements or concerns when relevant

📊 OUTPUT FORMAT:
- Start with an executive summary (2-3 sentences)
- Organize details into clear sections with headers
- Use bullet points for easy scanning
- Provide specific numbers and measurements
- End with professional observations or recommendations

🏢 CBRE STANDARD:
Your analysis must meet institutional investment-grade quality - detailed enough for acquisition decisions,
accurate enough for due diligence, and clear enough for C-suite presentations."""

    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    async def analyze_blueprint(self, image_path: str, question: str) -> Dict[str, Any]:
        """
        Analyze blueprint image and answer questions with full context awareness
        """
        try:
            # Encode the image
            base64_image = self.encode_image(image_path)
            
            # Determine image format
            image_format = image_path.split('.')[-1].lower()
            mime_type = f"image/{image_format}" if image_format != "jpg" else "image/jpeg"
            
            # Enhanced prompt that maintains conversation context
            analysis_instruction = f"""🎯 ANALYSIS REQUEST:
{question}

📋 INSTRUCTION:
If this is a follow-up question (referring to "the bedrooms", "that area", "those dimensions", etc.), 
analyze the SAME blueprint again and provide the specific information requested, referencing your previous analysis.

For follow-up questions:
- Re-examine the blueprint for the specific detail requested
- Provide exact measurements and calculations
- Reference previous findings when relevant
- Be concise but complete

📊 REQUIRED DETAIL LEVEL:
- Provide comprehensive, institutional-grade analysis
- Include ALL specific measurements, counts, and dimensions
- Use professional architectural terminology
- Structure your response with clear sections
- Give executive summary first, then detailed findings
- Note confidence levels and any assumptions
- Include actionable insights when needed

Analyze this blueprint with the precision expected by CBRE's Fortune 500 clients."""
            
            # Create enhanced message with detailed instructions
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": analysis_instruction
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                                "detail": "high"  # Request high-detail analysis
                            }
                        }
                    ]
                )
            ]
            
            # Get response from OpenAI
            response = self.llm.invoke(messages)
            
            return {
                "answer": response.content,
                "confidence": "high",
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "answer": f"Error analyzing blueprint: {str(e)}",
                "confidence": "error",
                "model": self.model_name
            }
    
    def extract_measurements(self, text: str) -> Dict[str, Any]:
        """
        Extract measurements and numerical data from analysis
        """
        measurements = {
            "rooms": [],
            "dimensions": {},
            "total_area": None,
            "features": []
        }
        
        # This is a simple parser - can be enhanced with regex
        lines = text.split('\n')
        for line in lines:
            if 'room' in line.lower() or 'bedroom' in line.lower() or 'bathroom' in line.lower():
                measurements["rooms"].append(line.strip())
            elif 'sq ft' in line.lower() or 'square feet' in line.lower():
                measurements["total_area"] = line.strip()
            elif any(word in line.lower() for word in ['width', 'length', 'dimension']):
                measurements["dimensions"][line.split(':')[0].strip()] = line.split(':')[1].strip() if ':' in line else line
        
        return measurements
    
    async def get_room_count(self, image_path: str) -> Dict[str, Any]:
        """
        Specialized method to count rooms
        """
        question = "How many rooms are there in this blueprint? List each room type and count them separately (bedrooms, bathrooms, kitchen, living areas, etc.)"
        return await self.analyze_blueprint(image_path, question)
    
    async def get_dimensions(self, image_path: str) -> Dict[str, Any]:
        """
        Specialized method to get dimensions
        """
        question = "What are the dimensions of this blueprint? Provide width, length, and total square footage. Also provide dimensions for individual rooms if visible."
        return await self.analyze_blueprint(image_path, question)
    
    async def get_features(self, image_path: str) -> Dict[str, Any]:
        """
        Specialized method to identify features
        """
        question = "What are all the notable features in this blueprint? Include doors, windows, stairs, elevators, HVAC systems, electrical outlets, plumbing fixtures, and any special architectural elements."
        return await self.analyze_blueprint(image_path, question)