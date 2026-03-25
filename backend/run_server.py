"""
Test server startup with explicit error handling
"""
import sys
import traceback

try:
    import uvicorn
    from main import app
    
    print("✅ App imported successfully")
    print("🚀 Starting uvicorn server...")
    
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
    
    server = uvicorn.Server(config)
    server.run()
    
except KeyboardInterrupt:
    print("\n⚠️  Server stopped by user (CTRL+C)")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"\n📋 Traceback:")
    traceback.print_exc()
    sys.exit(1)
