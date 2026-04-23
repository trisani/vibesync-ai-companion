 VibeSync: AI Emotional Companion

 Overview
VibeSync is a real-time emotion-aware AI system that detects facial expressions and generates context-aware conversational responses.


 Features
- Real-time emotion detection using webcam  
- Supports 7+ facial expressions (happy, sad, angry, etc.)  
- ~1 second response latency  
- Emotion-aware conversational responses  
- Multimodal interaction (text + voice)

 How It Works
- Captures live video input using OpenCV  
- Detects facial emotions using DeepFace  
- Maps detected emotion to contextual prompts  
- Generates responses using LLM (via Ollama API)

 Tech Stack
- Python  
- OpenCV  
- DeepFace  
- LLM Integration (Ollama)  
- Flask (if used)

## 📷 Demo

.png)

# System Architecture
1. Webcam input → Frame capture  
2. Emotion detection (DeepFace)  
3. Emotion-to-context mapping  
4. LLM generates response  
5. Output displayed (text/voice)
