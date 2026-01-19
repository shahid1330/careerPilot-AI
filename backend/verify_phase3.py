"""
Phase 3 Verification Script
Tests AI module imports and configuration
"""

import sys
sys.path.append(".")

print("=" * 60)
print("PHASE 3: AI/LLM INTEGRATION - VERIFICATION")
print("=" * 60)

try:
    # Test configuration
    print("\n1. Testing configuration...")
    from app.core.config import settings
    
    assert hasattr(settings, 'LLM_API_KEY'), "❌ LLM_API_KEY not in settings"
    assert hasattr(settings, 'LLM_MODEL_NAME'), "❌ LLM_MODEL_NAME not in settings"
    assert hasattr(settings, 'LLM_TIMEOUT'), "❌ LLM_TIMEOUT not in settings"
    assert hasattr(settings, 'LLM_MAX_TOKENS'), "❌ LLM_MAX_TOKENS not in settings"
    
    print(f"   ✅ LLM_MODEL_NAME: {settings.LLM_MODEL_NAME}")
    print(f"   ✅ LLM_TIMEOUT: {settings.LLM_TIMEOUT}s")
    print(f"   ✅ LLM_MAX_TOKENS: {settings.LLM_MAX_TOKENS}")
    print(f"   ✅ LLM_API_KEY: {'*' * 20}...{settings.LLM_API_KEY[-10:]}")
    
    # Test AI module imports
    print("\n2. Testing AI module imports...")
    from app.ai.groq_client import groq_client, GroqClient
    from app.ai.prompts import PromptTemplates
    print("   ✅ Groq client imported successfully")
    print("   ✅ Prompt templates imported successfully")
    
    # Test service imports
    print("\n3. Testing service imports...")
    from app.services.ai_service import AIService
    print("   ✅ AI service imported successfully")
    
    # Test schema imports
    print("\n4. Testing schema imports...")
    from app.schemas.ai import (
        RoadmapGenerateRequest,
        RoadmapResponse,
        DailyPlanGenerateRequest,
        DailyPlanResponse,
        TeachTopicRequest,
        TeachTopicResponse
    )
    print("   ✅ AI schemas imported successfully")
    
    # Test router imports
    print("\n5. Testing router imports...")
    from app.routers.ai import router
    print("   ✅ AI router imported successfully")
    
    # Verify router has endpoints
    print("\n6. Verifying router endpoints...")
    routes = [route.path for route in router.routes]
    expected_routes = ['/ai/generate-roadmap', '/ai/generate-daily-plan', '/ai/teach-topic']
    
    for route in expected_routes:
        if route in routes:
            print(f"   ✅ {route}")
        else:
            print(f"   ❌ {route} not found")
            raise Exception(f"Missing route: {route}")
    
    # Test prompt templates
    print("\n7. Testing prompt generation...")
    roadmap_prompt = PromptTemplates.roadmap_generation("Software Engineer")
    daily_plan_prompt = PromptTemplates.daily_plan_generation("Data Analyst", 7)
    teach_prompt = PromptTemplates.teach_topic("Python decorators")
    
    assert "Software Engineer" in roadmap_prompt, "❌ Role name not in roadmap prompt"
    assert "7-day" in daily_plan_prompt, "❌ Duration not in daily plan prompt"
    assert "Python decorators" in teach_prompt, "❌ Topic not in teach prompt"
    
    print("   ✅ Roadmap prompt generation works")
    print("   ✅ Daily plan prompt generation works")
    print("   ✅ Teaching prompt generation works")
    
    # Check httpx installation
    print("\n8. Checking dependencies...")
    try:
        import httpx
        print(f"   ✅ httpx version: {httpx.__version__}")
    except ImportError:
        print("   ❌ httpx not installed. Run: pip install httpx==0.26.0")
        raise
    
    # Test Groq client initialization
    print("\n9. Testing Groq client initialization...")
    assert groq_client.api_key is not None, "❌ Groq client API key not set"
    assert groq_client.model == settings.LLM_MODEL_NAME, "❌ Model mismatch"
    print(f"   ✅ Groq client initialized with model: {groq_client.model}")
    
    print("\n" + "=" * 60)
    print("🎉 ALL PHASE 3 VERIFICATION CHECKS PASSED!")
    print("=" * 60)
    print("\n✅ Phase 3 AI/LLM Integration is ready")
    print("✅ Run server: uvicorn main:app --reload")
    print("✅ Test endpoints at: http://localhost:8000/docs")
    print("\nPhase 3 Endpoints:")
    print("  • POST /ai/generate-roadmap")
    print("  • POST /ai/generate-daily-plan")
    print("  • POST /ai/teach-topic")
    print("\n" + "=" * 60)

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nMake sure you have installed all dependencies:")
    print("  pip install httpx==0.26.0")
    sys.exit(1)
except AssertionError as e:
    print(f"\n❌ Assertion Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
