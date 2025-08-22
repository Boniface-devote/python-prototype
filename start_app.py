#!/usr/bin/env python3
"""
Startup script for PDF Data Extractor
Runs both Flask backend and Next.js frontend
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask is not installed. Run: pip install -r requirements.txt")
        return False
    
    # Check if Node.js is installed
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js is installed: {result.stdout.strip()}")
        else:
            print("❌ Node.js is not installed")
            return False
    except FileNotFoundError:
        print("❌ Node.js is not installed")
        return False
    
    # Check if npm is installed
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm is installed: {result.stdout.strip()}")
        else:
            print("❌ npm is not installed")
            return False
    except FileNotFoundError:
        print("❌ npm is not installed")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies if needed"""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def start_backend():
    """Start the Flask backend"""
    print("🚀 Starting Flask backend...")
    try:
        # Start backend in background
        backend_process = subprocess.Popen([sys.executable, 'app.py'])
        time.sleep(3)  # Wait for backend to start
        
        # Check if backend is running
        try:
            import requests
            response = requests.get('http://localhost:5000/', timeout=5)
            if response.status_code == 200:
                print("✅ Backend is running on http://localhost:5000")
                return backend_process
        except:
            pass
        
        print("✅ Backend started (check http://localhost:5000)")
        return backend_process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend"""
    print("🚀 Starting Next.js frontend...")
    try:
        frontend_dir = Path("frontend")
        frontend_process = subprocess.Popen(['npm', 'run', 'dev'], cwd=frontend_dir)
        time.sleep(5)  # Wait for frontend to start
        
        print("✅ Frontend started on http://localhost:3000")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🚀 PDF Data Extractor - Starting up...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("\n❌ Failed to install frontend dependencies")
        return
    
    print("\n" + "=" * 50)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend")
        backend_process.terminate()
        return
    
    print("\n" + "=" * 50)
    print("🎉 Application is running!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend:  http://localhost:5000")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 50)
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
        
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
