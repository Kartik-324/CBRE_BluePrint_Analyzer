#backend/ai_processor.py
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
    
    async def get_comprehensive_analysis(self, image_path: str) -> Dict[str, Any]:
        """
        Automatic comprehensive analysis when blueprint is first uploaded
        Provides complete details of all rooms, dimensions, and features
        """
        question = """Please provide a COMPLETE and DETAILED analysis of this blueprint including:

**1. PROPERTY OVERVIEW**
   - Property type (residential, commercial, office, etc.)
   - Total floor area in square feet
   - Number of floors/levels shown
   - Building shape and orientation

**2. COMPLETE ROOM INVENTORY** (Count and list EVERY room with individual dimensions)
   - Bedrooms: Count each bedroom and provide dimensions (length × width in feet)
   - Bathrooms: Specify full bath, half bath, etc. with dimensions
   - Kitchen(s): Dimensions and layout type (L-shaped, galley, etc.)
   - Living Areas: Living room, family room, etc. with dimensions
   - Dining Areas: Formal dining, breakfast nook, etc. with dimensions
   - Utility Rooms: Laundry, mechanical room, storage with dimensions
   - Other Spaces: Home office, den, closets, hallways, foyer, etc. with dimensions
   - Outdoor Spaces: Patios, balconies, terraces if visible

**3. DETAILED DIMENSIONS**
   - Overall building dimensions (total length × width)
   - Individual room dimensions for EACH space identified above
   - Ceiling heights (if marked on blueprint)
   - Wall thickness measurements
   - Door widths and types (single, double, sliding, etc.)
   - Window dimensions and quantities

**4. ARCHITECTURAL FEATURES & ELEMENTS**
   - Main entry and all secondary entrances
   - Total number of doors (interior and exterior)
   - Total number of windows with placement
   - Stairs: Location, type, number of steps if visible
   - Elevators or lifts (if present)
   - Built-in features: Closets, cabinets, shelving
   - Fireplaces or special features
   - Structural elements: Columns, beams, load-bearing walls

**5. BUILDING SYSTEMS** (if visible on blueprint)
   - HVAC: Furnace location, AC units, vents, ductwork
   - Electrical: Panel locations, outlet placements, light fixtures
   - Plumbing: Fixtures in all bathrooms and kitchen, water heater location
   - Fire Safety: Smoke detectors, fire extinguishers, sprinkler systems
   - Special systems: Security, smart home features

**6. ACCESSIBILITY & CODE COMPLIANCE**
   - ADA accessibility features (ramps, wide doorways, etc.)
   - Emergency exits and egress routes
   - Handrails and grab bars
   - Code compliance observations
   - Safety features noted

**7. LAYOUT & CIRCULATION ASSESSMENT**
   - Traffic flow patterns and efficiency
   - Room adjacencies and relationships
   - Privacy zones (public vs private spaces)
   - Natural light and ventilation opportunities
   - Space utilization efficiency
   - Potential bottlenecks or circulation issues

**8. PROFESSIONAL OBSERVATIONS**
   - Strengths of the design
   - Potential concerns or limitations
   - Suggestions for optimization
   - Unique or notable design elements
   - Market appeal considerations

IMPORTANT: 
- Provide EXACT counts for all rooms
- Give SPECIFIC dimensions in feet and inches where visible
- Calculate total square footage
- Be thorough and leave nothing out
- Use clear formatting with bullet points
- If any measurement is not visible, state "Not marked on blueprint"
"""
        
        return await self.analyze_blueprint(image_path, question)
    
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